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
| `last_update.json` | Sync timestamps |
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
server timestamp to compare and every run downloads it in full (~3 400 products,
four pages, ~1.5 MB). That is why the byte-comparison above matters: the download
is unconditional, the *write* is not. The `products` key in `last_update.json` is
ours rather than the API's — it carries the catalogue's own newest `updated_at`,
so it means the same thing as its neighbours.

## A note on the public keys

`id_version.json` contains **public** keys only, in PEM form, one per signed tag format
version. They are meant to be embedded in readers so that TigerTag+ verification works with
no network access.

The corresponding private key is held solely by TigerTag Corp. If you ever find a private
key in this repository, treat it as a critical vulnerability and report it privately —
see [`../SECURITY.md`](../SECURITY.md).
