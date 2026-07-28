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

"""Incremental sync for the TigerTag reference JSON files and the catalogue.

Reads the API's `all/last_update` endpoint, compares each per-dataset timestamp
against the local `last_update.json`, and only re-downloads the files whose
server-side timestamp has changed. Designed to keep the GitHub mirror nearly
identical to the live API while minimising commits and API load.

The product catalogue (`id_catalog.json`) rides along in the same run. It cannot
use the timestamp shortcut — see `sync_catalog` — so it is fetched every time and
compared byte-for-byte before anything is written.

Usage:
    python db_update.py           # sync
    python db_update.py --check   # report what is stale, write nothing, exit 1
"""

import json
import os
import sys

import requests

API_BASE = "https://api.tigertag.io/api:tigertag"
HTTP_TIMEOUT = 30

# last_update key  ->  (API endpoint path,           local filename)
DATASETS = {
    "versions":           ("version/get/all",            "id_version.json"),
    "types":              ("type/get/all",               "id_type.json"),
    "brands":             ("brand/get/all",              "id_brand.json"),
    "filament_diameters": ("diameter/filament/get/all",  "id_diameter.json"),
    "filament_materials": ("material/get/all",           "id_material.json"),
    "aspects":            ("aspect/get/all",             "id_aspect.json"),
    "measure_units":      ("measure_unit/get/all",       "id_measure_unit.json"),
}

TARGET_FOLDER = os.path.dirname(os.path.abspath(__file__))
LAST_UPDATE_PATH = os.path.join(TARGET_FOLDER, "last_update.json")


def load_local_last_update():
    if not os.path.exists(LAST_UPDATE_PATH):
        return {}
    try:
        with open(LAST_UPDATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def fetch_remote_last_update():
    response = requests.get(f"{API_BASE}/all/last_update", timeout=HTTP_TIMEOUT)
    response.raise_for_status()
    return response.json(), response.text


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


def download_dataset(endpoint, filename):
    url = f"{API_BASE}/{endpoint}"
    response = requests.get(url, timeout=HTTP_TIMEOUT)
    response.raise_for_status()
    try:
        data = response.json()
    except ValueError as e:
        raise RuntimeError(f"Invalid JSON received for {filename}: {e}")
    validate_dataset(data, filename)
    path = os.path.join(TARGET_FOLDER, filename)
    write_atomic(path, json.dumps(data, ensure_ascii=False, indent=2))
    return path


# ── The product catalogue ───────────────────────────────────────────────────
# Not in DATASETS above, because it does not behave like the reference tables:
# it is a paged POST rather than a single GET, and `all/last_update` carries no
# `products` key, so there is no server timestamp to compare before downloading.
#
# It lives here rather than in a script of its own so that "sync the database" is
# one command. A second script had to be remembered and invoked separately, and
# the workflow never did — which is how the catalogue sat frozen at whatever was
# committed by hand. The same folding was already done in TigerTag-Studio-Manager
# (`assets/db/tigertag/db_update.py`); keeping the two the same shape means a fix
# to one is a readable patch for the other.
CATALOG_FILE = "id_catalog.json"
CATALOG_KEY = "products"
CATALOG_PER_PAGE = 1000
CATALOG_MAX_PAGES = 100   # runaway guard, NOT a catalogue-size limit
# The reference tables are single small GETs; a catalogue page is 1 000 products,
# so it gets its own, longer budget.
CATALOG_TIMEOUT = 60

CATALOG_PATH = os.path.join(TARGET_FOLDER, CATALOG_FILE)


def fetch_catalog():
    """Walk every page of `product/get/all` and return the products as one list."""
    items, page, pages = [], 1, 0
    while page and pages < CATALOG_MAX_PAGES:
        response = requests.post(
            f"{API_BASE}/product/get/all",
            json={"page": page, "per_page": CATALOG_PER_PAGE},
            timeout=CATALOG_TIMEOUT,
        )
        response.raise_for_status()
        payload = response.json()
        batch = payload.get("items") or []
        items.extend(batch)
        pages += 1
        page = payload.get("nextPage")
        print(f"[page] {pages}: +{len(batch)} products (total {len(items)})")
    if page:
        raise RuntimeError(
            f"stopped after {CATALOG_MAX_PAGES} pages with more to come — raise CATALOG_MAX_PAGES"
        )
    return items


def read_catalog_local():
    if not os.path.exists(CATALOG_PATH):
        return None
    try:
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def sync_catalog(check_only=False):
    """Rewrite `id_catalog.json` only when the catalogue actually differs.

    There is no server-side timestamp to compare first, so the whole catalogue is
    downloaded every run and the decision is made afterwards. Products sorted by
    `id` and keys sorted within each product, so an unchanged catalogue renders
    byte-identical: no rewrite, no 1.5 MB diff in everyone's clone, and the
    `git diff` that DOES appear is a real change worth reading.

    Returns (changed, newest_updated_at).
    """
    items = sorted(
        ({k: p[k] for k in sorted(p)} for p in fetch_catalog() if p and p.get("id") is not None),
        key=lambda p: p["id"],
    )
    validate_dataset(items, CATALOG_FILE)

    fresh = json.dumps(items, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    current = read_catalog_local()

    # The catalogue's own newest `updated_at`, so the stamp means the same thing
    # as its neighbours: when the DATA last changed, not when this script ran.
    # Products without an `updated_at` are simply not candidates for the max;
    # they cannot make the stamp look newer than it is.
    newest = max(
        (p["updated_at"] for p in items if isinstance(p.get("updated_at"), int)),
        default=None,
    )

    if fresh == current:
        print(f"[ok]   {CATALOG_FILE}: up to date ({len(items)} products)")
        return False, newest

    if check_only:
        print(f"[stale] {CATALOG_FILE}: differs from the API ({len(items)} products)")
        return True, newest

    write_atomic(CATALOG_PATH, fresh)
    before = current.count('"id":') if current else 0
    print(f"[sync] {CATALOG_FILE}: {len(items)} products"
          + (f" (was {before})" if current else " (new file)"))
    return True, newest


def sync(check_only=False):
    remote_data, remote_text = fetch_remote_last_update()
    local_data = load_local_last_update()

    updated = []
    for key, (endpoint, filename) in DATASETS.items():
        remote_ts = remote_data.get(key)
        local_ts = local_data.get(key)
        local_file = os.path.join(TARGET_FOLDER, filename)

        if remote_ts is None:
            print(f"[skip] {key}: not present in API last_update payload")
            continue

        if remote_ts == local_ts and os.path.exists(local_file):
            print(f"[ok]   {filename}: up to date ({remote_ts})")
            continue

        if check_only:
            print(f"[stale] {filename}: {local_ts} -> {remote_ts}")
            updated.append(filename)
            continue

        print(f"[sync] {filename}: {local_ts} -> {remote_ts}")
        download_dataset(endpoint, filename)
        updated.append(filename)

    # Computed against the API's own payload, before the catalogue stamp below is
    # merged in — `products` is ours, and must not report itself as unknown.
    for key in sorted(set(remote_data) - set(DATASETS)):
        if key == CATALOG_KEY:
            print(f"[note] `all/last_update` now carries a `{CATALOG_KEY}` timestamp — "
                  "sync_catalog could compare it first and skip the download entirely.")
        else:
            print(f"[warn] unknown dataset key in API response: {key}")

    catalog_changed, catalog_newest = sync_catalog(check_only=check_only)
    if catalog_changed:
        updated.append(CATALOG_FILE)

    # `products` is OURS, not the API's — `all/last_update` has no such key. It is
    # merged into the payload rather than written from `remote_text`, which would
    # drop it on every run.
    if catalog_newest is not None:
        remote_data = {**remote_data, CATALOG_KEY: catalog_newest}
        remote_text = json.dumps(remote_data, ensure_ascii=False)

    if check_only:
        if local_data != remote_data and "last_update.json" not in updated:
            updated.append("last_update.json")
        return updated

    if updated or local_data != remote_data:
        write_atomic(LAST_UPDATE_PATH, remote_text)
        if "last_update.json" not in updated:
            updated.append("last_update.json")

    return updated


if __name__ == "__main__":
    check = "--check" in sys.argv
    try:
        changed = sync(check_only=check)
    except requests.RequestException as exc:
        print(f"error: API request failed: {exc}", file=sys.stderr)
        sys.exit(1)
    # A bad payload is not a network error, and it must not surface as a traceback.
    # Nothing was written when it fires — the guards run before any write.
    except (RuntimeError, ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    if changed:
        verb = "stale" if check else "Updated"
        print(f"\n{verb} {len(changed)} file(s):")
        for name in changed:
            print(f"  {name}")
    else:
        print("\nAll datasets already up to date.")

    sys.exit(1 if (check and changed) else 0)
