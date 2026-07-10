# Trademark Policy — TigerTag & TigerTag+

## TL;DR

- ✅ You can **implement the TigerTag protocol** in any product, open source or proprietary, for free, forever. See [`LICENSING.md`](LICENSING.md).
- ✅ You can **build and sell commercial products** that read or write TigerTag chips.
- ✅ You can say your product is **"compatible with TigerTag"**.
- ✅ You can **display the TigerTag logo** to indicate compatibility, unmodified.
- ❌ You cannot **name your product or protocol "TigerTag"**.
- ❌ You cannot **issue TigerTag+ signatures** — we hold the private key.
- ❌ You cannot imply **certification, affiliation, or endorsement** without written authorization.

---

## The licences and the trademark are separate

The licences in [`LICENSING.md`](LICENSING.md) govern the **specification, the reference
database, and the sample code** — they let you read, quote, translate, implement, copy,
and ship, including commercially, with no royalties and no permission.

The trademark governs the **names and the brand** — it ensures that a product called
"TigerTag", or bearing the TigerTag logo as a mark of authenticity, comes from or is
authorized by TigerTag Corp.

You can have full rights to the protocol and still be bound by trademark rules on the
name. This is standard practice in open standards and open source (Arduino, OpenWrt,
Prusa Research, GS1, Bluetooth SIG).

> **Note:** an earlier version of this file stated that the protocol was available "under
> the MIT License". That was never accurate and has been removed. The authoritative
> statement of what is under what licence is [`LICENSING.md`](LICENSING.md).

---

## Protected trademarks

### "TigerTag"

**"TigerTag"** is a registered trademark of TigerTag Corp.

TigerTag refers to the **RFID material-identification protocol**, the **cloud service**
(`tigertag.io`), and the **official product catalogue**.

You **may** reference "TigerTag" in a factual, descriptive way
(e.g. *"compatible with TigerTag"*, *"reads TigerTag spools"*, *"implements the TigerTag
protocol v2.1"*) without permission.

You **may not** use "TigerTag" as the name of a competing RFID protocol, cloud service,
company, domain, or product brand without explicit written authorization.

### "TigerTag+"

**"TigerTag+"** is a trademark of TigerTag Corp and denotes a tag carrying a valid
ECDSA-P256 signature issued by TigerTag Corp.

Because TigerTag Corp holds the private key, a tag can only be *validly* signed by
TigerTag Corp. You **may not** describe a tag as "TigerTag+" unless it carries such a
signature — doing so is both trademark misuse and a false statement about authenticity.

Verifying a TigerTag+ signature is free, offline, and unrestricted. The public keys are
published in [`database/id_version.json`](database/id_version.json) and are in the public
domain.

---

## Logo usage

You **may** use the TigerTag logo, unmodified, to indicate compatibility:

- inside your application's UI,
- in your documentation, README, or store listing,
- on packaging, to state that a spool carries a TigerTag chip.

Conditions:

- Your product name must be clearly distinct from "TigerTag".
- The logo must remain unmodified — no recolouring, stretching, or recomposition.
- You must not imply affiliation, certification, or endorsement without permission.
- You must respect the visual guidelines in [`brand/`](brand/).

The contents of `brand/` are **all rights reserved** and are not covered by the licences
in `LICENSING.md`. The permission above is a limited, revocable permission to use the logo
descriptively; it is not a copyright licence to the artwork.

---

## What you can do freely

| Action | Allowed? |
|---|---|
| Read, quote, and translate the specification | ✅ Yes (CC-BY-4.0) |
| Implement the protocol in a closed-source product | ✅ Yes (irrevocable grant) |
| Ship a commercial printer, slicer, or reader that speaks TigerTag | ✅ Yes |
| Copy the sample code into your firmware | ✅ Yes (Apache-2.0) |
| Embed `database/*.json` in your product | ✅ Yes (CC0, no attribution needed) |
| Verify a TigerTag+ signature offline | ✅ Yes |
| Say "compatible with TigerTag" | ✅ Yes |
| Display the unmodified TigerTag logo for compatibility | ✅ Yes |
| Propose a change to the protocol | ✅ Encouraged — see [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| Name your app or protocol "TigerTag" | ❌ No (trademark) |
| Name your company or domain "TigerTag" | ❌ No (trademark) |
| Create a competing RFID protocol called "TigerTag" | ❌ No (trademark) |
| Issue or forge a TigerTag+ signature | ❌ No (key custody) |
| Label your tag "TigerTag+" without a valid signature | ❌ No (trademark + misrepresentation) |
| Claim TigerTag certification without agreement | ❌ No — see [`LICENSE_COMMERCIAL.md`](LICENSE_COMMERCIAL.md) |

---

## Official integration

If you manufacture filament or resin and want **officially supplied TigerTag media**
(pre-printed carriers), **TigerTag+ signatures**, **product-ID allocation**, or
**certified partner status**, that is what [`LICENSE_COMMERCIAL.md`](LICENSE_COMMERCIAL.md)
covers.

None of it is required to implement the protocol.

---

## Questions

Open an issue, or reach us on [Discord](https://discord.gg/3Qv5TSqnJH).
For trademark authorization requests: [tigertag@tigertag.io](mailto:tigertag@tigertag.io).

© 2025–2026 TigerTag Corp.
