# TigerTag Official Integration Agreement

> ### Implementing the TigerTag protocol requires no licence and no payment.
>
> This agreement covers the **marks**, the **TigerTag+ signature service**, **official
> product-ID allocation**, **officially supplied TigerTag media**, and **certified partner
> status**. It does **not** license the protocol, and you do not need it to build a
> product that reads or writes TigerTag chips.
>
> If all you want to do is implement the specification — at any volume, in any product,
> open source or proprietary — read [`LICENSING.md`](LICENSING.md) and stop there.

This TigerTag & TigerTag+ Official Integration Agreement ("Agreement") governs the use of
the TigerTag marks, the issuance of TigerTag+ signatures, the allocation of official
product identifiers, the supply of official TigerTag media, and certified partner status.

> **Draft — pending legal review.** This document is a good-faith restatement of the
> commercial relationship. It has not yet been reviewed by counsel and is not a binding
> offer. Contact [tigertag@tigertag.io](mailto:tigertag@tigertag.io) for executable terms.

---

## 1. Definitions

- **Licensor:** TigerTag Corp
- **Licensee:** The individual or entity agreeing to the terms of this Agreement
- **Protocol:** The TigerTag RFID specification, reference database, and sample code, as
  published in the TigerTag-RFID-Guide repository and licensed under
  [`LICENSING.md`](LICENSING.md). **The Protocol is not licensed by this Agreement.**
- **Marks:** The "TigerTag" and "TigerTag+" names, the TigerTag logo, and the contents of
  `brand/`
- **TigerTag+ Signature:** An ECDSA-P256 signature over a tag payload, issued using a
  private key held solely by the Licensor
- **Official Product ID:** An identifier allocated by the Licensor within the official
  TigerTag product catalogue
- **Official Media:** Physical TigerTag carriers supplied by the Licensor — pre-printed
  with the TigerTag logo, comprising the RFID inlays and adhesive backing

---

## 2. What this Agreement grants

The Licensor grants the Licensee a **non-exclusive, non-transferable** right to:

- Use the **Marks** on commercial packaging, marketing, and product listings, subject to
  [`TRADEMARK.md`](TRADEMARK.md)
- Request **issuance of TigerTag+ Signatures** for the Licensee's products
- Receive **allocation of Official Product IDs** in the official TigerTag catalogue
- Purchase and deploy **Official Media**
- Represent itself as a **certified TigerTag partner**, where such status has been granted
- Use the Licensor's **product-management tooling** for mass-production data entry

## 2 bis. What this Agreement does *not* restrict

For the avoidance of doubt, and notwithstanding anything else in this Agreement, the
Licensee and any third party may, without this Agreement and without payment:

- Implement the Protocol in any product or software, open source or proprietary
- Manufacture, encode, and sell RFID tags conforming to the Protocol, at any volume
- Redistribute the Protocol, the specification, the reference database, and the sample
  code, in source form, under the licences stated in [`LICENSING.md`](LICENSING.md)
- Read, write, and verify TigerTag chips

Such products may not, however, bear the Marks, claim TigerTag+ status, or use Official
Product IDs, except under this Agreement.

---

## 3. When this Agreement applies

This Agreement applies when the Licensee wishes to:

- Display the TigerTag or TigerTag+ Marks on products offered for sale or mass
  distribution
- Ship products carrying valid TigerTag+ Signatures
- Ship products carrying Official Product IDs resolvable in the official catalogue
- Purchase Official Media from the Licensor
- Claim certified partner status

It does **not** apply merely because the Protocol is used in a commercial, production, or
OEM context.

---

## 4. Conformance

Where the Licensee applies the Marks to a product, the Licensee shall encode data in
strict conformance with the published TigerTag specification, and shall not label as
"TigerTag-compatible" any product that departs from it in a way that compromises
interoperability.

This is a condition of using the Marks. It is not a restriction on the Protocol: anyone
remains free to modify, extend, or diverge from the specification in their own work,
provided they do not call the result TigerTag.

Proposals to change the specification are welcomed through the TEP process described in
[`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## 5. Trademark and logo usage

- The TigerTag name and logo are trademarks of TigerTag Corp.
- Logo use is allowed in compatibility disclosures (e.g. "Compatible with TigerTag")
  by anyone, under [`TRADEMARK.md`](TRADEMARK.md), without this Agreement.
- Do not use the logo in a misleading or brand-confusing manner.
- Modifying the logo is strictly prohibited.
- The use of the TigerTag name or logo in company, domain, or product names is prohibited
  without written approval.

---

## 6. Official Media, services, and fees

The Protocol is free at any volume. Fees under this Agreement attach only to the goods and
services the Licensor actually supplies:

- **Official Media** — supplied at low cost. Each carrier is delivered ready to apply,
  with the TigerTag logo already printed, the RFID inlays, and 3M adhesive backing. The
  Licensor acts as a central purchasing party, aggregating demand across the ecosystem so
  that individual manufacturers do not have to source, print, and assemble media
  themselves. The Licensee burns its own data at its own factory.
- **TigerTag+ Signature issuance** — per-product or per-batch, as agreed.
- **Official Product-ID allocation** — per catalogue entry, as agreed.
- **Certified partner status and support** — as agreed.

Revenue from these services funds the maintenance of the Protocol, the reference database,
the public API, and the official tools, all of which remain free.

Commercial terms, volumes, and pricing are agreed between the parties in a separate
schedule.

> **Superseded term.** A previous revision of this file granted the licence "royalty-free
> for low-volume OEM use (less than 10,000 units/year)", with negotiated fees above that
> threshold, applied to *units of product embedding TigerTag*. That threshold is
> incompatible with the irrevocable, royalty-free implementation grant in
> [`LICENSING.md`](LICENSING.md) and has been removed. Any volume tiering now belongs in
> the pricing schedule for Official Media, signatures, and product-ID allocation — not in
> a right to implement.

---

## 7. Support and updates

TigerTag is provided "as-is". No guarantees are made regarding support, updates, or bug
fixes. Optional support contracts may be offered separately.

---

## 8. Feedback

Licensee is encouraged to report bugs, compatibility issues, or improvement suggestions to
the Licensor. Feedback is voluntary but appreciated to help improve the TigerTag ecosystem.
Protocol change proposals should follow [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## 9. Termination

This Agreement may be terminated by the Licensor if:

- The Licensee breaches any clause of this Agreement
- The Licensee misuses the TigerTag brand, or applies the Marks to a product that does not
  conform to the specification
- The Licensee enters insolvency or ceases operation

**Termination of this Agreement does not withdraw the Licensee's right to implement the
Protocol.** That right is granted irrevocably in [`LICENSING.md`](LICENSING.md) to
everyone, and survives termination. What terminates is the right to use the Marks, to
receive TigerTag+ Signatures, to receive Official Product-ID allocations, to purchase
Official Media, and to claim certified partner status.

---

## 10. Liability

TigerTag is provided without warranty of any kind. The Licensor is not liable for any
damages or losses resulting from the use of TigerTag in commercial applications.

---

## 11. Governing law

This Agreement is governed by the laws of France. Any disputes shall be resolved in the
courts of Toulouse, France.

---

For inquiries, support, or licensing at scale, contact:
[tigertag@tigertag.io](mailto:tigertag@tigertag.io)

© 2025–2026 TigerTag Corp.
