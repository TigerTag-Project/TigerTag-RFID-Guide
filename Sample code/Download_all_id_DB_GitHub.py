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

# GitHub-mirror version: pulls the JSON reference files from this repo's
# `database/` folder via raw.githubusercontent.com instead of hitting the
# live TigerTag API.
#
# The repo is auto-synced with the API every 6 hours by a GitHub Actions
# workflow, so this mirror is at most ~6 h behind the live data — fine for
# most offline / read-mostly use cases, and avoids putting load on the
# TigerTag API. For real-time data, use Download_all_id_DB_API.py instead.

import os
import requests

# Base URL for the GitHub raw mirror
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/TigerTag-Project/TigerTag-RFID-Guide/main/database"

# Files to download from the GitHub mirror
json_filenames = [
    "id_version.json",
    "id_material.json",
    "id_aspect.json",
    "id_type.json",
    "id_diameter.json",
    "id_brand.json",
    "id_measure_unit.json",
    "last_update.json",
]

# Target folder
target_folder = os.path.dirname(os.path.abspath(__file__))

def download_json_files():
    for filename in json_filenames:
        url = f"{GITHUB_RAW_BASE}/{filename}"
        file_path = os.path.join(target_folder, filename)
        try:
            print(f"Downloading {url}...")
            response = requests.get(url)
            response.raise_for_status()
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"Saved: {file_path}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")

if __name__ == "__main__":
    download_json_files()
