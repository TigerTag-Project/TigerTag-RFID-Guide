#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
#
# TigerTag NFC (RFID-compatible) Guide
# Copyright (c) 2025-2026 TigerTag Corp.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Check the documentation for broken links and for facts that have diverged.

The same facts live in more than one place on purpose: `README.md` is written for
a human, the summary at the end of it and `llms.txt` are written for a model, and
all three repeat the chip count, the brand lists and the repository URLs. That
duplication is fine as long as a divergence is *visible*, which is what this
script is for. It does not deduplicate anything; it fails when the copies stop
agreeing.

Two passes:

* **Links.** Every local reference (`src=`, markdown links to files) must exist on
  disk, every in-page `#anchor` must match a real heading, and every external URL
  must answer. External rot needs no commit to happen — a site moves and the link
  dies quietly — which is why this also runs on a schedule, not only on push.

* **Facts.** Declared below. The check is written against the *pattern* a fact
  appears in, not against its value, so a stale copy is caught even in a form a
  plain text search would miss — a count URL-encoded inside a shields.io badge,
  for instance.

Usage:
    python tools/docs_check.py                # everything
    python tools/docs_check.py --no-external  # skip the network, for a fast local run
    python tools/docs_check.py --links-only
    python tools/docs_check.py --facts-only
"""

import argparse
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import unquote

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# The sub-directory READMEs are the ones that point at the asset and data files,
# so a rename that breaks them has to be caught here too. Their links are written
# relative to their OWN directory, which is why targets resolve against the
# document rather than against the repository root.
DOCS = ["README.md", "llms.txt", "brand/README.md", "database/README.md"]

# Docs whose backticked filenames name files sitting in that same directory, so a
# bare `name.svg` can be resolved and checked. The root README is deliberately not
# in here: it backticks bare names as labels for files that live elsewhere
# (`id_brand.json` is in database/, `logo_tigertag.svg` is in brand/), and the
# real path is carried by the link next to them.
BACKTICK_DOCS = {"brand/README.md", "database/README.md"}

HTTP_TIMEOUT = 20
MAX_WORKERS = 8
USER_AGENT = (
    "Mozilla/5.0 (compatible; TigerTag-docs-check/1.0; "
    "+https://github.com/TigerTag-Project/TigerTag-RFID-Guide)"
)

# Hosts that routinely refuse automated requests (bot walls, 403 on User-Agent,
# aggressive rate limits). A failure on these is reported as a warning and does
# NOT fail the run: a check that goes red for reasons nobody can fix is a check
# everybody learns to ignore, which is worse than not having one.
FLAKY_HOSTS = {
    "apps.apple.com",
    "play.google.com",
    "www.linkedin.com",
    "linkedin.com",
    "twitter.com",
    "x.com",
}

# ── Facts that must agree wherever they appear ──────────────────────────────
#
# Each entry is (name, pattern, expected). The pattern must capture exactly the
# part carrying the value. Anything the pattern matches whose capture differs
# from `expected` is a failure, reported with file:line.
VALUE_FACTS = [
    (
        "deployed chip count (prose)",
        re.compile(r"([\d,]+)\+ chips deployed"),
        "2,500,000",
    ),
    (
        "deployed chip count (metrics table)",
        re.compile(r"Chips deployed in production\s*\|\s*\*\*([\d,]+)\+\*\*"),
        "2,500,000",
    ),
    (
        "deployed chip count (README badge, URL-encoded)",
        re.compile(r"chips%20deployed-([^-\s\)]+)-"),
        "2.5M%2B",
    ),
]

# Enumerations that must stay complete. `anchor` identifies the sentence making
# the claim — deliberately not a heuristic over "any line mentioning a member",
# because members legitimately appear in smaller groups elsewhere (an image
# caption naming three of the five filament brands is not a claim about all of
# them). `window` is how many lines after the anchor the list may wrap onto.
LIST_FACTS = [
    (
        "printer / slicer integrations",
        re.compile(r"[Pp]rinters?\s*(?:/|and)\s*slicers?"),
        ["Snapmaker", "Bambu Lab", "FlashForge", "Elegoo", "Creality", "Anycubic"],
        3,
    ),
    (
        "filament / resin brands",
        re.compile(r"[Ff]ilament\s*(?:&|/|and)\s*resin brands"),
        ["eSun", "Rosa3D", "Sunlu", "R3D", "Landu"],
        3,
    ),
]

# ── Extraction ─────────────────────────────────────────────────────────────

RE_EXTERNAL = re.compile(r"https?://[^\s<>\"'\)\]\|]+")
# Deliberately matches the target of any `](...)`, without trying to parse what
# comes before it. A badge is a link wrapping an image — `[![alt](img)](#anchor)`
# — and a regex anchored on a leading `[` misses the outer target every time.
RE_MD_LINK = re.compile(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
RE_HTML_ATTR = re.compile(r"(?:src|href|srcset)=\"([^\"]+)\"")
RE_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*$")

# Not broken links: a localhost address is an instruction to run something
# yourself, and a URL carrying $placeholders or {braces} is a template showing
# the shape of a call, not an address anything can answer.
RE_PLACEHOLDER = re.compile(r"[${}<>]|\.\.\.")
LOCAL_HOSTS = ("localhost", "127.0.0.1", "0.0.0.0", "[::1]")


def is_probeable(url):
    host = re.sub(r"^https?://([^/:]+).*$", r"\1", url).lower()
    return host not in LOCAL_HOSTS and not RE_PLACEHOLDER.search(url)


def read_lines(relpath):
    with open(os.path.join(REPO_ROOT, relpath), "r", encoding="utf-8") as f:
        return f.read().splitlines()


def github_slug(heading):
    """Reproduce GitHub's heading -> anchor slug.

    Lowercase, drop everything that is not alphanumeric / space / hyphen /
    underscore (which is what removes emoji, em-dashes, dots and brackets), then
    spaces to hyphens. Runs of removed punctuation leave their spaces behind, so
    "5. Ecosystem — official tools" becomes "5-ecosystem--official-tools", with
    the doubled hyphen that the real anchors in this repo already carry.
    """
    text = heading.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return text.replace(" ", "-")


def collect_anchors(lines):
    """Every anchor the file defines, with GitHub's -1/-2 suffix on duplicates."""
    seen, anchors = {}, set()
    for line in lines:
        m = RE_HEADING.match(line)
        if not m:
            continue
        slug = github_slug(m.group(2))
        if not slug:
            continue
        n = seen.get(slug, 0)
        seen[slug] = n + 1
        anchors.add(slug if n == 0 else f"{slug}-{n}")
    return anchors


ASSET_EXT = (".svg", ".png", ".ico", ".icns", ".jpg", ".jpeg", ".json", ".py", ".yml", ".yaml")
RE_BACKTICK = re.compile(r"`([^`\s]+)`")


def backticked_assets(line):
    """Filenames named in prose as `like_this.svg` rather than linked.

    The brand and database READMEs list their assets in tables of backticked
    names, so a rename breaks them in a way no link check would ever see. Tokens
    carrying a glob or a slash are skipped: `id_*.json` is a pattern, and
    `icon.icns/ico/png` is three extensions written as one word, not a path.
    """
    for token in RE_BACKTICK.findall(line):
        if not token.lower().endswith(ASSET_EXT):
            continue
        if "*" in token or "/" in token:
            continue
        yield token


def collect_refs(relpath, lines):
    """Return (external, local, anchors) references as (value, line_no) pairs."""
    external, local, anchors = [], [], []
    in_code_fence = False
    for n, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue

        for url in RE_EXTERNAL.findall(line):
            external.append((url.rstrip(".,;:"), n))

        for target in RE_MD_LINK.findall(line) + RE_HTML_ATTR.findall(line):
            if target.startswith(("http://", "https://", "mailto:", "data:")):
                continue
            if target.startswith("#"):
                anchors.append((target[1:], n))
            else:
                local.append((target.split("#", 1)[0], n))

    return external, local, anchors


# ── Checks ─────────────────────────────────────────────────────────────────


def check_local_and_anchors(problems):
    for relpath in DOCS:
        lines = read_lines(relpath)
        _, local, anchors = collect_refs(relpath, lines)

        base = os.path.dirname(os.path.join(REPO_ROOT, relpath))
        for target, n in local:
            if not target:
                continue
            # Markdown percent-encodes spaces in paths ("Sample%20code/"), so the
            # link on the page is not the name on disk.
            resolved = os.path.normpath(os.path.join(base, unquote(target)))
            if not os.path.exists(resolved):
                problems.append(f"{relpath}:{n}  missing file: {target}")

        in_fence = False
        for n, line in enumerate(lines, 1) if relpath in BACKTICK_DOCS else []:
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for token in backticked_assets(line):
                if not os.path.exists(os.path.join(base, token)):
                    problems.append(f"{relpath}:{n}  backticked asset not found: {token}")

        if relpath.endswith(".md"):
            defined = collect_anchors(lines)
            for anchor, n in anchors:
                if anchor not in defined:
                    problems.append(f"{relpath}:{n}  anchor matches no heading: #{anchor}")


def check_external(problems, warnings):
    try:
        import requests
    except ImportError:
        warnings.append("requests is not installed — external links were not checked")
        return

    # One check per distinct URL, but report every line it appears on.
    where = {}
    for relpath in DOCS:
        external, _, _ = collect_refs(relpath, read_lines(relpath))
        for url, n in external:
            if not is_probeable(url):
                continue
            locations = where.setdefault(url, [])
            location = f"{relpath}:{n}"
            if location not in locations:
                locations.append(location)

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    def probe(url):
        # Retry connection-level failures: several of these URLs sit on the same
        # host, and probing them in parallel is enough to get one connection
        # dropped. A single transient reset must not turn the run red.
        last_error = None
        for attempt in range(3):
            try:
                r = session.head(url, timeout=HTTP_TIMEOUT, allow_redirects=True)
                # Plenty of servers do not implement HEAD properly.
                if r.status_code >= 400 or r.status_code == 405:
                    r = session.get(url, timeout=HTTP_TIMEOUT, allow_redirects=True, stream=True)
                    r.close()
                return url, r.status_code, None
            except requests.RequestException as exc:
                last_error = type(exc).__name__
                time.sleep(1.5 * (attempt + 1))
        return url, None, last_error

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        results = list(pool.map(probe, sorted(where)))

    for url, status, err in results:
        if status is not None and status < 400:
            continue
        host = re.sub(r"^https?://([^/]+).*$", r"\1", url).lower()
        detail = f"HTTP {status}" if status is not None else err
        locations = ", ".join(where[url])
        message = f"{locations}  {detail}: {url}"
        (warnings if host in FLAKY_HOSTS else problems).append(message)


def check_facts(problems):
    for relpath in DOCS:
        lines = read_lines(relpath)

        for name, pattern, expected in VALUE_FACTS:
            for n, line in enumerate(lines, 1):
                for found in pattern.findall(line):
                    if found != expected:
                        problems.append(
                            f"{relpath}:{n}  {name}: found {found!r}, expected {expected!r}"
                        )

        for name, anchor, members, window in LIST_FACTS:
            for n, line in enumerate(lines, 1):
                if not anchor.search(line):
                    continue
                span = "\n".join(lines[n - 1 : n - 1 + window])
                present = [
                    m for m in members
                    if re.search(rf"(?<!\w){re.escape(m)}(?!\w)", span)
                ]
                # The anchor also matches prose about the topic — "support across
                # multiple printer and slicer ecosystems" names no one. Two or more
                # members is what separates an actual enumeration from a mention.
                if len(present) < 2:
                    continue
                missing = [m for m in members if m not in present]
                if missing:
                    problems.append(
                        f"{relpath}:{n}  {name}: list is missing {', '.join(missing)}"
                    )


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--no-external", action="store_true",
                        help="skip network checks (local files, anchors and facts only)")
    parser.add_argument("--links-only", action="store_true")
    parser.add_argument("--facts-only", action="store_true")
    args = parser.parse_args()

    do_links = not args.facts_only
    do_facts = not args.links_only

    problems, warnings = [], []

    if do_links:
        check_local_and_anchors(problems)
        if not args.no_external:
            check_external(problems, warnings)
    if do_facts:
        check_facts(problems)

    for w in warnings:
        print(f"warning: {w}")

    if problems:
        print(f"\n{len(problems)} problem(s):", file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        return 1

    print("\nDocumentation check passed"
          + (f" ({len(warnings)} warning(s))" if warnings else "") + ".")
    return 0


if __name__ == "__main__":
    sys.exit(main())
