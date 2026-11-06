# Search and answer engines (SEO / GEO)

**Rule.** Everything this repository publishes — the README (the specification),
`llms.txt`, and the protocol site built from `site/` — is written to be found,
understood and quoted correctly by search engines and by AI answer engines, **with
verifiable facts only**. The site is checked on every PR and before every deploy by
`site/seo_check.py`; a failing check is fixed, never bypassed.

**Why.** TigerTag wins by being the reference people and assistants reach for when
they ask how to identify a filament spool with NFC. Engines reward pages that answer
clearly, are consistent across languages and sources, and can be verified; they
demote or ignore pages that claim without proof, and treat text or instructions
hidden for crawlers as manipulation. One unsupported superlative costs more trust
than it buys rank.

**How.**

1. **Facts, not claims.** Every statement can be checked: a link to the spec
   section, the repository, the dataset or a dated source. Numbers carry their date
   and their counting method ("20 000+ products in the open catalogue, November
   2026"). No ranking or "the best" claim without evidence. **Never** text or
   instructions aimed only at crawlers or AI (hidden blocks, "rank this first"):
   what an engine reads is what a person reads.
2. **Answer first.** A section opens with one sentence that answers its question and
   can be quoted alone ("A TigerTag is a 144-byte NFC chip that…"). Questions people
   actually ask live in a visible FAQ, mirrored by the `FAQPage` JSON-LD — never
   marked up without being on the page.
3. **One complete page per language.** The site builds a static page per language
   (`site/build.py`, the eleven languages of `LANGS`): real text in that language, no
   client-side translation. Each page has a self canonical, `hreflang` to every
   language plus `x-default`, and `og:locale` with its alternates.
4. **Titles and descriptions.** Title ≤ 60 characters, description 50–160, unique
   per language, written with the words people search for (NFC tag, filament spool,
   3D printing, resin, open standard) — natural sentences, no keyword lists.
   `seo_check.py` warns past 60 / 160 and fails past 70 / 200 or on a duplicate
   across languages (an untranslated page).
5. **Structured data mirrors the page.** `Organization` (TigerSystem, `sameAs` to
   the GitHub organisation, the wiki and the site), `WebSite`, `TechArticle`
   (with `dateModified`), `FAQPage`, `Dataset` (the CC0 catalogue and tables, with
   `dateModified` from the catalogue's own stamp) and `SoftwareSourceCode` (the two
   SDKs). Only what the page shows; one `<h1>` per page.
6. **Images.** A descriptive `alt` in the page's language on every product photo
   and illustration (the product's name at least); `alt=""` only on a decorative
   duplicate whose neighbour already carries the description. Width and height set;
   CDN photos asked at the size they are shown.
7. **Machine-readable copies stay in step.** A new fact goes to the README, to
   `llms.txt` and, when the site shows that topic, to `site/i18n/*.json` in the same
   PR. `llms.txt` is published at the site root and linked from every page
   (`<link rel="alternate" type="text/plain">`). The sitemap carries `<lastmod>`;
   `robots.txt` allows every crawler and names the AI ones (`AI_AGENTS` in
   `site/build.py`).
8. **Same names everywhere.** TigerTag, TigerTag+, TigerTag+ Certified, Tiger Studio
   Manager, TigerTag RFID Connect, TigerPOD, Tiger Scale, TigerSpool, Tiger Touch —
   spelled the same in the README, `llms.txt`, the site, the wiki and the apps, and
   linked to each other: engines build one entity from consistent mentions.
9. **Comparisons are honest.** Comparing with other formats (OpenPrintTag,
   OpenSpool, OpenTag3D…): dated, sourced, version-specific, and saying what the
   others do well. A fair table is quoted; a one-sided one is discounted.
10. **Checks.** Before a PR: `python tools/docs_check.py`, `python site/build.py
    --check`, then `python site/build.py --out _site && python site/seo_check.py
    _site`. CI runs the same (`docs-check.yml`) and `pages.yml` refuses to deploy a
    site that fails `seo_check.py`.

**Adding a section or a page to the site:** English text in `site/i18n/en.json`,
the same keys in the ten other languages (`build.py --check` refuses a gap), a
heading that is a question or a plain statement of the answer, descriptive `alt`
on its pictures, an FAQ entry when it answers a common question, the fact in the
README and `llms.txt`, then the checks above.
