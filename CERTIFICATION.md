# TigerTag Certification

**Implementing the protocol is free and always will be. Certification is what lets you put our mark
on your product and tell a buyer it is genuine.**

This document describes the programme. It follows the model the Connectivity Standards Alliance uses
for Zigbee and Matter, and the reasoning is the same: a mark on a product is a promise to the buyer,
and a promise is only worth what verifies it.

---

## Two marks. Only one of them needs us.

| | **TigerTag Compatible** | **TigerTag Certified** |
|---|---|---|
| Who | Anything a third party builds and has not had verified | Anything a third party builds **and has had verified** — hardware or software alike: filament and resin manufacturers, inlay and carrier producers, machine makers, and equally readers, apps, slicers and tools |
| Says | *"This works with TigerTag."* | *"This has been verified by TigerTag."* |
| Audit | None | **Required** |
| Cost | Free | **Paid** |
| Approval | None. Self-declared | Written authorization |
| Logo | In your app, docs, store listing | **On the product, the chip and the packaging** |
| TigerTag+ signature issuance | — | TigerTag+ Certified scope only |
| Product-ID allocation | — | Yes |
| Public listing | — | Yes — in the certified registry |

**The line between the two columns is whether anyone checked — not what
the product is.** Certification is open to anything a third party builds,
software included: a reader, a slicer or a mobile app can be certified on
exactly the same terms as a spool, by passing the audit and meeting the
specification. That is the Zigbee model this programme is modelled on, and
it is the intent. Nothing is excluded from certification by category.

### Two scopes

| Scope | Covers |
|---|---|
| **TigerTag Certified** | The product has been audited against the specification and conforms. |
| **TigerTag+ Certified** | The above, plus verified handling of **signed** tags — issuing them for a manufacturer, or reading and verifying them correctly for a reader or an app. Signature issuance belongs to this scope. |

If you only read the specification and ship a reader, you need nothing from us. Say
*"compatible with TigerTag"*, show the logo in your interface, sell it commercially. See
[`TRADEMARK.md`](TRADEMARK.md). Compatible is self-declared, free, and requires no audit
and no permission — and it will stay that way. Certification is something you may choose to
seek, never something you are made to.

The rest of this page is about the second column.

---

## Why certification is audited, and why it is paid

A buyer who sees the TigerTag logo on a spool must be able to conclude, without checking anything,
that the chip is genuine, correctly written, and behaves as the specification promises. That
conclusion is the entire value of the mark — to them, and to every certified partner who paid to
earn it.

An unverified mark is worse than no mark. It misleads the buyer, and it devalues the partners who
did the work.

There is also a legal reason. A trademark owner who licenses a mark **without exercising quality
control over its licensees** risks losing the mark entirely. Auditing is not administrative overhead;
it is what keeps the trademark enforceable and therefore what keeps the protocol's promise alive.

Certification is a paid service because auditing costs real work: conformance testing, physical
sample verification, catalogue review, and ongoing surveillance. **The fee schedule is provided with
the partner agreement** ([`LICENSE_COMMERCIAL.md`](LICENSE_COMMERCIAL.md)).

---

## The process

### 1. Apply

Contact TigerTag Corp and sign the partner agreement. It covers the trademark licence, signature
issuance, product-ID allocation and certified partner status.

### 2. Conformance statement

Declare, in writing, exactly what you implement: which specification version, which fields you write,
which chip types you use, how the tag is applied to the product. This is your statement of intent,
and the audit is measured against it.

### 3. Audit

Physical samples are tested against the conformance suite. The audit verifies that:

1. **The chip is written correctly** — byte-exact against the specification, on every sample.
2. **The catalogue data is accurate** — what the product page says matches what the spool actually is,
   and you have a process to keep it correct after shipping.
3. **Signed tags carry valid signatures**, issued by TigerTag Corp — in the TigerTag+
   Certified scope. An unsigned TigerTag+ is conformant and is not a finding.
4. **The logo appears only where the chip actually is** — on the product, on the packaging, nowhere else.
5. **The tag survives the product** — placement, adhesion and readability through the spool's life,
   in the orientations a customer will actually load it.

### 4. Declaration of conformity

You sign it. It states that production units match the audited samples.

### 5. Issuance

On a pass, TigerTag Corp grants:

- the **trademark licence** — the right to apply the TigerTag logo and name to that product line;
- **TigerTag+ signature issuance** for your products, in the TigerTag+ Certified scope;
- **product-ID allocation** in the official catalogue;
- a **public listing in the certified registry**.

### 6. Surveillance

Certification is not a one-time event. TigerTag Corp samples the market periodically and re-audits on:

- a new specification version,
- a change to your writing process, tag supplier or chip type,
- a new product line under the same certification,
- a substantiated complaint.

### 7. Revocation

Certification can be withdrawn. When it is, TigerTag Corp **stops issuing signatures**, delists the
partner from the registry, and terminates the trademark licence.

That first consequence is the one that matters, and it is why the programme has teeth: the TigerTag+
signature is issued under a private key held by TigerTag Corp. It cannot be forged, and it cannot be
issued by anyone else. **Revocation is technically real, not merely contractual.**

---

## Rebranding a certified product

Filament and resin are widely white-labelled. If you sell, under your own brand, a product already
certified by its manufacturer, you do not repeat the full audit: the certification is transferred,
subject to a reduced fee and a listing of its own.

The audited facts do not change. The name on the box does.

---

## The certified registry

Every certified partner and product line is listed publicly. That registry is the **only authoritative
way a buyer can check whether a logo on a spool is legitimate**, and the only way a partner can prove
they earned it.

It plays the role the Distributed Compliance Ledger plays for Matter, with the same purpose:
verification without trust.

---

## Independence

Today the audit is performed by TigerTag Corp. As the number of partners grows, TigerTag Corp intends
to authorize independent test laboratories, as the Connectivity Standards Alliance does. We say this
plainly rather than imply an independence we do not yet have.

---

## Questions

Certification, partner agreements and the fee schedule: **licensing@tigertag.io**

Nothing on this page is required to implement the protocol. See
[`LICENSING.md`](LICENSING.md) and [`TRADEMARK.md`](TRADEMARK.md).
