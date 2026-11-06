# The protocol site

The public site of the TigerTag protocol, published on GitHub Pages:
<https://tigertag-project.github.io/TigerTag-RFID-Guide/>

It presents and explains the protocol, and links to every part of the TigerSystem
ecosystem and to the other repositories. It is static HTML, one page per language,
built by [`build.py`](build.py) and published by
[`pages.yml`](../.github/workflows/pages.yml) on every push to `main` that touches
`site/`, `Images/`, `brand/` or `llms.txt`.

## Files

| File | Contents |
|---|---|
| [`template.html`](template.html) | The page. Every `{{key}}` is replaced by the text of that key in the page's language; `{{@…}}` keys are filled by `build.py` (language menu, `hreflang` links, JSON-LD, chip page grid). |
| [`i18n/en.json`](i18n/en.json) | The English text, which is the reference: every other language has exactly its keys. |
| `i18n/<lang>.json` | One file per language: `fr`, `de`, `es`, `it`, `zh` (Simplified Chinese), `pt` (Brazil), `pt-pt` (Portugal), `pl`, `ru`, `nl` — the languages of the Tiger Touch site. |
| [`site.css`](site.css), [`site.js`](site.js) | The look (dark by default, light on request) and the theme / language buttons. |
| [`playground.js`](playground.js) | The playground: build a chip from the catalogue or by hand (custom mode), or decode one, and see every byte. Its encoder is the JavaScript SDK's, byte for byte (`TigerTag.fromCatalogEntry` / `create` / `toBytes`); its words are the `pj_*` keys, its labels the `pg_*` keys. The codec is exposed as `window.TigerTagPlayground` in the browser console. |
| [`assets/`](assets/) | Pictures made for the site. The others come from `Images/` and `brand/`, so the site shows the same pictures as the README. |
| [`og.jpg`](og.jpg) | The picture shown when the site is shared (1200 × 630). |

The build also publishes, under `data/`, the reference tables the playground reads
(`id_brand`, `id_material`, `id_aspect`, `id_type`, `id_diameter`, `id_measure_unit`) and
the per-brand catalogue (`data/brands/`), straight from `database/`. A catalogue sync
redeploys the site, so the playground always shows the current catalogue.

## Editing

- **Change a text**: edit `i18n/en.json`, then the same key in every other language.
- **Add a text**: add the key to every `i18n/*.json` file and use `{{key}}` in `template.html`.
  The build refuses a language that misses a key, has an unknown one or an empty value.
- **Check and preview**:

  ```bash
  python3 site/build.py --check
  python3 site/build.py && python3 -m http.server 8000 --directory _site
  python3 site/build.py --only en   # English only, while translations are pending
  ```

- **Search and answer engines**: `python3 site/build.py --out _site && python3 site/seo_check.py _site`
  checks every page (title and description length, one `h1`, canonical and `hreflang`,
  sharing cards, `alt` text, JSON-LD types and the FAQ they mirror, in-page links,
  sitemap, robots, `llms.txt`). It runs on every PR and before every deploy; the rule
  behind it is [`.agents/rules/seo-geo.md`](../.agents/rules/seo-geo.md).

The English page is the root (`/`), every other language has its own folder (`/fr/`,
`/zh/`…): each page is complete in its language for readers, search engines and AI
assistants, and the pages point to each other with `hreflang`. A language chosen in the
menu is remembered, and the English root forwards to it on the next visit.
