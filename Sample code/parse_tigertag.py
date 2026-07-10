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

"""
parse_tigertag.py — TigerTag NTAG213 Offline SDK  (v1.0)
=========================================================
Single-file, self-contained SDK for reading TigerTag RFID chips.

Spec    : https://github.com/TigerTag-Project/TigerTag-RFID-Guide
SDK repo: https://github.com/TigerTag-Project/tigertag-sdk-python

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCOPE — 100% OFFLINE MODE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  This SDK operates in pure offline mode: all filament data
  (temperatures, material, brand, colors…) is read directly from the
  NTAG213 chip. No API call is made to enrich or validate filament data.

  The only network activity is the optional download of reference JSON
  databases (id_material.json, id_brand.json…). These databases are
  used solely to resolve integer IDs into human-readable labels. They
  are cached locally and never queried during normal tag reads.

  ┌──────────────────────────────────────────────────────────────────┐
  │  TigerTag type    │  This SDK (Offline)     │  Future Online SDK │
  ├───────────────────┼─────────────────────────┼────────────────────┤
  │  TigerTag (Maker) │  ✅ full support         │  ✅ full support    │
  │  TigerTag Init    │  ✅ full support         │  ✅ full support    │
  │  TigerTag+        │  ✅ full support         │  ✅ chip + cloud    │
  │                   │  (identical to Maker)   │  (product API)     │
  └───────────────────┴─────────────────────────┴────────────────────┘

  TigerTag+ tags carry a cloud product ID (id_product ≠ 0xFFFFFFFF)
  alongside all standard filament data. This SDK reads all chip data
  identically for every tag type — there is no functional difference
  between TigerTag Maker and TigerTag+ in offline mode. The cloud
  product ID is exposed in to_dict() as product.id so callers can
  optionally query the TigerTag API themselves if needed.
  The Online SDK (coming later) will add that enrichment automatically:
    GET /product/get?uid={UID}&product_id={id_product}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUICK START
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  # 1. Install dependencies (see DEPENDENCIES section below)
  pip install requests cryptography

  # 2. Parse a tag (databases auto-downloaded on first run)
  python parse_tigertag.py dump.bin

  # 3. Use as a library in your project
  from parse_tigertag import TigerTag

  tag = TigerTag.from_dump(open("dump.bin", "rb").read())
  tag.sync_db()           # download/update reference databases (optional)
  print(tag.pretty())     # human-readable output
  print(tag.to_dict())    # dict for JSON serialization or API response
  print(tag.verify())     # ECDSA signature verification

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DEPENDENCIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  REQUIRED — core parsing (Python stdlib, no install needed):
    struct, json, os, sys, pathlib, dataclasses, datetime, typing

  REQUIRED for database sync (auto-download reference JSON files):
    pip install requests
    → https://docs.python-requests.org
    → Without this, databases must be present locally before use.

  OPTIONAL for ECDSA signature verification:
    pip install cryptography
    → https://cryptography.io/en/latest/installation/
    → Without this, verify() returns SignatureResult.NO_CRYPTO.

  Install everything at once:
    pip install requests cryptography

  Embedded / MicroPython environments:
    pip install micropython-urequests   # drop-in replacement for requests
    (ECDSA signature verification not available without cryptography)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BINARY LAYOUT — NTAG213 (pages 0x04-0x27, 144 bytes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Page      Offset  Size  Field                   Type
  ────────  ──────  ────  ──────────────────────  ────────
  0x04      +0      4B    ID TigerTag             u32 BE
  0x05      +4      4B    ID Product              u32 BE
  0x06      +8      2B    ID Material             u16 BE
  0x06      +10     1B    ID Aspect 1             u8
  0x06      +11     1B    ID Aspect 2             u8
  0x07      +12     1B    ID Type                 u8
  0x07      +13     1B    ID Diameter             u8
  0x07      +14     2B    ID Brand                u16 BE
  0x08      +16     4B    Color 1 (RGBA)          bytes
  0x09      +20     3B    Measure                 u24 BE
  0x09      +23     1B    ID Unit                 u8
  0x0A      +24     2B    Nozzle Temp Min         u16 BE  °C
  0x0A      +26     2B    Nozzle Temp Max         u16 BE  °C
  0x0B      +28     1B    Dry Temp                u8      °C
  0x0B      +29     1B    Dry Time                u8      hours
  0x0B      +30     1B    Bed Temp Min            u8      °C
  0x0B      +31     1B    Bed Temp Max            u8      °C
  0x0C      +32     4B    Twin Tag ID+Timestamp   u32 BE  sec since 2000-01-01 GMT
  0x0D      +36     3B    Color 2 (RGB)           bytes
  0x0D      +39     1B    Reserved                u8      = 0x00
  0x0E      +40     3B    Color 3 (RGB)           bytes
  0x0E      +43     1B    Reserved                u8      = 0x00
  0x0F      +44     2B    TD HueForge             u16 BE  value / 10
  0x0F      +46     2B    Reserved                u16     = 0x0000
  0x10-0x16 +48     28B   Custom Message          UTF-8
  0x17      +76     3B    Measure Available       u24 BE
  0x17      +79     1B    Reserved                u8      = 0x00
  0x18-0x1F +80     32B   Signature R (ECDSA)     bytes   optional
  0x20-0x27 +112    32B   Signature S (ECDSA)     bytes   optional

  Capacity : 80B user data + 64B signature = 144B = full NTAG213 user memory

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SIGNATURE ALGORITHM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Algorithm : ECDSA SECP256R1 (P-256)
  Hash      : SHA-256
  Message   : SHA-256( UID_bytes + block4 + block5 )

  Where:
    UID_bytes = 7 raw bytes from chip pages 0-1 (NOT hex string, NOT decimal)
                page0[0:3] + page1[0:4]
    block4    = page 0x04 bytes 0-3  (ID TigerTag, u32 BE)
    block5    = page 0x05 bytes 4-7  (ID Product,  u32 BE)

  The UID is used as raw binary bytes per ISO 14443 / NFC standard.
  The public key is stored in id_version.json ("public_key" field) and
  resolved automatically from the chip's id_tigertag value.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACCEPTED DUMP FORMATS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  180 bytes — full chip dump (pages 0-44): UID auto-extracted → signature verifiable
  144 bytes — user data + signature  (pages 0x04-0x27): signature NOT verifiable (no UID)
   80 bytes — user data only         (pages 0x04-0x17)
"""

from __future__ import annotations

# ──────────────────────────────────────────────────────────────────────────────
# Standard library (no install required)
# ──────────────────────────────────────────────────────────────────────────────
import json
import os
import struct
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# ──────────────────────────────────────────────────────────────────────────────
# Optional: requests  (pip install requests)
# Required for auto-downloading reference JSON databases
# ──────────────────────────────────────────────────────────────────────────────
try:
    import requests as _requests
    _REQUESTS_AVAILABLE = True
except ImportError:
    _REQUESTS_AVAILABLE = False

# ──────────────────────────────────────────────────────────────────────────────
# Optional: cryptography  (pip install cryptography)
# Required for ECDSA signature verification
# ──────────────────────────────────────────────────────────────────────────────
try:
    from cryptography.hazmat.primitives.asymmetric import ec as _ec
    from cryptography.hazmat.primitives import hashes as _hashes
    from cryptography.hazmat.primitives.serialization import load_pem_public_key as _load_pem_public_key
    from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature as _encode_dss_signature
    from cryptography.exceptions import InvalidSignature as _InvalidSignature
    _CRYPTO_AVAILABLE = True
except ImportError:
    _CRYPTO_AVAILABLE = False


# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

# Database sources
_API_BASE        = "https://api.tigertag.io/api:tigertag"
_GITHUB_RAW_BASE = "https://raw.githubusercontent.com/TigerTag-Project/TigerTag-RFID-Guide/main/database"
_HTTP_TIMEOUT    = 30

# Database files: last_update key → (API endpoint, local filename)
_DATASETS: Dict[str, tuple] = {
    "versions":           ("version/get/all",           "id_version.json"),
    "types":              ("type/get/all",              "id_type.json"),
    "brands":             ("brand/get/all",             "id_brand.json"),
    "filament_diameters": ("diameter/filament/get/all", "id_diameter.json"),
    "filament_materials": ("material/get/all",          "id_material.json"),
    "aspects":            ("aspect/get/all",            "id_aspect.json"),
    "measure_units":      ("measure_unit/get/all",      "id_measure_unit.json"),
}

# NTAG213 memory layout
CHIP_DUMP_LEN = 180   # full chip: 45 pages × 4B (pages 0-44)
FULL_DATA_LEN = 144   # user data + signature (pages 0x04-0x27)
MIN_DATA_LEN  = 80    # user data only        (pages 0x04-0x17)

# Epoch for TigerTag timestamps (seconds since this date)
_TIGERTAG_EPOCH = datetime(2000, 1, 1, tzinfo=timezone.utc)

# Product ID sentinel values
MAKER_PRODUCT_ID = 0xFFFFFFFF  # offline Maker tag
INIT_PRODUCT_ID  = 0x00000000  # blank / uninitialized tag


# ══════════════════════════════════════════════════════════════════════════════
# DATABASE SYNC
# ══════════════════════════════════════════════════════════════════════════════

def sync_databases(
    db_path: Path,
    force: bool = False,
    verbose: bool = True,
) -> List[str]:
    """
    Download or update TigerTag reference JSON databases.

    Tries the live TigerTag API first; falls back to the GitHub mirror if the
    API is unreachable. Only downloads files whose timestamp has changed.

    Args:
        db_path : Folder where JSON files are stored (created if missing).
        force   : Re-download all files even if already up to date.
        verbose : Print progress to stdout.

    Returns:
        List of filenames that were downloaded/updated.

    Raises:
        RuntimeError : if both API and GitHub mirror are unreachable.
        ImportError  : if 'requests' is not installed.

    Example:
        sync_databases(Path("./database"))
    """
    if not _REQUESTS_AVAILABLE:
        raise ImportError(
            "Database sync requires 'requests'.\n"
            "Install it with:  pip install requests"
        )

    db_path = Path(db_path)
    db_path.mkdir(parents=True, exist_ok=True)
    last_update_path = db_path / "last_update.json"

    def _get(url: str):
        r = _requests.get(url, timeout=_HTTP_TIMEOUT)
        r.raise_for_status()
        return r.json(), r.text

    def _log(msg: str):
        if verbose:
            print(msg)

    # Pick source: API first, GitHub fallback
    try:
        remote_data, remote_text = _get(f"{_API_BASE}/all/last_update")
        source = "api"
        def _dataset_url(endpoint: str, filename: str) -> str:
            return f"{_API_BASE}/{endpoint}"
    except Exception as exc:
        _log(f"[warn] TigerTag API unreachable ({exc}), falling back to GitHub mirror")
        try:
            remote_data, remote_text = _get(f"{_GITHUB_RAW_BASE}/last_update.json")
        except Exception as exc2:
            raise RuntimeError(
                f"Both API and GitHub mirror are unreachable.\n"
                f"API error:    {exc}\n"
                f"GitHub error: {exc2}\n"
                f"Check your internet connection."
            ) from exc2
        source = "github"
        def _dataset_url(endpoint: str, filename: str) -> str:
            return f"{_GITHUB_RAW_BASE}/{filename}"

    _log(f"[info] source: {source}")

    # Load local timestamps
    local_data: Dict = {}
    if last_update_path.exists():
        try:
            local_data = json.loads(last_update_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass

    updated: List[str] = []

    for key, (endpoint, filename) in _DATASETS.items():
        remote_ts = remote_data.get(key)
        local_ts  = local_data.get(key)
        local_file = db_path / filename

        if remote_ts is None:
            _log(f"[skip] {key}: not in last_update payload")
            continue

        if not force and remote_ts == local_ts and local_file.exists():
            _log(f"[ok]   {filename}: up to date")
            continue

        _log(f"[sync] {filename}: {local_ts} → {remote_ts}")
        r = _requests.get(_dataset_url(endpoint, filename), timeout=_HTTP_TIMEOUT)
        r.raise_for_status()
        data = r.json()
        local_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        updated.append(filename)

    if updated or local_data != remote_data:
        last_update_path.write_text(remote_text, encoding="utf-8")
        if "last_update.json" not in updated:
            updated.append("last_update.json")

    return updated


# ══════════════════════════════════════════════════════════════════════════════
# DATABASE LOADER
# ══════════════════════════════════════════════════════════════════════════════

class TigerTagDB:
    """
    Loads and exposes TigerTag JSON reference databases.

    All ID lookups return the full JSON entry dict (or None if not found).
    The JSON files are the single source of truth — no hardcoded ID mappings.

    Args:
        db_path     : Folder containing the JSON files.
        auto_sync   : Download missing/stale files automatically (requires requests).
        verbose     : Print sync progress.

    Example:
        db = TigerTagDB(Path("./database"), auto_sync=True)
        mat = db.material(38219)
        print(mat["label"])   # "PLA"
        print(mat["density"]) # 1.24
    """

    REQUIRED_FILES = list(_DATASETS.values())  # list of (endpoint, filename) tuples

    def __init__(
        self,
        db_path: Path = None,
        auto_sync: bool = True,
        verbose: bool = True,
    ):
        self._path = Path(db_path) if db_path else Path(__file__).parent / "database"
        self._auto_sync = auto_sync
        self._verbose = verbose
        self._ensure_db()
        self._versions   = self._load("id_version.json")
        self._materials  = self._load("id_material.json")
        self._aspects    = self._load("id_aspect.json")
        self._types      = self._load("id_type.json")
        self._diameters  = self._load("id_diameter.json")
        self._brands     = self._load("id_brand.json")
        self._units      = self._load("id_measure_unit.json")

    def _ensure_db(self) -> None:
        """Check for missing files; auto-sync or print clear error."""
        missing = [fn for _, fn in self.REQUIRED_FILES if not (self._path / fn).exists()]
        if not missing:
            return

        if self._auto_sync and _REQUESTS_AVAILABLE:
            print(f"[info] Missing {len(missing)} database file(s) — downloading now...")
            try:
                sync_databases(self._path, verbose=self._verbose)
                return
            except Exception as exc:
                print(f"[warn] Auto-sync failed: {exc}", file=sys.stderr)

        # Still missing after sync attempt (or auto_sync=False / no requests)
        missing_still = [fn for _, fn in self.REQUIRED_FILES if not (self._path / fn).exists()]
        if not missing_still:
            return

        sync_cmd = f'python "{Path(__file__).parent / "Sample code" / "sync_id_database_api_or_github.py"}"'
        print("", file=sys.stderr)
        print("❌  TigerTag database files not found.", file=sys.stderr)
        print(f"    Expected folder: {self._path.resolve()}", file=sys.stderr)
        print("", file=sys.stderr)
        print("    Missing files:", file=sys.stderr)
        for fn in missing_still:
            print(f"      • {fn}", file=sys.stderr)
        print("", file=sys.stderr)
        if not _REQUESTS_AVAILABLE:
            print("    ⚠️  'requests' is not installed — cannot auto-download.", file=sys.stderr)
            print("    Install it first:  pip install requests", file=sys.stderr)
            print("", file=sys.stderr)
        print("    ➜  Manual download:", file=sys.stderr)
        print(f"       {sync_cmd}", file=sys.stderr)
        print("", file=sys.stderr)
        sys.exit(1)

    def _load(self, filename: str) -> List[Dict]:
        fp = self._path / filename
        if not fp.exists():
            return []
        with open(fp, encoding="utf-8") as f:
            return json.load(f)

    def _find(self, table: List[Dict], id_value: int) -> Optional[Dict]:
        return next((e for e in table if e.get("id") == id_value), None)

    def sync(self, force: bool = False) -> List[str]:
        """Manually trigger a database update. Returns list of updated files."""
        updated = sync_databases(self._path, force=force, verbose=self._verbose)
        # Reload updated files
        self._versions   = self._load("id_version.json")
        self._materials  = self._load("id_material.json")
        self._aspects    = self._load("id_aspect.json")
        self._types      = self._load("id_type.json")
        self._diameters  = self._load("id_diameter.json")
        self._brands     = self._load("id_brand.json")
        self._units      = self._load("id_measure_unit.json")
        return updated

    # ── Lookups (return full JSON entry or None) ──────────────────────────────

    def version(self, id_value: int) -> Optional[Dict]:
        """id_version.json — includes public_key for signature verification."""
        return self._find(self._versions, id_value)

    def material(self, id_value: int) -> Optional[Dict]:
        """id_material.json — includes density, recommended temps, bambuID…"""
        return self._find(self._materials, id_value)

    def aspect(self, id_value: int) -> Optional[Dict]:
        """id_aspect.json — includes color_count."""
        return self._find(self._aspects, id_value)

    def type_(self, id_value: int) -> Optional[Dict]:
        """id_type.json."""
        return self._find(self._types, id_value)

    def diameter(self, id_value: int) -> Optional[Dict]:
        """id_diameter.json."""
        return self._find(self._diameters, id_value)

    def brand(self, id_value: int) -> Optional[Dict]:
        """id_brand.json."""
        return self._find(self._brands, id_value)

    def unit(self, id_value: int) -> Optional[Dict]:
        """id_measure_unit.json."""
        return self._find(self._units, id_value)

    @staticmethod
    def label(entry: Optional[Dict]) -> str:
        """Safe label from any DB entry dict."""
        if entry is None:
            return "Unknown"
        return entry.get("label") or entry.get("name") or "Unknown"


# ══════════════════════════════════════════════════════════════════════════════
# SIGNATURE RESULT
# ══════════════════════════════════════════════════════════════════════════════

class SignatureResult:
    """
    Result of an ECDSA signature verification.

    Attributes:
        status  : One of the class constants (VALID, INVALID, UNSIGNED, …)
        ok      : True only when status == VALID
        detail  : Human-readable explanation for failures

    Example:
        result = tag.verify()
        if result.ok:
            print("Authentic TigerTag")
        else:
            print(f"Problem: {result}")
    """

    VALID     = "valid"     # ✅ signature present and cryptographically correct
    INVALID   = "invalid"   # ❌ signature present but verification failed
    UNSIGNED  = "unsigned"  # ⬜ no signature (all zeros in pages 0x18-0x27)
    NO_CRYPTO = "no_crypto" # ⚠️  'cryptography' package not installed
    NO_KEY    = "no_key"    # ⚠️  public key missing from id_version.json
    NO_UID    = "no_uid"    # ⚠️  UID unavailable (partial dump, not 180 bytes)

    _ICONS = {
        VALID:     "✅ VALID",
        INVALID:   "❌ INVALID",
        UNSIGNED:  "⬜ NOT SIGNED",
        NO_CRYPTO: "⚠️  cryptography not installed — run: pip install cryptography",
        NO_KEY:    "⚠️  public key not found in id_version.json",
        NO_UID:    "⚠️  UID unavailable — provide a full 180-byte chip dump",
    }

    def __init__(self, status: str, detail: str = ""):
        self.status = status
        self.detail = detail
        self.ok     = (status == self.VALID)

    def __str__(self) -> str:
        base = self._ICONS.get(self.status, f"? {self.status}")
        return f"{base}  {self.detail}".rstrip()

    def __repr__(self) -> str:
        return f"SignatureResult(status={self.status!r}, ok={self.ok})"

    def to_dict(self) -> Dict:
        return {"status": self.status, "ok": self.ok, "detail": self.detail}


# ══════════════════════════════════════════════════════════════════════════════
# TIGERTAG — MAIN CLASS
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class TigerTag:
    """
    Parsed TigerTag NTAG213 payload.

    All fields are plain integers/bytes/strings. Use a TigerTagDB instance
    (via .db property or .resolve()) to get human-readable labels.

    Create instances with:
        TigerTag.from_dump(bytes)  — parse from binary dump
        TigerTag.from_file(path)   — parse from .bin file

    Example:
        tag = TigerTag.from_file("dump.bin")
        tag.sync_db()             # auto-download databases if needed
        print(tag.pretty())       # human-readable
        d = tag.to_dict()         # dict for JSON / API
        result = tag.verify()     # SignatureResult
    """

    # ── Identity ──────────────────────────────────────────────────────────────
    id_tigertag : int    # u32 BE — format/version identifier (see id_version.json)
    id_product  : int    # u32 BE — 0xFFFFFFFF=Maker, 0=Init, else cloud product ID

    # ── Material (all IDs resolve via TigerTagDB) ──────────────────────────────
    id_material : int    # u16 BE — see id_material.json
    id_aspect_1 : int    # u8    — see id_aspect.json
    id_aspect_2 : int    # u8    — see id_aspect.json
    id_type     : int    # u8    — see id_type.json (0x8E=Filament, 0xAD=Resin)
    id_diameter : int    # u8    — see id_diameter.json (0x38=1.75mm, 0xDD=2.85mm)
    id_brand    : int    # u16 BE — see id_brand.json

    # ── Colors ─────────────────────────────────────────────────────────────────
    color1_r : int       # Color 1 Red   (page 0x08)
    color1_g : int       # Color 1 Green
    color1_b : int       # Color 1 Blue
    color1_a : int       # Color 1 Alpha
    color2_r : int       # Color 2 Red   (page 0x0D)
    color2_g : int       # Color 2 Green
    color2_b : int       # Color 2 Blue
    color3_r : int       # Color 3 Red   (page 0x0E)
    color3_g : int       # Color 3 Green
    color3_b : int       # Color 3 Blue

    # ── Quantity ───────────────────────────────────────────────────────────────
    measure           : int  # u24 BE — quantity at manufacturing
    id_unit           : int  # u8    — see id_measure_unit.json
    measure_available : int  # u24 BE — remaining (updated by Tiger Scale)

    # ── Temperatures (°C) ─────────────────────────────────────────────────────
    nozzle_temp_min : int  # u16 BE — minimum nozzle temperature
    nozzle_temp_max : int  # u16 BE — maximum nozzle temperature
    dry_temp        : int  # u8
    dry_time        : int  # u8 hours
    bed_temp_min    : int  # u8
    bed_temp_max    : int  # u8

    # ── Traceability ──────────────────────────────────────────────────────────
    timestamp      : int   # u32 BE — seconds since 2000-01-01 GMT + twin tag pairing ID
    custom_message : str   # UTF-8, max 28 bytes (emoji allowed)

    # ── HueForge ──────────────────────────────────────────────────────────────
    td_raw : int           # u16 BE — actual TD = td_raw / 10  (0=undefined, 1-1000 valid)

    # ── Signature (optional, pages 0x18-0x27) ─────────────────────────────────
    signature_r : bytes = field(default_factory=lambda: bytes(32))
    signature_s : bytes = field(default_factory=lambda: bytes(32))

    # ── Chip UID (auto-extracted from full 180-byte dump, else None) ───────────
    uid : Optional[bytes] = field(default=None)

    # ── Internal: lazily loaded DB ────────────────────────────────────────────
    _db : Optional[TigerTagDB] = field(default=None, repr=False, compare=False)

    # ── Derived properties ────────────────────────────────────────────────────

    @property
    def is_maker(self) -> bool:
        return self.id_product == MAKER_PRODUCT_ID

    @property
    def is_init(self) -> bool:
        return self.id_product == INIT_PRODUCT_ID

    @property
    def is_signed(self) -> bool:
        return self.signature_r != bytes(32) or self.signature_s != bytes(32)

    @property
    def uid_hex(self) -> Optional[str]:
        """UID as uppercase hex string (e.g. '04AABBCCDDEE11'), or None."""
        return self.uid.hex().upper() if self.uid else None

    @property
    def td_value(self) -> float:
        """HueForge TD as float. 0.0=undefined, valid range 0.1–100.0."""
        return self.td_raw / 10.0

    @property
    def manufacturing_date(self) -> datetime:
        return datetime.fromtimestamp(
            _TIGERTAG_EPOCH.timestamp() + self.timestamp,
            tz=timezone.utc,
        )

    @property
    def color1_hex(self) -> str:
        return f"#{self.color1_r:02X}{self.color1_g:02X}{self.color1_b:02X}"

    @property
    def color2_hex(self) -> str:
        return f"#{self.color2_r:02X}{self.color2_g:02X}{self.color2_b:02X}"

    @property
    def color3_hex(self) -> str:
        return f"#{self.color3_r:02X}{self.color3_g:02X}{self.color3_b:02X}"

    @property
    def stock_percent(self) -> Optional[float]:
        if self.measure == 0:
            return None
        return round((self.measure_available / self.measure) * 100, 1)

    # ── Database ──────────────────────────────────────────────────────────────

    @property
    def db(self) -> TigerTagDB:
        """Lazily loaded database (auto-downloads if needed)."""
        if self._db is None:
            self._db = TigerTagDB()
        return self._db

    def sync_db(self, db_path: Path = None, force: bool = False) -> List[str]:
        """Download or update reference databases. Returns list of updated files."""
        path = db_path or (Path(__file__).parent / "database")
        self._db = TigerTagDB(path, auto_sync=True)
        return []

    # ── Constructors ──────────────────────────────────────────────────────────

    @classmethod
    def from_pages(cls, payload: bytes, uid: bytes, db: TigerTagDB = None) -> "TigerTag":
        """
        Parse a TigerTag from NFC SDK native output.  ← PRIMARY METHOD

        This is the recommended constructor for production use with any NFC SDK.
        The UID and payload are provided separately, exactly as NFC SDKs expose them.

        Args:
            payload : 80 or 144 bytes — pages 0x04 to 0x27 read by the NFC SDK.
                      80 bytes  = pages 0x04-0x17 (user data, no signature)
                      144 bytes = pages 0x04-0x27 (user data + ECDSA signature)
            uid     : 7-byte chip UID as returned natively by the NFC SDK.
                      Used as raw bytes for signature verification.
                      NOT a hex string, NOT a decimal integer — raw bytes only.
            db      : Optional pre-loaded TigerTagDB instance.

        Returns:
            TigerTag with .uid set and .verify() fully operational.

        Examples:
            # Android (NfcA / MifareUltralight)
            uid     = tag.id                          # ByteArray → bytes
            payload = mifare.readPages(4, 39)         # 144 bytes

            # iOS (CoreNFC)
            uid     = tag.identifier                  # Data → bytes
            payload = tag.readNDEF(...)               # pages 4-39

            # Flutter (flutter_nfc_kit)
            uid     = bytes.fromhex(tag.id)
            payload = await FlutterNfcKit.readBlock(4, length=144)

            # Python nfcpy / ACR122U
            uid     = tag.identifier                  # bytes
            payload = tag.read(4, 36)                 # 36 pages × 4 bytes

            # Arduino MFRC522
            uid     = mfrc522.uid.uidByte             # byte array
            # read pages 4-39 manually into payload buffer

            # Then in all cases:
            tag = TigerTag.from_pages(payload, uid=uid)
            result = tag.verify()  # ✅ fully autonomous
        """
        if len(payload) not in (MIN_DATA_LEN, FULL_DATA_LEN):
            raise ValueError(
                f"Invalid payload size: {len(payload)} bytes. "
                f"Expected 80B (pages 0x04-0x17) or 144B (pages 0x04-0x27)."
            )
        if not uid or len(uid) != 7:
            raise ValueError(
                f"Invalid UID: expected 7 bytes, got {len(uid) if uid else 0}. "
                f"Pass the raw bytes returned by your NFC SDK."
            )
        tag = cls.from_dump(payload, db=db)
        tag.uid = uid
        return tag

    @classmethod
    def from_dump(cls, data: bytes, db: TigerTagDB = None) -> "TigerTag":
        """
        Parse a TigerTag from a raw binary dump.

        Use this for full chip dumps (files, ACR122U raw read, testing).
        For production NFC SDK integration, prefer from_pages() instead.

        Args:
            data : Accepted sizes:
                   180 bytes — full NTAG213 chip dump (pages 0-44):
                               UID auto-extracted from system pages.
                   144 bytes — user data + signature (pages 0x04-0x27):
                               UID not available, signature cannot be verified.
                    80 bytes — user data only (pages 0x04-0x17).
            db   : Optional pre-loaded TigerTagDB instance.

        Raises:
            ValueError : if data length is not 80, 144, or 180 bytes.
        """
        uid: Optional[bytes] = None

        if len(data) == CHIP_DUMP_LEN:
            # Full chip dump: extract 7-byte UID from system pages, strip system+CFG
            # NTAG213 memory layout:
            #   Bytes   0-15  : system pages 0-3 (UID, BCC, lock, CC)
            #   Bytes  16-159 : user pages 4-39  (144 bytes, our payload)
            #   Bytes 160-179 : CFG pages 40-44  (configuration, ignored)
            #
            # UID layout in system pages:
            #   Page 0 [0:3] = UID[0], UID[1], UID[2]  (byte 3 = BCC0, not part of UID)
            #   Page 1 [0:4] = UID[3], UID[4], UID[5], UID[6]
            #   → 7-byte UID = bytes[0:3] + bytes[4:8]
            #
            # UID is used as RAW BYTES for signature verification
            # (NOT as hex string, NOT as decimal — raw binary per ISO 14443)
            uid  = data[0:3] + data[4:8]
            data = data[16:160]  # user data only: pages 0x04-0x27 (144 bytes)

        if len(data) not in (MIN_DATA_LEN, FULL_DATA_LEN):
            raise ValueError(
                f"Invalid dump size: {len(data)} bytes.\n"
                f"Accepted: 180B (full chip), 144B (user+sig), 80B (user only)."
            )

        def u8 (o: int) -> int: return data[o]
        def u16(o: int) -> int: return struct.unpack_from(">H", data, o)[0]
        def u24(o: int) -> int: return (data[o]<<16)|(data[o+1]<<8)|data[o+2]
        def u32(o: int) -> int: return struct.unpack_from(">I", data, o)[0]

        msg = data[48:76].rstrip(b"\x00").decode("utf-8", errors="replace")
        sig_r = data[80:112] if len(data) >= FULL_DATA_LEN else bytes(32)
        sig_s = data[112:144] if len(data) >= FULL_DATA_LEN else bytes(32)

        tag = cls(
            id_tigertag       = u32(0),
            id_product        = u32(4),
            id_material       = u16(8),
            id_aspect_1       = u8(10),
            id_aspect_2       = u8(11),
            id_type           = u8(12),
            id_diameter       = u8(13),
            id_brand          = u16(14),
            color1_r          = u8(16),
            color1_g          = u8(17),
            color1_b          = u8(18),
            color1_a          = u8(19),
            measure           = u24(20),
            id_unit           = u8(23),
            nozzle_temp_min   = u16(24),
            nozzle_temp_max   = u16(26),
            dry_temp          = u8(28),
            dry_time          = u8(29),
            bed_temp_min      = u8(30),
            bed_temp_max      = u8(31),
            timestamp         = u32(32),
            color2_r          = u8(36),
            color2_g          = u8(37),
            color2_b          = u8(38),
            color3_r          = u8(40),
            color3_g          = u8(41),
            color3_b          = u8(42),
            td_raw            = u16(44),
            custom_message    = msg,
            measure_available = u24(76),
            signature_r       = sig_r,
            signature_s       = sig_s,
            uid               = uid,
        )
        tag._db = db
        return tag

    @classmethod
    def from_file(cls, path, db: TigerTagDB = None) -> "TigerTag":
        """
        Parse a TigerTag from a .bin file.

        Args:
            path : Path to binary dump file (str or Path)
            db   : Optional pre-loaded TigerTagDB

        Example:
            tag = TigerTag.from_file("dump.bin")
        """
        with open(path, "rb") as f:
            return cls.from_dump(f.read(), db=db)

    # ── Serializer ────────────────────────────────────────────────────────────

    def to_bytes(self, include_signature: bool = False) -> bytes:
        """
        Serialize back to binary (pages 0x04 onward).
        Returns 80 bytes (user data) or 144 bytes (with signature).
        """
        def p16(v): return struct.pack(">H", v & 0xFFFF)
        def p24(v): v &= 0xFFFFFF; return bytes([(v>>16)&0xFF,(v>>8)&0xFF,v&0xFF])
        def p32(v): return struct.pack(">I", v & 0xFFFFFFFF)

        msg = self.custom_message.encode("utf-8")[:28]
        msg += bytes(28 - len(msg))

        data = (
            p32(self.id_tigertag)
            + p32(self.id_product)
            + p16(self.id_material)
            + bytes([self.id_aspect_1, self.id_aspect_2])
            + bytes([self.id_type, self.id_diameter])
            + p16(self.id_brand)
            + bytes([self.color1_r, self.color1_g, self.color1_b, self.color1_a])
            + p24(self.measure)
            + bytes([self.id_unit])
            + p16(self.nozzle_temp_min)
            + p16(self.nozzle_temp_max)
            + bytes([self.dry_temp, self.dry_time, self.bed_temp_min, self.bed_temp_max])
            + p32(self.timestamp)
            + bytes([self.color2_r, self.color2_g, self.color2_b])
            + b"\x00"
            + bytes([self.color3_r, self.color3_g, self.color3_b])
            + b"\x00"
            + p16(self.td_raw)
            + b"\x00\x00"
            + msg
            + p24(self.measure_available)
            + b"\x00"
        )

        assert len(data) == MIN_DATA_LEN

        if include_signature:
            data += (self.signature_r + bytes(32))[:32]
            data += (self.signature_s + bytes(32))[:32]

        return data

    # ── Validation ────────────────────────────────────────────────────────────

    def validate(self) -> List[str]:
        """
        Basic field-level sanity checks.
        Returns list of warning strings. Empty = no issues.

        Example:
            warnings = tag.validate()
            for w in warnings:
                print(f"⚠  {w}")
        """
        warnings = []
        if self.nozzle_temp_min > self.nozzle_temp_max > 0:
            warnings.append(f"Nozzle temp min ({self.nozzle_temp_min}°C) > max ({self.nozzle_temp_max}°C)")
        if self.bed_temp_min > self.bed_temp_max > 0:
            warnings.append(f"Bed temp min ({self.bed_temp_min}°C) > max ({self.bed_temp_max}°C)")
        if self.td_raw != 0 and not (10 <= self.td_raw <= 1000):
            warnings.append(f"TD HueForge out of range: {self.td_raw} (valid: 10–1000 or 0=undefined)")
        if self.measure > 0 and self.measure_available > self.measure:
            warnings.append(f"measure_available ({self.measure_available}) > initial measure ({self.measure})")
        if len(self.custom_message.encode("utf-8")) > 28:
            warnings.append("custom_message exceeds 28 bytes")
        return warnings

    # ── Signature verification ────────────────────────────────────────────────

    def verify(self, db: TigerTagDB = None) -> SignatureResult:
        """
        Verify the ECDSA-P256 signature — fully autonomous.

        The signed message is: SHA-256( uid_bytes + block4 + block5 )
          uid_bytes = 7 raw bytes from chip pages 0-1
                      (raw binary, NOT hex string, NOT decimal — per ISO 14443)
          block4    = id_tigertag as 4-byte big-endian (page 0x04)
          block5    = id_product  as 4-byte big-endian (page 0x05)

        The public key is read automatically from id_version.json.

        Returns:
            SignatureResult with .ok (bool) and .status (str)

        Requires:
            - 180-byte chip dump (for UID extraction)
            - pip install cryptography
            - id_version.json with "public_key" field

        Example:
            result = tag.verify()
            print(result)        # ✅ VALID  /  ❌ INVALID  /  ⬜ NOT SIGNED  …
            print(result.ok)     # True / False
        """
        if not self.is_signed:
            return SignatureResult(SignatureResult.UNSIGNED)

        if not _CRYPTO_AVAILABLE:
            return SignatureResult(SignatureResult.NO_CRYPTO)

        if not self.uid:
            return SignatureResult(
                SignatureResult.NO_UID,
                "Provide a full 180-byte chip dump (system pages 0-3 include the UID).",
            )

        _db = db or self.db
        version_entry = _db.version(self.id_tigertag) or {}
        pem = version_entry.get("public_key", "").strip()
        if not pem:
            return SignatureResult(
                SignatureResult.NO_KEY,
                f"No public_key in id_version.json for 0x{self.id_tigertag:08X}.",
            )

        try:
            # Signed message: UID (raw bytes) + block4 + block5
            # UID is used as 7 raw binary bytes, which is the NFC/ISO 14443 standard.
            # NOT as a hex string, NOT as a decimal integer — raw bytes only.
            block4  = self.id_tigertag.to_bytes(4, "big")
            block5  = self.id_product.to_bytes(4, "big")
            message = self.uid + block4 + block5

            r   = int.from_bytes(self.signature_r, "big")
            s   = int.from_bytes(self.signature_s, "big")
            der = _encode_dss_signature(r, s)

            pub = _load_pem_public_key(pem.encode())
            pub.verify(der, message, _ec.ECDSA(_hashes.SHA256()))

            return SignatureResult(SignatureResult.VALID)

        except _InvalidSignature:
            return SignatureResult(
                SignatureResult.INVALID,
                "Signature does not match — tag may be cloned or tampered.",
            )
        except Exception as exc:
            return SignatureResult(SignatureResult.INVALID, f"Verification error: {exc}")

    # ── Output ────────────────────────────────────────────────────────────────

    def to_dict(self, db: TigerTagDB = None) -> Dict:
        """
        Return a fully-resolved dict (all IDs replaced by their labels + metadata).
        Suitable for JSON serialization, API responses, or further processing.

        Example:
            import json
            print(json.dumps(tag.to_dict(), indent=2))
        """
        _db   = db or self.db
        mat   = _db.material(self.id_material) or {}
        rec   = mat.get("recommended", {})
        stock = self.stock_percent

        return {
            "sdk":        "tigertag-sdk-python",
            "sdk_mode":   "offline",          # reads chip data only — no API enrichment
            "protocol":   "TigerTag Open Source v2.0",
            "chip":       "NTAG213",
            "uid":        self.uid_hex,
            "version": {
                "id":    self.id_tigertag,
                "hex":   f"0x{self.id_tigertag:08X}",
                "label": TigerTagDB.label(_db.version(self.id_tigertag)),
            },
            "product": {
                "id":   self.id_product,
                "mode": "maker" if self.is_maker else "init" if self.is_init else "cloud",
                # TigerTag+ (mode=cloud): id_product is a cloud product ID.
                # This SDK reads it from the chip like any other field.
                # To retrieve enriched product data from the TigerTag cloud:
                #   GET https://api.tigertag.io/api:tigertag/product/get
                #         ?uid={uid_hex}&product_id={id_product}
                # (handled by the future tigertag-sdk-online, not this SDK)
            },
            "material": {
                "id":      self.id_material,
                "label":   TigerTagDB.label(_db.material(self.id_material)),
                "density": mat.get("density"),
                "filled":  mat.get("filled"),
                "recommended": {
                    "nozzle": {"min": rec.get("nozzleTempMin"), "max": rec.get("nozzleTempMax")},
                    "bed":    {"min": rec.get("bedTempMin"),    "max": rec.get("bedTempMax")},
                    "dry":    {"temp": rec.get("dryTemp"),      "time_h": rec.get("dryTime")},
                } if rec else None,
                "metadata": mat.get("metadata"),
            },
            "aspect_1": {"id": self.id_aspect_1, "label": TigerTagDB.label(_db.aspect(self.id_aspect_1))},
            "aspect_2": {"id": self.id_aspect_2, "label": TigerTagDB.label(_db.aspect(self.id_aspect_2))},
            "type":     {"id": self.id_type,     "label": TigerTagDB.label(_db.type_(self.id_type))},
            "diameter": {"id": self.id_diameter, "label": TigerTagDB.label(_db.diameter(self.id_diameter))},
            "brand":    {"id": self.id_brand,    "label": TigerTagDB.label(_db.brand(self.id_brand))},
            "colors": {
                "primary":   {"hex": self.color1_hex, "rgba": [self.color1_r, self.color1_g, self.color1_b, self.color1_a]},
                "secondary": {"hex": self.color2_hex, "rgb":  [self.color2_r, self.color2_g, self.color2_b]},
                "tertiary":  {"hex": self.color3_hex, "rgb":  [self.color3_r, self.color3_g, self.color3_b]},
            },
            "hueforge_td": self.td_value if self.td_raw != 0 else None,
            "unit": {"id": self.id_unit, "label": TigerTagDB.label(_db.unit(self.id_unit))},
            "measure": {
                "initial":   self.measure,
                "available": self.measure_available,
                "percent":   stock,
            },
            "temperatures": {
                "nozzle": {"min": self.nozzle_temp_min, "max": self.nozzle_temp_max},
                "bed":    {"min": self.bed_temp_min,    "max": self.bed_temp_max},
                "dry":    {"temp": self.dry_temp,       "time_h": self.dry_time},
            },
            "timestamp":           self.timestamp,
            "manufacturing_date":  self.manufacturing_date.isoformat(),
            "twin_tag_pairing_id": self.timestamp,
            "custom_message":      self.custom_message,
            "signed":              self.is_signed,
        }

    def pretty(self, db: TigerTagDB = None, sig_result: SignatureResult = None) -> str:
        """
        Human-readable summary of the tag.

        Args:
            db         : Optional TigerTagDB (uses self.db by default)
            sig_result : Optional pre-computed SignatureResult

        Example:
            print(tag.pretty())
        """
        _db   = db or self.db
        mat   = _db.material(self.id_material) or {}
        rec   = mat.get("recommended", {})
        stock = self.stock_percent
        ul    = TigerTagDB.label(_db.unit(self.id_unit))
        sig   = str(sig_result) if sig_result else ("signed ✓" if self.is_signed else "not signed")

        def rec_note(kmin, kmax, suffix="°C"):
            return f"  (DB: {rec[kmin]}–{rec[kmax]}{suffix})" if rec.get(kmin) is not None else ""

        return (
            f"┌─ TigerTag ────────────────────────────────────────────\n"
            f"│  Version      {TigerTagDB.label(_db.version(self.id_tigertag))} (0x{self.id_tigertag:08X})\n"
            f"│  Product      {'Maker (offline)' if self.is_maker else f'Cloud #{self.id_product}'}\n"
            f"│  UID          {self.uid_hex or '— (partial dump)'}\n"
            f"├─ Material ────────────────────────────────────────────\n"
            f"│  Material     {TigerTagDB.label(_db.material(self.id_material))}  (id={self.id_material})\n"
            f"│  Density      {mat.get('density', '—')} g/cm³\n"
            f"│  Type         {TigerTagDB.label(_db.type_(self.id_type))}\n"
            f"│  Diameter     {TigerTagDB.label(_db.diameter(self.id_diameter))}\n"
            f"│  Brand        {TigerTagDB.label(_db.brand(self.id_brand))}\n"
            f"│  Aspect 1     {TigerTagDB.label(_db.aspect(self.id_aspect_1))}\n"
            f"│  Aspect 2     {TigerTagDB.label(_db.aspect(self.id_aspect_2))}\n"
            f"├─ Colors ──────────────────────────────────────────────\n"
            f"│  Color 1      {self.color1_hex}  α={self.color1_a}\n"
            f"│  Color 2      {self.color2_hex}\n"
            f"│  Color 3      {self.color3_hex}\n"
            f"│  HueForge TD  {self.td_value:.1f}" + (" (undefined)\n" if self.td_raw == 0 else "\n") +
            f"├─ Temperatures ────────────────────────────────────────\n"
            f"│  Nozzle       {self.nozzle_temp_min}°C → {self.nozzle_temp_max}°C{rec_note('nozzleTempMin','nozzleTempMax')}\n"
            f"│  Bed          {self.bed_temp_min}°C → {self.bed_temp_max}°C{rec_note('bedTempMin','bedTempMax')}\n"
            f"│  Drying       {self.dry_temp}°C / {self.dry_time}h{rec_note('dryTemp','dryTime',' h')}\n"
            f"├─ Quantity ────────────────────────────────────────────\n"
            f"│  Unit         {ul}\n"
            f"│  Initial      {self.measure} {ul}\n"
            f"│  Available    {self.measure_available} {ul}" + (f"  ({stock}% remaining)\n" if stock is not None else "\n") +
            f"├─ Traceability ────────────────────────────────────────\n"
            f"│  Manufactured {self.manufacturing_date.strftime('%Y-%m-%d %H:%M UTC')}\n"
            f"│  Twin tag ID  {self.timestamp}\n"
            f"│  Message      {self.custom_message!r}\n"
            f"├─ Signature ───────────────────────────────────────────\n"
            f"│  ECDSA        {sig}\n"
            f"└───────────────────────────────────────────────────────"
        )


# ══════════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(
        description="TigerTag NTAG213 standalone SDK — parse, verify, export",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  python parse_tigertag.py dump.bin              # parse + auto-sync DB\n"
            "  python parse_tigertag.py dump.bin --json       # output as JSON\n"
            "  python parse_tigertag.py dump.bin --raw        # raw IDs, no DB lookup\n"
            "  python parse_tigertag.py --sync-only           # update databases only\n"
            "\n"
            "dump formats:\n"
            "  180 bytes  full chip dump (pages 0-44): UID extracted, signature verifiable\n"
            "  144 bytes  user data + signature (pages 0x04-0x27)\n"
            "   80 bytes  user data only (pages 0x04-0x17)\n"
            "\n"
            "spec: https://github.com/TigerTag-Project/TigerTag-RFID-Guide"
        ),
    )
    ap.add_argument("dump",       nargs="?",    help="Binary .bin file to parse")
    ap.add_argument("--db",       metavar="PATH", default=None,
                    help="Database folder (default: ./database next to this script)")
    ap.add_argument("--json",     action="store_true", help="Output as JSON")
    ap.add_argument("--raw",      action="store_true", help="Print raw dataclass, no DB lookup")
    ap.add_argument("--no-sync",  action="store_true", help="Do not auto-download databases")
    ap.add_argument("--sync-only",action="store_true", help="Update databases and exit")
    args = ap.parse_args()

    db_path = Path(args.db) if args.db else Path(__file__).parent / "database"

    # Sync-only mode
    if args.sync_only:
        if not _REQUESTS_AVAILABLE:
            print("❌  'requests' is not installed. Run:  pip install requests", file=sys.stderr)
            sys.exit(1)
        updated = sync_databases(db_path, verbose=True)
        if updated:
            print(f"\nUpdated {len(updated)} file(s): {', '.join(updated)}")
        else:
            print("\nAll databases already up to date.")
        sys.exit(0)

    if not args.dump:
        ap.print_help()
        sys.exit(0)

    # Parse
    with open(args.dump, "rb") as f:
        raw_data = f.read()

    tag = TigerTag.from_dump(raw_data)

    # Warnings
    warnings = tag.validate()
    if warnings:
        for w in warnings:
            print(f"⚠  {w}")
        print()

    # Raw mode (no DB)
    if args.raw:
        import pprint
        pprint.pprint(tag)
        sys.exit(0)

    # Load DB (auto-sync unless --no-sync)
    db = TigerTagDB(db_path, auto_sync=not args.no_sync)

    # Signature verification (fully autonomous)
    sig_result = tag.verify(db) if tag.is_signed else SignatureResult(SignatureResult.UNSIGNED)

    # Output
    if args.json:
        d = tag.to_dict(db)
        d["signature"] = sig_result.to_dict()
        print(json.dumps(d, indent=2, default=str))
    else:
        print(tag.pretty(db, sig_result))