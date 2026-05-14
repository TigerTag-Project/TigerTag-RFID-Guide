# TigerTag RFID Guide
# Copyright (C) 2025 TigerTag
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# Plug-and-play GitHub-mirror sync for the TigerTag reference JSONs.
#
# What it does on each run:
#   1. Fetches last_update.json from this repo's GitHub raw mirror
#   2. Compares every per-dataset timestamp to the local last_update.json
#   3. Downloads only the files whose timestamp has changed in the mirror
#
# First run downloads everything; subsequent runs are no-ops when nothing
# has changed. Drop this script wherever you want the JSON files to live
# and run it — no other setup needed.
#
# The mirror is auto-synced with the live TigerTag API every 6 hours by a
# GitHub Actions workflow, so the data is at most ~6 h stale. Use this
# variant when you don't need real-time freshness — it offloads bandwidth
# from the TigerTag API to the GitHub CDN. For real-time data, use
# Download_all_id_DB_API.py instead.

import json
import os
import sys

import requests

GITHUB_RAW_BASE = "https://raw.githubusercontent.com/TigerTag-Project/TigerTag-RFID-Guide/main/database"
HTTP_TIMEOUT = 30

# last_update key  ->  filename (same on both the GitHub mirror and locally)
DATASETS = {
    "versions":           "id_version.json",
    "types":              "id_type.json",
    "brands":             "id_brand.json",
    "filament_diameters": "id_diameter.json",
    "filament_materials": "id_material.json",
    "aspects":            "id_aspect.json",
    "measure_units":      "id_measure_unit.json",
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
    response = requests.get(f"{GITHUB_RAW_BASE}/last_update.json", timeout=HTTP_TIMEOUT)
    response.raise_for_status()
    return response.json(), response.text


def download_dataset(filename):
    url = f"{GITHUB_RAW_BASE}/{filename}"
    response = requests.get(url, timeout=HTTP_TIMEOUT)
    response.raise_for_status()
    try:
        data = response.json()
    except ValueError as e:
        raise RuntimeError(f"Invalid JSON received for {filename}: {e}")
    with open(os.path.join(TARGET_FOLDER, filename), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def sync():
    remote_data, remote_text = fetch_remote_last_update()
    local_data = load_local_last_update()

    updated = []
    for key, filename in DATASETS.items():
        remote_ts = remote_data.get(key)
        local_ts = local_data.get(key)
        local_file = os.path.join(TARGET_FOLDER, filename)

        if remote_ts is None:
            print(f"[skip] {key}: not present in mirror last_update payload")
            continue

        if remote_ts == local_ts and os.path.exists(local_file):
            print(f"[ok]   {filename}: up to date ({remote_ts})")
            continue

        print(f"[sync] {filename}: {local_ts} -> {remote_ts}")
        download_dataset(filename)
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
        print(f"error: GitHub request failed: {exc}", file=sys.stderr)
        sys.exit(1)

    if changed:
        print(f"\nUpdated {len(changed)} file(s):")
        for name in changed:
            print(f"  {name}")
    else:
        print("\nAll datasets already up to date.")
