# TigerTag reference database

This directory contains the reference registry for the TigerTag protocol: the canonical
identifiers for materials, brands, aspects, types, diameters, measurement units, and tag
format versions, plus the public keys used to verify TigerTag+ signatures offline.

## Licence

**The contents of `database/*.json` are released into the public domain under
[CC0 1.0 Universal](../LICENSES/CC0-1.0.txt) (`SPDX-License-Identifier: CC0-1.0`).**

No attribution is required. No notice needs to be carried into your binary. Embed these
files directly in a slicer, a printer firmware, a reader, or a mobile app, commercial or
otherwise, without asking and without crediting anyone.

CC0 is used deliberately rather than CC-BY. In the European Union, a compiled dataset can
attract the *sui generis* database right independently of copyright, which would otherwise
require an explicit grant before anyone could lawfully extract and re-use a substantial part
of it. CC0 waives that right along with copyright. Maximum adoption is the goal; a registry
that manufacturers hesitate to embed is a registry that fails.

We would still enjoy a credit and a link to <https://tigertag.io>. You do not owe us one.

`database/db_update.py` is **source code**, not data, and is licensed under
[Apache-2.0](../LICENSES/Apache-2.0.txt). See [`../LICENSING.md`](../LICENSING.md).

## These files are generated — do not edit them

`database/*.json` is generated from the TigerTag catalogue and synchronised into this
repository automatically by [`.github/workflows/sync-database.yml`](../.github/workflows/sync-database.yml).

**Pull requests adding or modifying entries will be reverted on the next sync.** To have a
brand, material, aspect, or type added, open an issue or contact
[tigertag@tigertag.io](mailto:tigertag@tigertag.io).

Fixes to `db_update.py` and the sync tooling are welcome as pull requests.

## Live API

The same data is available, always current, with no key and no login:

<https://api.tigertag.io/api:tigertag>

## Files

| File | Contents |
|---|---|
| `id_version.json` | Tag format versions and their ECDSA-P256 **public keys**. See [`../VERSIONING.md`](../VERSIONING.md) |
| `id_material.json` | Material identifiers (PLA, PETG, ABS, resin, …) |
| `id_brand.json` | Brand identifiers |
| `id_aspect.json` | Surface aspect / finish identifiers |
| `id_type.json` | Product type identifiers |
| `id_diameter.json` | Filament diameter identifiers |
| `id_measure_unit.json` | Measurement unit identifiers |
| `last_update.json` | Sync timestamp |
| `db_update.py` | Sync tooling (Apache-2.0) |

## A note on the public keys

`id_version.json` contains **public** keys only, in PEM form, one per signed tag format
version. They are meant to be embedded in readers so that TigerTag+ verification works with
no network access.

The corresponding private key is held solely by TigerTag Corp. If you ever find a private
key in this repository, treat it as a critical vulnerability and report it privately —
see [`../SECURITY.md`](../SECURITY.md).
