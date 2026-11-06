# TigerTag RFID Guide — notes for agents and contributors

This repository is the **TigerTag protocol**: the specification (`README.md`), the
reference database (`database/`), the machine-readable description (`llms.txt`) and
the public protocol site built from `site/` and published on GitHub Pages
(<https://tigertag-project.github.io/TigerTag-RFID-Guide/>).

## Where things are

| Path | What it is |
|---|---|
| `README.md` | The specification and the ecosystem overview — the source of truth for facts |
| `llms.txt` | The same facts for AI assistants; kept in step with the README |
| `database/` | Reference tables and catalogue, **generated** from the TigerTag backend (Xano) by `database/db_update.py`, split per brand by `database/split_catalog.py` |
| `site/` | The protocol site: `template.html`, `i18n/<lang>.json` (eleven languages), `playground.js`, `build.py`, `seo_check.py` — see `site/README.md` |
| `tools/docs_check.py` | Links, assets and facts that must agree across documents |
| `.github/workflows/` | `sync-database.yml` (every 6 h), `docs-check.yml` (PRs), `pages.yml` (site deploy) |

## Rules

- **Search and answer engines**: everything published is written to be found and
  quoted correctly, with verifiable facts only, and the site passes
  `site/seo_check.py` → [`.agents/rules/seo-geo.md`](.agents/rules/seo-geo.md)
- **Generated data**: never edit `database/*.json` by hand. A missing or wrong field
  in the export is an issue in TigerTag-Project/TigerTag-Manager (the repository
  behind manager.tigertag.io), never a workaround here.
- **No AI attribution**: commits, PRs, issues, docs and code never mention the AI
  that helped write them; no `Co-Authored-By` trailer.
- **No emoji** in the site or any UI text: inline SVG icons, or words.
- **Logo**: on a light background the contoured (black) logo, on a dark one the
  white logo (`brand/README.md`).
- **Language**: code, comments, commits, docs and rule files are in English; the
  site's text lives in `site/i18n/` in eleven languages.

## Before opening a PR

```bash
python tools/docs_check.py
python site/build.py --check
python site/build.py --out _site && python site/seo_check.py _site
```
