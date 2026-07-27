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

"""Incremental sync for the TigerTag reference JSON files.

Reads the API's `all/last_update` endpoint, compares each per-dataset
timestamp against the local `last_update.json`, and only re-downloads the
files whose server-side timestamp has changed. Designed to keep the GitHub
mirror nearly identical to the live API while minimising commits and API load.
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


def sync():
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

        print(f"[sync] {filename}: {local_ts} -> {remote_ts}")
        download_dataset(endpoint, filename)
        updated.append(filename)

    unknown_keys = set(remote_data) - set(DATASETS)
    for key in sorted(unknown_keys):
        print(f"[warn] unknown dataset key in API response: {key}")

    if updated or local_data != remote_data:
        write_atomic(LAST_UPDATE_PATH, remote_text)
        if "last_update.json" not in updated:
            updated.append("last_update.json")

    return updated


if __name__ == "__main__":
    try:
        changed = sync()
    except requests.RequestException as exc:
        print(f"error: API request failed: {exc}", file=sys.stderr)
        sys.exit(1)
    # A bad payload is not a network error, and it must not surface as a traceback.
    # Nothing was written when it fires — the guards run before any write.
    except (RuntimeError, ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    if changed:
        print(f"\nUpdated {len(changed)} file(s):")
        for name in changed:
            print(f"  {name}")
    else:
        print("\nAll datasets already up to date.")
