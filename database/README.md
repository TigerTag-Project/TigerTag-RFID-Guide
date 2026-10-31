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

We would still enjoy a credit and a link to <https://tigersystem.io>. You do not owe us one.

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
| `id_catalog.json` | **The full TigerTag+ product catalogue** — named like its `id_*.json` neighbours because that is what it is: the ids — every referenced product with its brand, series, name, material, aspect, colour, SKU, barcode, capacity and image |
| `last_update.json` | Sync timestamps, as served by the API's `all/last_update` |
| `manifest.json` | Every table above with its sha256, size, entry count and last change date. See [The manifest](#the-manifest) |
| `db_update.py` | Sync tooling for everything above — tables and catalogue (Apache-2.0) |

### The product catalogue

The tables above name the *vocabulary* — what a material or a brand id means.
`id_catalog.json` is the **catalogue itself**: ~3 000 real products, each with the
`id` a chip carries in `id_product`. Resolving a scanned chip to an actual
product needs nothing more than this file.

It is mirrored here so an integration can ship the catalogue with it — no API
call, no key, no pagination, no rebuilding anything, and it works offline. Same
deal as the reference tables.

```jsonc
{
  "id": 1251796608,            // matches the chip's id_product
  "product_type": "Filament",
  "brand": "3DXTech",
  "series": "CarbonX",
  "name": "Black",
  "title": "CarbonX - Black",  // series + name, pre-joined
  "material": "PP",
  "aspect1": "Carbon",
  "aspect2": null,
  "color": "#000000FF",
  "color_info": { "type": "mono", "colors": ["#000000FF"] },
  "measure": "750 g",
  "sku": "PP01010750BK0",
  "barcode": "07050135",
  "img_src": "https://cdn.tigertag.io/img?id=1251796608&v=4",
  "updated_at": 1785083620855
}
```

Read `series` and `name` from their own fields — do **not** split `title` on the
last `" - "`. A colour name may contain one: *"PLA Basic - CMYK - Magenta"* is
series `PLA Basic` + name `CMYK - Magenta`, and splitting gets it backwards.

`sku`, `barcode` and `updated_at` are **not** filled in for every product; treat
them as optional. `id`, `product_type`, `brand`, `series`, `name`, `material`,
`aspect1`, `color`, `color_info` and `measure` are always present.

Refreshed by `python db_update.py`, in the same run as the tables above — there
is no separate catalogue command. It walks every page, sorts by `id` and sorts
each product's keys, so an unchanged catalogue yields a byte-identical file and
no commit. `--check` writes nothing and exits non-zero when any file has fallen
behind — handy in CI.

Unlike the tables, the catalogue has no key in `all/last_update`, so there is no
server timestamp to compare and every run downloads it in full (19 205 products,
four pages, ~17 MB in October 2026). That is why the byte-comparison above matters:
the download is unconditional, the *write* is not. `last_update.json` stays the
API's own payload; the script would only add a `products` key from the products'
`updated_at`, which the API does not return today. The catalogue's change date is
therefore in `manifest.json`.

### The manifest

`manifest.json` is written by `db_update.py` at the end of every run, after the
tables, with the same atomic write. It lets a client check for updates and verify
every download from any source, without the GitHub API:

```json
{
  "format": 1,
  "generatedAt": "2026-10-31T16:44:10Z",
  "files": {
    "id_catalog.json": {
      "sha256": "1a37a1b90766c96dd1bb299a269daa7ec7454a27f112e3b4143e37cede95c39d",
      "bytes": 17268794,
      "entries": 19205,
      "updatedAt": "2026-10-31T16:44:10Z"
    }
  }
}
```

- `files` lists every JSON file of this folder except the manifest itself.
- `sha256` (hex) and `bytes` describe the exact bytes of the file as published.
- `entries` is the length of the top-level array, or `null` for an object
  (`last_update.json`).
- `updatedAt` is the last time this file's content changed; unchanged files keep
  their date.
- `generatedAt` is the last time any file changed. A run that changes nothing
  leaves the manifest byte-identical, so it causes no commit.

A client fetches `manifest.json` from the first source that answers, downloads only
the files whose `sha256` differs from its own copy, checks `bytes`, `sha256` and
`entries`, and replaces its tables in one step, keeping the current ones on any
error. Since every file is checked against the manifest, a mirror needs no more
trust than GitHub: a stale or altered file is refused.

`python db_update.py --manifest` rebuilds the manifest from the files on disk
without touching the network (`--manifest --check` only reports).

## A note on the public keys

`id_version.json` contains **public** keys only, in PEM form, one per signed tag format
version. They are meant to be embedded in readers so that TigerTag+ verification works with
no network access.

The corresponding private key is held solely by TigerTag Corp. If you ever find a private
key in this repository, treat it as a critical vulnerability and report it privately —
see [`../SECURITY.md`](../SECURITY.md).
