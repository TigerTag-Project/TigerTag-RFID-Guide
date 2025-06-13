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

import os
import requests

# List of URLs and corresponding filenames to download
json_files = [
    ("https://api.tigertag.io/api:tigertag/SpoolmanDB/materials", "materials.json")
]

# Target folder
target_folder = os.path.dirname(os.path.abspath(__file__))

def download_json_files():
    for url, filename in json_files:
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