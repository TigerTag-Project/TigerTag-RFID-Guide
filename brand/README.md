# TigerTag brand assets

## © 2025–2026 TigerTag Corp. All rights reserved.

**The contents of this directory are NOT covered by the licences in
[`../LICENSING.md`](../LICENSING.md).**

The specification is CC-BY-4.0. The reference database is CC0. The sample code is
Apache-2.0. **The logo, wordmark, banner, and icons in this directory are none of those.**
They are proprietary artwork and registered trademarks of TigerTag Corp, and no copyright
licence to them is granted by any file in this repository.

This is intentional and it is how open standards work. The protocol is free so that anyone
can implement it. The mark is protected so that "TigerTag" continues to mean something.

---

## What you may do without asking

You have a limited, revocable permission to use the TigerTag logo, **unmodified**, to state
a true fact about compatibility:

- inside your application's UI,
- in your documentation, README, or store listing,
- on packaging, to indicate that a spool carries a TigerTag chip.

## What you may not do

- Modify the logo — no recolouring, stretching, cropping, or recomposition.
- Use "TigerTag" in your product, company, or domain name.
- Imply affiliation, certification, endorsement, or partner status you do not have.
- Present your product as "TigerTag+" unless its tags carry a signature issued by
  TigerTag Corp.

Full terms: [`../TRADEMARK.md`](../TRADEMARK.md).
Official partner status and packaging rights: [`../LICENSE_COMMERCIAL.md`](../LICENSE_COMMERCIAL.md).

---

## Usage guidelines

| Asset | Use on |
|---|---|
| `logo_tigertag_contouring.svg` | White and light backgrounds |
| `logo_tigertag.svg` | Dark backgrounds only |
| `TigerTag_Banner.png` | Press, social, article headers |
| `TigerTag_Logo.png` | Raster fallback where SVG is unsupported |
| `icon.png`, `icon.ico`, `icon.icns` | Application icons for compatible tools |

Preserve clear space around the logo equal to the height of the tiger's ear. Do not place
the logo on a background that reduces its contrast below legibility.

---

## Icon kit — neutral and marked

Two families of "Tiger" icon assets, in addition to the historical lettered logo above
(`TigerTag_Logo.png`, `logo_tigertag.svg`, `logo_tigertag_contouring.svg`,
`icon.icns/ico/png`), which remain the canonical references for brand communication and
stay in use everywhere they already are. Nothing below replaces them — these are
**additional** assets for contexts the historical logo doesn't fit well.

Each family ships in the same three compositions:

- **overflow** — the default: a rounded black card with the tiger elements deliberately
  breaking past its edge, outlined with a white keyline. Display as-is, uncropped.
- **contained** — the same artwork kept fully inside the rounded card. Use wherever the
  shape gets masked (round favicons, adaptive/maskable app icons) — an overflowing
  element would get clipped by the mask.
- **square** — the same artwork on a full-bleed square card (black fills 100% of the
  canvas). Use wherever a masked context needs a square source instead of a rounded one
  (platforms that apply their own corner-rounding).

### Neutral (no wordmark)

Tiger-head motif only, no "TIGER TAG" lettering. Use in product/app contexts where the
name is already displayed next to the icon, or where a wordmark would be superfluous or
illegible at the render size (small app icons, favicons, tray icons).

| Asset | Composition | Use on |
|---|---|---|
| `logo_tigertag_head.svg` | Lockup (head + speed lines + circuit traces), white motif on transparent | Headers or contexts already labelled with the product name |
| `logo_tiger_icon_overflow.svg` | Overflow | General app icon use |
| `logo_tiger_icon_contained.svg` | Contained | Masked contexts (round favicons, adaptive icons) |
| `logo_tiger_icon_square.svg` | Square | Masked contexts requiring a square source |

### Marked ("TIGER TAG" lockup)

Same tiger-head icon, with the "TIGER TAG" wordmark set below it. Use for brand
communication where a single asset carrying both the icon and the name is wanted (social
avatars, app store listings, partner decks) instead of pairing the neutral icon with
separate text.

| Asset | Composition | Use on |
|---|---|---|
| `logo_tigertag_icon_overflow.svg` | Overflow | General brand lockup use |
| `logo_tigertag_icon_contained.svg` | Contained | Masked contexts (round favicons, adaptive icons) |
| `logo_tigertag_icon_square.svg` | Square | Masked contexts requiring a square source |

Same trademark terms apply to both families: unmodified use only, no implied affiliation or
endorsement. Full rules: [`../TRADEMARK.md`](../TRADEMARK.md).

---

## Questions

Trademark authorization requests and press enquiries:
[tigertag@tigertag.io](mailto:tigertag@tigertag.io)
