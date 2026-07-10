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