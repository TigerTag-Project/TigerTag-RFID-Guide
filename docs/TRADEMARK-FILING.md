# Trademark filing — preparation dossier

> **Not legal advice.** This gathers, in one place, everything a filing needs so the work with an
> attorney (or a direct INPI filing) starts from decisions already made rather than from a blank
> page. Every point marked **DECIDE** needs a human answer; every point marked **ASK COUNSEL** is a
> legal judgement that should not be made from this file.
>
> Status: **nothing is filed anywhere** (INPI, EUIPO, USPTO) as of 2026-07-19.

---

## 1. Why this blocks the business, not just the paperwork

The protocol is open on purpose, so the licence is not what stops a manufacturer using TigerTag —
and it is not meant to be. What stops them printing **"TigerTag Certified"** on a box without having
certified anything is that the *name* is a registered mark and can be enforced. This is exactly the
Zigbee / Matter model: open specification, protected logo.

**So the certification programme has no teeth until the mark is registered.** It can be documented
and operated, but not enforced against someone who ignores it. This is the single external
dependency the commercial plan rests on.

---

## 2. Applicant — DECIDE FIRST, everything else follows

The documents in this repo are written in the name of **"TigerTag Corp"** (33 mentions across 7
files). The real legal entity behind the project is **3D FRANCE**. These cannot both be right.

| | 3D FRANCE | "TigerTag Corp" |
|---|---|---|
| Exists as a registered entity | **Yes** — SIREN 820444305, est. 2016 | **Unverified — likely not** |
| Used for the Azure code-signing identity | Yes | No |
| Named in the certification/trademark docs | No | Yes, everywhere |

**Risk:** an agreement signed by an entity that does not exist may be unenforceable — and the
counterparty, not you, is the one who benefits from that. **ASK COUNSEL** whether to file in the
name of 3D FRANCE now, or to incorporate the naming entity first and file in its name. Filing in one
name and later assigning is possible but costs an extra step and a recordal fee.

**Applicant details (3D FRANCE), ready to paste:**

```
Name:      3D FRANCE
SIREN:     820444305
Address:   12G rue de l'Europe, 31150 LESPINASSE, Haute-Garonne, France
Contact:   benoit@tigertag.io  /  tigertag@tigertag.io
Domains:   tigertag.io, tigersystem.io
Applicant: Benoit Michaut
```

Once decided, the same string must be corrected across the 7 files that say "TigerTag Corp"
(`TRADEMARK.md`, `CERTIFICATION.md`, `LICENSING.md`, `LICENSE_COMMERCIAL.md`, `README.md`,
`SECURITY.md`, `CONTRIBUTING.md`) and in the `©` line.

---

## 3. What to file, in priority order

Budget is finite, so file in the order of what actually protects revenue. Marks lower down can wait.

| # | Mark | Why | Priority |
|---|---|---|---|
| 1 | **TigerTag** | The protocol, the chips sold to manufacturers, the whole brand | **Essential** |
| 2 | **TigerTag Certified** | The enforcement lever of the certification programme — without it the label is unprotectable | **Essential** |
| 3 | **TigerTag+** | The paid, signed tier | High |
| 4 | **TigerSystem** | Umbrella name for the ecosystem | Medium |
| 5 | **TigerScale**, **TigerPOD** | Open hardware, given away — brand value is low and both have known collisions | Low |
| — | **TigerData** | Display name for chipless entries; internal vocabulary, not a product sold | Probably skip |
| — | **TigerTag Compatible** | Free, self-declared tier — protecting it matters less than protecting "Certified" | Optional |

**ASK COUNSEL:** a word mark, a figurative (logo) mark, or both? A word mark is broader and usually
filed first; the logo can follow.

---

## 4. Classes (Nice classification)

**ASK COUNSEL to confirm the exact wording** — these are the classes the activity falls in, not
validated specifications.

| Class | Covers | Wording to discuss |
|---|---|---|
| **9** | The chips and the software — **the core class** | RFID and NFC tags and transponders; blank and encoded electronic chips; downloadable computer software for inventory management; recorded software |
| **42** | The cloud service and the technical side of certification | Software as a service (SaaS); design and development of computer software; technical consultancy; **quality control and authentication services** |
| **35** | Only if a certified-product directory / marketplace is operated | Compilation and management of a register of certified products; commercial information services |
| **45** | Only if trademark licensing is a formal activity | Licensing of intellectual property |

Classes 9 and 42 are the load-bearing pair. 35 and 45 are additions to weigh against their cost.

**Note on class 9 — this is where the collision risk sits.** See §6.

---

## 5. Certification mark, or ordinary mark under licence? — ASK COUNSEL

There are two distinct legal instruments, and the choice has a structural consequence:

- **An ordinary trademark**, licensed contractually to certified partners. Flexible; the control
  comes from the licence agreement.
- **A certification mark** (*marque de garantie ou de certification* in France since 2019, EU
  certification mark since 2017). Purpose-built for this, but it comes with **regulations of use**
  filed with the office — and, importantly, **the owner of an EU certification mark may not carry on
  a business involving the supply of goods or services of the kind certified.**

**That restriction may be decisive here**, because the plan is to sell chips *and* certify the
manufacturers who use them. If it applies, a formal certification mark could be incompatible with
the business model, pushing towards an ordinary mark licensed under contract — which is what
`CERTIFICATION.md` already describes. **This is the single most important question to put to
counsel**, because it shapes the documents as much as the filing.

---

## 6. Prior marks found — verify before filing

Public-web signals only, gathered during the 2026-07-19 review. **None of these is a legal
conclusion** — a proper availability search is the attorney's job, and it must come *before* filing,
not after a refusal.

| Prior mark | Field | Why it matters |
|---|---|---|
| **TigerTags** (tiger-tags.com) | Smart trackers / electronic tags | **Identical string, same class 9, adjacent field.** The most serious signal. Domain was not resolving, so possibly dormant — but dormant is not the same as abandoned |
| **TigerScale** (tigerscale.net) | Weighing scales, India | Directly collides with the TigerScale product, which is itself a scale |
| **TigerPOD** | iShot camera-tripod mark | Collides with the TigerPOD name |
| **Tiger Data** (ex-Timescale) | Database software | Raises the density of Tiger-family marks in tech |

**Practical consequence:** the availability search should be run **before** spending on filings, and
it may change the priority list in §3 — for instance dropping TigerScale and TigerPOD, or filing
them as figurative marks only.

---

## 7. Where to file, and roughly what it costs

Order matters: a first filing gives a **6-month priority window** in which later filings elsewhere
keep the first date.

| Office | Territory | Ballpark official fees | When |
|---|---|---|---|
| **INPI** (France) | France | ~190 € for one class, ~40 € per extra class | **First** — cheapest, home jurisdiction, establishes the date |
| **EUIPO** | 27 EU countries | ~850 € for one class, ~50 € for the 2nd, ~150 € each beyond | Within the 6-month priority window if the EU market matters |
| **USPTO** | United States | ~250–350 $ per class | Only if selling into the US — the US requires **proof of use in commerce**, which is a real constraint |

Attorney fees are on top and typically exceed the official fees. **Figures are indicative and change
— confirm on each office's current schedule.**

**ASK COUNSEL** whether the Madrid System (a single international application via WIPO) is cheaper
than separate filings for the territories actually wanted.

---

## 8. Do now, before any filing — free

- [x] Stop claiming a registration that does not exist: `TRADEMARK.md` said *"registered trademark"*.
      Corrected 2026-07-19 to a plain trademark claim, with a note that it is unregistered.
- [x] Confirm no `®` appears anywhere in the product, the site or the guides — checked across all
      five repositories on 2026-07-19; the only occurrence was in the review report describing this
      very problem.
- [ ] **Use ™ consistently** on first prominent use of TigerTag, TigerTag+, TigerTag Certified.
      ™ signals a claim, which is true today. ® asserts a registration, which is not.
- [ ] **Decide the applicant** (§2) and correct the entity string across the 7 files.
- [ ] **Keep evidence of first use** — dated screenshots, the first public release, the first
      invoice mentioning the name, the domain purchase invoices. Unregistered rights and any future
      US filing both depend on provable use, and this evidence is cheapest to collect now rather
      than reconstruct later.

---

## 9. What is already solid

Worth stating, because it means the work here is filing rather than designing: `CERTIFICATION.md`,
`TRADEMARK.md` and `VERSIONING.md` were assessed in the 2026-07-19 review as *"a competent CSA/Matter
clone"* — a two-mark split (free self-declared vs audited paid), a full
conformance → audit → declaration → issuance → surveillance → revocation process, a certified
registry, and honest disclosure that third-party labs do not exist yet. The programme is designed.
**It is the registration that is missing, not the thinking.**
