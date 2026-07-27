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
#
# Implementing the TigerTag protocol requires no licence and no payment.
# See LICENSING.md.

"""Mirror the full TigerTag product catalogue into `id_catalog.json`.

Companion to `db_update.py`, which syncs the small reference tables. This one
handles the product catalogue, and it differs in three ways that shape the
design:

* **It is paged.** `product/get/all` is a POST returning `items` plus a
  `nextPage` cursor, where every other dataset is a single GET.
* **It has no server-side timestamp.** `all/last_update` carries a key for each
  reference table but none for products, so there is nothing to compare before
  downloading. We fetch the whole catalogue every run and decide afterwards
  whether anything actually moved.
  (If a `products` key is ever added to `all/last_update`, this script should
  read it and skip the download entirely — see `check_last_update_gap`.)
* **It is two orders of magnitude bigger** (~3 000 products) than any reference
  table, so a needless rewrite is a needless commit in everyone's clone.

To keep the mirror diff-friendly the payload is normalised before writing:
products sorted by `id`, keys sorted within each product, two-space indent. A
re-run that changes nothing therefore produces a byte-identical file and the
script exits without touching it — which is what makes "commit only when the
catalogue really changed" possible.

Usage:
    python products_update.py           # sync
    python products_update.py --check   # exit 1 if the mirror is stale, write nothing
"""

import json
import os
import sys

import requests

API_BASE = "https://api.tigertag.io/api:tigertag"
HTTP_TIMEOUT = 60
PER_PAGE = 1000
# A runaway guard, NOT a catalogue-size limit: the loop follows `nextPage` until
# the API says there is none. Raise it if the catalogue ever exceeds this.
MAX_PAGES = 100

TARGET_FOLDER = os.path.dirname(os.path.abspath(__file__))
CATALOG_PATH = os.path.join(TARGET_FOLDER, "id_catalog.json")
LAST_UPDATE_PATH = os.path.join(TARGET_FOLDER, "last_update.json")


def fetch_all_products():
    """Walk every page of `product/get/all` and return the products as one list."""
    items, page, seen_pages = [], 1, 0
    while page and seen_pages < MAX_PAGES:
        response = requests.post(
            f"{API_BASE}/product/get/all",
            json={"page": page, "per_page": PER_PAGE},
            timeout=HTTP_TIMEOUT,
        )
        response.raise_for_status()
        payload = response.json()
        batch = payload.get("items") or []
        items.extend(batch)
        seen_pages += 1
        page = payload.get("nextPage")
        print(f"[page] {seen_pages}: +{len(batch)} products (total {len(items)})")
    if page:
        raise RuntimeError(
            f"stopped after {MAX_PAGES} pages with more to come — raise MAX_PAGES"
        )
    return items


def normalise(items):
    """Stable ordering so an unchanged catalogue produces an unchanged file."""
    return sorted(
        ({k: p[k] for k in sorted(p)} for p in items if p and p.get("id") is not None),
        key=lambda p: p["id"],
    )


def render(items):
    return json.dumps(items, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_atomic(path, text):
    """Write via a temp file + rename, so a good file is never half-replaced.

    `open(path, "w")` truncates BEFORE writing: a crash, a full disk or a killed
    process between those two moments leaves a truncated JSON that the app then
    fails to parse. `os.replace` is atomic on POSIX and on Windows, so the file at
    `path` is either entirely the old one or entirely the new one.
    """
    tmp = path + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except OSError:
                pass


def validate_dataset(data, filename):
    """Refuse anything that would silently destroy a good reference file.

    Every dataset here is a non-empty JSON array. A 200 response is NOT proof of
    a good payload: an API can answer `[]` during a migration, `{"error": ...}`
    on a soft failure, or an HTML page from a proxy — all of which parse or fail
    in ways that would otherwise overwrite live data. The bar is deliberately
    crude and absolute: a list, and not empty.
    """
    if not isinstance(data, list):
        raise RuntimeError(
            f"{filename}: expected a JSON array, got {type(data).__name__} — refusing to overwrite"
        )
    if not data:
        raise RuntimeError(f"{filename}: the API returned an EMPTY array — refusing to overwrite")


def read_local():
    if not os.path.exists(CATALOG_PATH):
        return None
    try:
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def stamp_last_update(items):
    """Record the catalogue's freshness alongside the reference tables.

    The value is the newest `updated_at` the catalogue carries, so it means the
    same thing as the other keys — when the DATA last changed, not when we last
    ran. Products without an `updated_at` are simply not candidates for the max;
    they cannot make the stamp look newer than it is.
    """
    stamps = [p["updated_at"] for p in items if isinstance(p.get("updated_at"), int)]
    if not stamps:
        return
    try:
        with open(LAST_UPDATE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        data = {}
    data["products"] = max(stamps)
    with open(LAST_UPDATE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
        f.write("\n")


def check_last_update_gap():
    """Say so, once, if the API gains the `products` key this script cannot use."""
    try:
        remote = requests.get(f"{API_BASE}/all/last_update", timeout=HTTP_TIMEOUT).json()
    except (requests.RequestException, ValueError):
        return
    if "products" in remote:
        print(
            "[note] `all/last_update` now carries a `products` timestamp — this "
            "script could skip the download entirely by comparing it first."
        )


def sync(check_only=False):
    items = normalise(fetch_all_products())
    if not items:
        raise RuntimeError("the API returned no products — refusing to overwrite the mirror")

    fresh, current = render(items), read_local()
    if fresh == current:
        print(f"[ok]   id_catalog.json: up to date ({len(items)} products)")
        return False

    if check_only:
        print(f"[stale] id_catalog.json differs from the API ({len(items)} products)")
        return True

    write_atomic(CATALOG_PATH, fresh)
    stamp_last_update(items)
    print(f"[sync] id_catalog.json: written ({len(items)} products)")
    return True


if __name__ == "__main__":
    check = "--check" in sys.argv
    try:
        changed = sync(check_only=check)
        check_last_update_gap()
    except (requests.RequestException, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
    sys.exit(1 if (check and changed) else 0)
