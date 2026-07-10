# Licensing

This repository contains four different kinds of material, and they are not all
under the same licence. This page says exactly what is under what.

If you only read one paragraph, read the next one.

---

## Implementation grant

> TigerTag Corp grants an irrevocable, worldwide, royalty-free right to implement
> this specification in any product or software, open source or proprietary,
> without restriction and without further permission.

You do not need a licence to read this specification. You do not need a licence to
implement it. You do not need to tell us, register with us, or pay us. This applies
to commercial products, closed-source firmware, printers, slicers, and anything else.

This grant is irrevocable. It does not expire, and it is not conditional on your
staying in anyone's good graces.

---

## What is under what

| Path | Licence | SPDX identifier |
|---|---|---|
| `README.md` and all protocol documentation | Creative Commons Attribution 4.0 International | `CC-BY-4.0` |
| `Images/`, `assets/` — diagrams and figures | Creative Commons Attribution 4.0 International | `CC-BY-4.0` |
| `database/*.json` — the reference registry | Creative Commons Zero 1.0 Universal (public domain) | `CC0-1.0` |
| `Sample code/`, `SpoolmanDB/`, `database/db_update.py` — all source code | Apache License 2.0 | `Apache-2.0` |
| `brand/` — logo, banner, icons, wordmarks | **All rights reserved.** Not covered by any licence above | — |

The repository's root `LICENSE` file contains the full text of CC-BY-4.0, because the
specification is the primary content here. Full texts of every licence used are in
[`LICENSES/`](LICENSES/).

---

## What this means in practice

**You want to build a reader, a writer, a printer, or a slicer that speaks TigerTag.**
Go ahead. Nothing here stops you. The specification is CC-BY-4.0, so quote it and
translate it freely with attribution; the implementation grant above covers the act of
implementing it, which copyright would not have restricted anyway.

**You want to copy the sample code into your firmware.**
It is Apache-2.0. Keep the notice, keep the licence text, state your changes. Apache-2.0
includes an express patent grant from every contributor — that is deliberate, and it is
why we chose Apache-2.0 over MIT for code.

**You want to embed `database/*.json` in your product.**
It is CC0-1.0 — public domain. No attribution required, no notice required, nothing to
carry into your binary. In the European Union the *sui generis* database right can attach
to a compiled dataset independently of copyright, so CC0 is used here to waive that too,
explicitly. We would still enjoy a credit. You do not owe us one.

**You want to translate the specification, quote it in a book, or teach from it.**
CC-BY-4.0. Attribute TigerTag Corp and you are done.

**You want to call your product "TigerTag" or put our logo on your box.**
That is the one thing that is not free, and it is a trademark matter, not a licensing
one. See [`TRADEMARK.md`](TRADEMARK.md).

---

## What is *not* granted here

Three things sit outside every licence on this page:

1. **The TigerTag™ and TigerTag+™ marks and the logo.** All rights reserved.
   See [`TRADEMARK.md`](TRADEMARK.md). Note that CC-BY-4.0 §2(b)(2) expressly
   does not license trademark rights, and neither do we.

2. **The TigerTag+ signature.** TigerTag Corp holds the ECDSA-P256 private key. Anyone
   may *verify* a signature offline — the public keys are published in
   [`database/id_version.json`](database/id_version.json) and are CC0. Nobody but
   TigerTag Corp can *issue* one. That is a property of key custody, not of a licence,
   and it is what makes a validly signed tag provably originate from TigerTag.

3. **Product-ID allocation in the official catalogue.** Like a GS1 company prefix, an
   official product ID is *allocated*, not licensed. The protocol is free; the identity
   space is administered.

Points 1–3 are what [`LICENSE_COMMERCIAL.md`](LICENSE_COMMERCIAL.md) covers, together
with the supply of official pre-printed TigerTag media. None of them restrict the
protocol.

---

## Why not GPL

Earlier revisions of this repository announced GPLv3. That was a mistake, and it has been
corrected.

Copyleft on a *specification* frightens the manufacturers a standard needs — a filament
brand's counsel reading "any derivative work must also be GPLv3" next to a document
describing a memory layout will, correctly, escalate. A specification intended to become
the EAN barcode of 3D printing must be permissive, and its reference code must carry a
patent grant. Nothing was gained by the GPL and a great deal was at risk.

The GPLv3 announcement was also never operative: the old `LICENSE.md` contained a
placeholder where the licence text should have been, so GitHub reported the repository as
`NOASSERTION` — "all rights reserved." For a period, nobody could lawfully implement this
protocol at all. That is now fixed.

---

## Why forking the specification is pointless

Nothing in these licences stops you from forking this repository. We are not going to try.

But a specification is not a program. Its entire value is that everyone agrees on it. A
fork of the TigerTag protocol produces a document that describes chips nobody makes, that
no reader in the field implements, and that cannot be called TigerTag. It fragments the
ecosystem and helps no one, least of all whoever wrote it.

If the specification is wrong, or incomplete, or missing a field you need, the useful move
is a proposal, not a fork. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the TEP
(TigerTag Enhancement Proposal) process, and [`VERSIONING.md`](VERSIONING.md) for how
accepted changes reach a released version of the spec.

---

## SPDX

Source files carry `SPDX-License-Identifier` headers. For the repository as a whole:

```
SPDX-License-Identifier: CC-BY-4.0 AND CC0-1.0 AND Apache-2.0
```

---

## Contact

Licensing questions: [tigertag@tigertag.io](mailto:tigertag@tigertag.io)

© 2025–2026 TigerTag Corp.
