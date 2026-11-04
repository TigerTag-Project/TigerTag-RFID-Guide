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

"""Split the product catalogue into one file per brand.

Reads `id_catalog.json` and writes `brands/id_<brand>.json`: the same products,
in the same order and the same format, one file per brand. A reader, a scale or
a brand's own tool can then embed only the brand it needs instead of the whole
catalogue (19 885 products, ~17 MB in November 2026).

Products are grouped by `RFID_Data.id_brand`, the id the chip carries, never by
the brand's display name. The file name is built from that name (`Rosa3D` →
`id_rosa3d.json`, `Bambu Lab` → `id_bambu_lab.json`); `brands/index.json` maps
every `id_brand` to its file, so a renamed brand never leaves a client guessing.

No network, nothing but the catalogue on disk: it runs after `db_update.py` in
the sync workflow. Files are rewritten only when their content changes, and a
brand that left the catalogue has its file removed, so the folder always mirrors
the catalogue exactly and an unchanged catalogue produces no commit.

Usage:
    python split_catalog.py           # write brands/
    python split_catalog.py --check   # report what would change, write nothing, exit 1
"""

import hashlib
import json
import os
import re
import sys
import unicodedata

TARGET_FOLDER = os.path.dirname(os.path.abspath(__file__))
CATALOG_PATH = os.path.join(TARGET_FOLDER, "id_catalog.json")
BRANDS_FOLDER = os.path.join(TARGET_FOLDER, "brands")
INDEX_FILE = "index.json"
INDEX_FORMAT = 1


def write_atomic(path, text):
    """Temp file + rename, as in db_update.py: a file is never half-written."""
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


def slugify(name):
    """`3DKordo (Everfil)` → `3dkordo_everfil`: ASCII, lower case, `_` between words."""
    ascii_name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", ascii_name.lower()).strip("_")


def render(items):
    """The exact format of `id_catalog.json`, so a brand file reads like a slice of it."""
    return json.dumps(items, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def read_text(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def split(catalog):
    """Group the catalogue by brand. Returns ({filename: (id_brand, brand, items)}, unassigned)."""
    groups, names, unassigned = {}, {}, 0
    for product in catalog:
        brand_id = (product.get("RFID_Data") or {}).get("id_brand")
        name = product.get("brand")
        if brand_id is None or not isinstance(name, str) or not slugify(name):
            unassigned += 1
            continue
        groups.setdefault(brand_id, []).append(product)
        names.setdefault(brand_id, name)

    # Two brands whose names reduce to the same slug keep their id in the file name.
    slugs = {}
    for brand_id, name in names.items():
        slugs.setdefault(slugify(name), []).append(brand_id)

    files = {}
    for brand_id, items in groups.items():
        slug = slugify(names[brand_id])
        if len(slugs[slug]) > 1:
            slug = f"{slug}_{brand_id}"
        files[f"id_{slug}.json"] = (brand_id, names[brand_id], items)
    return files, unassigned


def main(check_only=False):
    raw = read_text(CATALOG_PATH)
    if raw is None:
        raise RuntimeError("id_catalog.json not found — run db_update.py first")
    catalog = json.loads(raw)
    if not isinstance(catalog, list) or not catalog:
        raise RuntimeError("id_catalog.json is not a non-empty JSON array — refusing to split it")

    files, unassigned = split(catalog)
    changed, removed = [], []

    entries = []
    for filename in sorted(files, key=lambda n: files[n][1].lower()):
        brand_id, name, items = files[filename]
        text = render(items)
        data = text.encode("utf-8")
        entries.append({
            "id_brand": brand_id,
            "brand": name,
            "file": filename,
            "entries": len(items),
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        })
        path = os.path.join(BRANDS_FOLDER, filename)
        if read_text(path) != text:
            changed.append(filename)
            if not check_only:
                os.makedirs(BRANDS_FOLDER, exist_ok=True)
                write_atomic(path, text)

    # Remove the files of brands that left the catalogue (only our own id_*.json).
    if os.path.isdir(BRANDS_FOLDER):
        for name in sorted(os.listdir(BRANDS_FOLDER)):
            if name.startswith("id_") and name.endswith(".json") and name not in files:
                removed.append(name)
                if not check_only:
                    os.remove(os.path.join(BRANDS_FOLDER, name))

    index = {
        "format": INDEX_FORMAT,
        "source": "id_catalog.json",
        "sourceSha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
        "products": len(catalog),
        "unassigned": unassigned,
        "brands": entries,
    }
    index_text = json.dumps(index, ensure_ascii=False, indent=2) + "\n"
    index_path = os.path.join(BRANDS_FOLDER, INDEX_FILE)
    if read_text(index_path) != index_text:
        changed.append(INDEX_FILE)
        if not check_only:
            os.makedirs(BRANDS_FOLDER, exist_ok=True)
            write_atomic(index_path, index_text)

    print(f"[{'stale' if check_only and (changed or removed) else 'ok'}] brands/: {len(files)} brands, "
          f"{len(catalog) - unassigned} products"
          + (f", {unassigned} without a brand" if unassigned else ""))
    for name in changed:
        print(f"  {'would update' if check_only else 'updated'} {name}")
    for name in removed:
        print(f"  {'would remove' if check_only else 'removed'} {name}")
    return changed + removed


if __name__ == "__main__":
    check = "--check" in sys.argv
    try:
        changed = main(check_only=check)
    except (RuntimeError, ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
    sys.exit(1 if (check and changed) else 0)
