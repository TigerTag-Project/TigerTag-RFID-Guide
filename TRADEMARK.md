# Trademark Policy — TigerTag & TigerTag+

## TL;DR

- ✅ You can **implement the TigerTag protocol** in any product, open source or proprietary, for free, forever. See [`LICENSING.md`](LICENSING.md).
- ✅ You can **build and sell commercial products** that read or write TigerTag chips.
- ✅ You can say your product is **"compatible with TigerTag"**.
- ✅ You can **display the TigerTag logo to indicate compatibility**, unmodified — in your app, your
  docs, your store listing.
- ❌ You cannot put the TigerTag logo **on a chip, a spool, or its packaging** without written
  authorization. There, the logo is a mark of **authenticity**, not of compatibility.
- ❌ You cannot **name your product or protocol "TigerTag"**, or use the name commercially as a brand.
- ❌ You cannot **issue TigerTag+ signatures** — we hold the private key.
- ❌ You cannot imply **certification, affiliation, or endorsement** without written authorization.
- 🔍 **Certification is an audit, and it is a paid service** — see [`CERTIFICATION.md`](CERTIFICATION.md).

> Say what your product *does* as loudly as you like. Only we say what a TigerTag *is*.

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

**"TigerTag"** is a trademark of TigerTag Corp.

> **Registration status.** TigerTag is claimed as an unregistered ("common law") mark and is
> written **TigerTag™**, never TigerTag®. No application has been filed at INPI, EUIPO or the
> USPTO yet; filing is planned (see `docs/TRADEMARK-FILING.md`). Do not write "registered"
> or use the ® symbol anywhere until a registration certificate actually exists — claiming a
> registration you do not hold is an offence in several jurisdictions, France included, and
> this document is the one a partner reads before signing.

TigerTag refers to the **RFID material-identification protocol**, the **cloud service**
(`tigersystem.io`), and the **official product catalogue**.

You **may** reference "TigerTag" in a factual, descriptive way
(e.g. *"compatible with TigerTag"*, *"reads TigerTag spools"*, *"implements the TigerTag
protocol v2.1"*) without permission.

You **may not** use "TigerTag" as the name of a competing RFID protocol, cloud service,
company, domain, or product brand without explicit written authorization.

### "TigerTag+"

**"TigerTag+"** is a trademark of TigerTag Corp and denotes a tag whose identity carries
a **product ID from the official catalogue**, together with optional enrichment metadata
held cloud-side.

**The `+` means *identified*, not *certified*.** It says the tag is a known catalogue
product, not that anyone has vouched for its origin. A TigerTag+ read in airplane mode
behaves like any other TigerTag: everything needed to print is on the chip, and the
enrichment is an extra, never a dependency. A TigerTag+ carrying no signature is entirely
legitimate.

A TigerTag+ that **additionally** carries a valid ECDSA-P256 signature is a
**"TigerTag+ Certified"**. That signature is written by a manufacturer holding TigerTag+
certification, which is what the signing tools come with. **TigerTag Corp holds the private
key**, so no one else can issue a valid signature — which is the whole reason verification
means anything.

You **may not** describe a tag as "TigerTag+ Certified" unless it carries such a signature:
that would be both trademark misuse and a false statement about authenticity. Describing an
unsigned catalogue tag as "TigerTag+" is correct and always has been intended to be.

Verifying a signature is free, offline, and unrestricted. The public keys are published in
[`database/id_version.json`](database/id_version.json) and are in the public domain.

The canonical definition of the tier lives on the wiki:
<https://wiki.tigersystem.io/products/tigertag-plus/>. The binary layout of the signature
it depends on is specified [here](README.md#3-verify-signature-ecdsa-p256-fully-offline).

---

## Logo usage

There are **two different uses of the logo**, and only one of them is free.

The distinction is the same one Zigbee draws between *"Zigbee Compatible"* and
*"Zigbee Certified"*: saying your product **talks to** TigerTag is a factual statement about
your product. Putting our mark **on** a chip, a spool, or its packaging is a statement about
**origin and authenticity** — and a buyer reads it as a guarantee.

### 1. Referential use — free, no permission needed

You **may** use the TigerTag logo, unmodified, to indicate **compatibility**:

- inside your application's UI,
- in your documentation, README, or store listing,
- in marketing that describes what your product works with.

Conditions:

- Your product name must be clearly distinct from "TigerTag".
- The logo must remain unmodified — no recolouring, stretching, or recomposition.
- It must appear as a compatibility statement, never as a seal or a badge of quality.
- You must not imply affiliation, certification, or endorsement.
- You must respect the visual guidelines in [`brand/`](brand/).

### 2. Product use — written authorization required

You **may not**, without a written trademark licence from TigerTag Corp:

- print, emboss, engrave or otherwise apply the TigerTag logo **on an RFID chip, an inlay,
  a carrier, a label, a spool, a resin bottle, or its packaging**;
- use the TigerTag name **commercially as a brand or product designation**;
- present the logo as a **mark of authenticity, certification, quality, or partnership**.

Applied to a product, the mark no longer says *"this works with TigerTag"*. It says
**"this *is* a TigerTag"** — an assertion about who made it and whether it can be trusted.
That assertion is ours to make, and only ours.

Authorization is granted through **certification**: an audit of your product and your process,
followed by a trademark licence. It is a paid service. See [`CERTIFICATION.md`](CERTIFICATION.md).

### Why this line exists

Trademark law exists to **protect the buyer**, not the brand: it prevents confusion about who
made a product and whether it meets the standard it claims. A consumer who sees our logo on a
spool must be able to conclude, without checking anything, that the chip is genuine, correctly
written, and will behave as the specification promises.

That guarantee is only worth something if we verify the integrations behind it. So certification
is not paperwork — it is what makes the promise true. It is also a legal necessity: a trademark
owner who licenses a mark without exercising quality control over licensees risks losing the mark
altogether.

**The protocol stays free. The promise stays ours to keep.**

### Artwork

The contents of `brand/` are **all rights reserved** and are not covered by the licences
in `LICENSING.md`. The referential permission above is a limited, revocable permission to use
the logo descriptively; it is not a copyright licence to the artwork.

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
| Say "compatible with TigerTag", including on a commercial product | ✅ Yes |
| Display the unmodified logo **in your app, docs or store listing** to show compatibility | ✅ Yes |
| Propose a change to the protocol | ✅ Encouraged — see [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| Put the TigerTag logo **on a chip, inlay, label, spool, bottle or packaging** | ❌ No — written authorization + certification |
| Use the TigerTag name **commercially as a brand or product designation** | ❌ No (trademark) |
| Present the logo as a **seal of authenticity, quality or partnership** | ❌ No — written authorization + certification |
| Name your app or protocol "TigerTag" | ❌ No (trademark) |
| Name your company or domain "TigerTag" | ❌ No (trademark) |
| Create a competing RFID protocol called "TigerTag" | ❌ No (trademark) |
| Issue or forge a TigerTag+ signature | ❌ No (key custody) |
| Label your tag "TigerTag+" — a catalogue product id, no signature needed | ✅ Yes |
| Label your tag "TigerTag+ **Certified**" without a valid signature | ❌ No (trademark + misrepresentation) |
| Claim TigerTag certification without agreement | ❌ No — see [`LICENSE_COMMERCIAL.md`](LICENSE_COMMERCIAL.md) |

---

## Official integration

Three words, and only one of them needs us:

- **Official** — made by TigerSystem. A statement of origin, not a mark that gets granted.
- **Certified** — made by a third party, audited and validated by TigerSystem. Open to
  anything a third party builds, hardware or software alike: the line is whether anyone
  checked, not what the product is.
- **Compatible** — made by a third party, self-declared. Free, unaudited, no permission
  needed, and staying that way.

Certification comes in two scopes, **TigerTag Certified** and **TigerTag+ Certified**, the
second covering verified handling of signed tags. Who may claim what, what the audit
verifies, and what each mark costs are defined in
[`CERTIFICATION.md`](CERTIFICATION.md) — that is where those facts live, and they are not
restated here.

If you manufacture filament or resin and want **officially supplied TigerTag media**
(pre-printed carriers), **TigerTag+ signatures**, **product-ID allocation**, the right to put
**the TigerTag logo on your product or packaging**, or **certified partner status**, you need
certification.

Certification is an **audit** — of your product and of your process — followed by a trademark
licence. It is a paid service, on the model the Connectivity Standards Alliance uses for Zigbee
and Matter. The process, what the audit verifies, surveillance and revocation are all described
in [`CERTIFICATION.md`](CERTIFICATION.md). The agreement itself is
[`LICENSE_COMMERCIAL.md`](LICENSE_COMMERCIAL.md).

Certified partners are listed publicly. That registry is the only authoritative way for a buyer
to check whether a logo on a spool is legitimate.

**None of it is required to implement the protocol.** Implement it freely, sell freely, say
"compatible with TigerTag" freely. Certification is required only to make the *promise* —
to put our mark on your product and tell a buyer it is genuine.

---

## Questions

Open an issue, or reach us on [Discord](https://discord.gg/3Qv5TSqnJH).
For trademark authorization requests: [tigertag@tigertag.io](mailto:tigertag@tigertag.io).

© 2025–2026 TigerTag Corp.
