# SPDX-License-Identifier: Apache-2.0
#
# TigerTag RFID Guide
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

# Plug-and-play sync for the TigerTag reference JSONs with API primary
# and GitHub mirror fallback.
#
# What it does on each run:
#   1. Tries the live TigerTag API for the all/last_update manifest
#   2. If the API is unreachable (network error, timeout, HTTP 4xx/5xx, or
#      invalid JSON body), falls back to the GitHub mirror for the rest of
#      the run so the manifest and the dataset downloads stay coherent
#   3. Compares every per-dataset timestamp to the local last_update.json
#   4. Downloads only the files whose timestamp has changed on the chosen
#      source
#
# Use this script when you want real-time data but still want sync to keep
# working during an API outage. For pure-API see sync_id_database_api.py;
# for the mirror only (no API traffic, ~6 h stale) see
# sync_id_database_github.py.

import json
import os
import sys

import requests

API_BASE = "https://api.tigertag.io/api:tigertag"
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/TigerTag-Project/TigerTag-RFID-Guide/main/database"
HTTP_TIMEOUT = 30

# last_update key  ->  (API endpoint path, filename on disk and GitHub mirror)
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


def fetch_json(url):
    response = requests.get(url, timeout=HTTP_TIMEOUT)
    response.raise_for_status()
    return response.json(), response.text


def pick_source():
    """Return (source_name, last_update_data, last_update_text, dataset_url_for).

    dataset_url_for is a callable (endpoint, filename) -> URL pointing at the
    chosen source.
    """
    try:
        data, text = fetch_json(f"{API_BASE}/all/last_update")
        return (
            "api",
            data,
            text,
            lambda endpoint, filename: f"{API_BASE}/{endpoint}",
        )
    except (requests.RequestException, ValueError) as exc:
        print(
            f"[warn] API unreachable ({exc}); falling back to GitHub mirror",
            file=sys.stderr,
        )
        data, text = fetch_json(f"{GITHUB_RAW_BASE}/last_update.json")
        return (
            "github",
            data,
            text,
            lambda endpoint, filename: f"{GITHUB_RAW_BASE}/{filename}",
        )


def download_dataset(url, filename):
    response = requests.get(url, timeout=HTTP_TIMEOUT)
    response.raise_for_status()
    try:
        data = response.json()
    except ValueError as e:
        raise RuntimeError(f"Invalid JSON received for {filename}: {e}")
    with open(os.path.join(TARGET_FOLDER, filename), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def sync():
    source, remote_data, remote_text, dataset_url_for = pick_source()
    print(f"[info] source: {source}")
    local_data = load_local_last_update()

    updated = []
    for key, (endpoint, filename) in DATASETS.items():
        remote_ts = remote_data.get(key)
        local_ts = local_data.get(key)
        local_file = os.path.join(TARGET_FOLDER, filename)

        if remote_ts is None:
            print(f"[skip] {key}: not present in {source} last_update payload")
            continue

        if remote_ts == local_ts and os.path.exists(local_file):
            print(f"[ok]   {filename}: up to date ({remote_ts})")
            continue

        print(f"[sync] {filename}: {local_ts} -> {remote_ts}")
        download_dataset(dataset_url_for(endpoint, filename), filename)
        updated.append(filename)

    if updated or local_data != remote_data:
        with open(LAST_UPDATE_PATH, "w", encoding="utf-8") as f:
            f.write(remote_text)
        if "last_update.json" not in updated:
            updated.append("last_update.json")

    return updated


if __name__ == "__main__":
    try:
        changed = sync()
    except requests.RequestException as exc:
        print(
            f"error: both API and GitHub mirror requests failed: {exc}",
            file=sys.stderr,
        )
        sys.exit(1)

    if changed:
        print(f"\nUpdated {len(changed)} file(s):")
        for name in changed:
            print(f"  {name}")
    else:
        print("\nAll datasets already up to date.")
