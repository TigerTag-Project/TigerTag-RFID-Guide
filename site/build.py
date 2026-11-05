# SPDX-License-Identifier: Apache-2.0
#
# TigerTag NFC (RFID-compatible) Guide
# Copyright (c) 2025-2026 TigerTag Corp.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Build the TigerTag protocol site (GitHub Pages) into `_site/`.

One static page per language, all from `template.html` and `i18n/<lang>.json`:
English at the root, the others under `/<lang>/`. Every page is complete HTML in
its own language — what a search engine, an AI crawler or a reader without
JavaScript sees — with `hreflang` links between them, a FAQPage JSON-LD in its
language, and a sitemap listing them all.

The images come from the repository's own `Images/` and `brand/` folders, so the
site always shows the same pictures as the README.

Usage:
    python site/build.py                 # build into _site/
    python site/build.py --check         # only check the translations
    python site/build.py --out DIR --url https://example.org/path/
"""

import argparse
import html
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SITE_URL = "https://tigertag-project.github.io/TigerTag-RFID-Guide/"

# The eleven languages of the Tiger Touch site, in the same order. `pt` (Brazil)
# and `pt-pt` (Portugal) are separate dictionaries on purpose.
LANGS = ["en", "fr", "de", "es", "it", "zh", "pt", "pt-pt", "pl", "ru", "nl"]
HTML_LANG = {"zh": "zh-Hans", "pt": "pt-BR", "pt-pt": "pt-PT"}
OG_LOCALE = {"en": "en_US", "fr": "fr_FR", "de": "de_DE", "es": "es_ES", "it": "it_IT",
             "zh": "zh_CN", "pt": "pt_BR", "pt-pt": "pt_PT", "pl": "pl_PL", "ru": "ru_RU", "nl": "nl_NL"}

# Repository file -> published path under assets/.
ASSETS = {
    "Images/TigerSystem_Hero.webp": "TigerSystem_Hero.webp",
    "Images/TigerStudio_Pod.webp": "TigerStudio_Pod.webp",
    "Images/TigerTag_RFID_Connect_Apps.png": "TigerTag_RFID_Connect_Apps.png",
    "Images/TigerScale_V3.png": "TigerScale_V3.png",
    "Images/TigerSpool.png": "TigerSpool.png",
    "Images/TigerTouch.png": "TigerTouch.png",
    "Images/Box_eSun.png": "Box_eSun.png",
    "Images/Box_Rosa3D.png": "Box_Rosa3D.png",
    "Images/Box_Sunlu.png": "Box_Sunlu.png",
    # White logo on the dark theme, black (contouring) logo on the light one.
    "brand/logo_tigertag_head.svg": "logo-tigertag-white.svg",
    "brand/logo_tigertag_contouring_head.svg": "logo-tigertag-black.svg",
    "brand/tigersystem-icon-framed.svg": "favicon.svg",
}

# The playground reads these, published under data/ next to the pages.
DATA_TABLES = ["id_brand.json", "id_material.json", "id_aspect.json", "id_type.json",
               "id_diameter.json", "id_measure_unit.json"]
# The product the playground opens with (Rosa3D PLA-Silk Red).
DEFAULT_PRODUCT_ID = 710056716


def default_product():
    """The playground's first product, taken from its brand file, inlined in every page."""
    index = json.loads((REPO / "database/brands/index.json").read_text(encoding="utf-8"))
    for brand in index["brands"]:
        products = json.loads((REPO / "database/brands" / brand["file"]).read_text(encoding="utf-8"))
        for product in products:
            if product.get("id") == DEFAULT_PRODUCT_ID:
                return product
    raise SystemExit(f"error: default playground product {DEFAULT_PRODUCT_ID} is not in the catalogue")


def script_json(value):
    """JSON safe inside a <script> block."""
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


PLACEHOLDER = re.compile(r"\{\{([a-z0-9_@]+)\}\}")


def load_dictionaries():
    """Every language, checked against English: same keys, none empty."""
    dicts = {}
    for lang in LANGS:
        path = HERE / "i18n" / f"{lang}.json"
        if not path.exists():
            raise SystemExit(f"error: missing translation {path.relative_to(REPO)}")
        dicts[lang] = json.loads(path.read_text(encoding="utf-8"))
    reference = list(dicts["en"])
    problems = []
    for lang, words in dicts.items():
        missing = [k for k in reference if k not in words]
        extra = [k for k in words if k not in dicts["en"]]
        empty = [k for k, v in words.items() if not isinstance(v, str) or not v.strip()]
        for label, keys in (("missing", missing), ("unknown", extra), ("empty", empty)):
            if keys:
                problems.append(f"{lang}.json: {label} key(s): {', '.join(keys)}")
    template_keys = set(PLACEHOLDER.findall((HERE / "template.html").read_text(encoding="utf-8")))
    unused = [k for k in template_keys if not k.startswith("@") and k not in dicts["en"]]
    if unused:
        problems.append(f"template.html uses unknown key(s): {', '.join(sorted(unused))}")
    if problems:
        raise SystemExit("error: translations do not match en.json\n  " + "\n  ".join(problems))
    return dicts


def page_path(lang):
    return "" if lang == "en" else f"{lang}/"


def pages_grid():
    """The 36 user pages of the chip, 0x04 to 0x27: data, then signature."""
    cells = []
    for page in range(0x04, 0x28):
        kind = "data" if page <= 0x17 else "sig"
        cells.append(f'        <span class="pg {kind}">{page:02X}</span>')
    return "\n".join(cells)


def render(template, lang, words, dicts, site_url, product):
    base = "" if lang == "en" else "../"
    url = site_url + page_path(lang)

    alternates = [f'<link rel="alternate" hreflang="{HTML_LANG.get(l, l)}" href="{site_url}{page_path(l)}">' for l in LANGS]
    alternates.append(f'<link rel="alternate" hreflang="x-default" href="{site_url}">')

    menu = []
    for l in LANGS:
        current = ' aria-current="true"' if l == lang else ""
        menu.append(f'          <li><a href="{base}{page_path(l)}" hreflang="{HTML_LANG.get(l, l)}" '
                    f'lang="{HTML_LANG.get(l, l)}" data-lang="{l}"{current}>{html.escape(dicts[l]["lang_name"])}</a></li>')

    faq = [{"@type": "Question", "name": words[f"faq{i}_q"],
            "acceptedAnswer": {"@type": "Answer", "text": words[f"faq{i}_a"]}} for i in range(1, 8)]
    jsonld = [
        {"@context": "https://schema.org", "@type": "WebSite", "name": "TigerTag", "url": url,
         "inLanguage": HTML_LANG.get(lang, lang), "description": words["meta_description"]},
        {"@context": "https://schema.org", "@type": "TechArticle", "headline": words["meta_title"],
         "about": "TigerTag NFC protocol for 3D-printing materials", "inLanguage": HTML_LANG.get(lang, lang),
         "url": url, "image": site_url + "assets/og.jpg",
         "license": "https://creativecommons.org/licenses/by/4.0/",
         "isBasedOn": "https://github.com/TigerTag-Project/TigerTag-RFID-Guide",
         "publisher": {"@type": "Organization", "name": "TigerTag Corp", "url": "https://tigersystem.io"}},
        {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": HTML_LANG.get(lang, lang), "mainEntity": faq},
    ]
    jsonld.append({
        "@context": "https://schema.org", "@type": "Dataset",
        "name": "TigerTag product catalogue and reference tables",
        "description": "Open catalogue of 3D-printing filament and resin products with the ids written on TigerTag NFC chips, "
                       "the reference tables (materials, brands, aspects, types, diameters, units) and one file per brand.",
        "url": "https://github.com/TigerTag-Project/TigerTag-RFID-Guide/tree/main/database",
        "license": "https://creativecommons.org/publicdomain/zero/1.0/",
        "isAccessibleForFree": True,
        "creator": {"@type": "Organization", "name": "TigerTag Corp", "url": "https://tigersystem.io"},
        "distribution": [
            {"@type": "DataDownload", "encodingFormat": "application/json",
             "contentUrl": "https://raw.githubusercontent.com/TigerTag-Project/TigerTag-RFID-Guide/main/database/id_catalog.json"},
            {"@type": "DataDownload", "encodingFormat": "application/json",
             "contentUrl": "https://raw.githubusercontent.com/TigerTag-Project/TigerTag-RFID-Guide/main/database/brands/index.json"},
        ],
    })
    # `</` never appears inside a <script> block.
    jsonld_html = "\n".join('<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False).replace("</", "<\\/") + "</script>"
                            for j in jsonld)

    special = {
        "@lang": lang,
        "@htmllang": HTML_LANG.get(lang, lang),
        "@oglocale": OG_LOCALE[lang],
        "@url": url,
        "@siteurl": site_url,
        "@base": base,
        "@langpath": page_path(lang),
        "@alternates": "\n".join(alternates),
        "@langmenu": "\n".join(menu),
        "@pages": pages_grid(),
        "@pgi18n": script_json({k[3:]: v for k, v in words.items() if k.startswith("pj_")}),
        "@pgdefault": script_json(product),
        "@jsonld": jsonld_html,
        "@trademark": f'<a href="https://github.com/TigerTag-Project/TigerTag-RFID-Guide/blob/main/TRADEMARK.md">{html.escape(words["foot_trademark"])}</a>',
    }

    def fill(match):
        key = match.group(1)
        if key in special:
            return special[key]
        return html.escape(words[key], quote=True)

    return PLACEHOLDER.sub(fill, template)


def build(out, site_url):
    dicts = load_dictionaries()
    template = (HERE / "template.html").read_text(encoding="utf-8")
    product = default_product()
    if out.exists():
        shutil.rmtree(out)
    (out / "assets").mkdir(parents=True)

    for lang in LANGS:
        target = out / page_path(lang) / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(template, lang, dicts[lang], dicts, site_url, product), encoding="utf-8")

    # The reference tables and the per-brand catalogue, for the playground.
    (out / "data" / "brands").mkdir(parents=True)
    for name in DATA_TABLES:
        shutil.copy2(REPO / "database" / name, out / "data" / name)
    for path in (REPO / "database" / "brands").glob("*.json"):
        shutil.copy2(path, out / "data" / "brands" / path.name)
    for name in ("site.css", "site.js", "playground.js"):
        shutil.copy2(HERE / name, out / name)
    for source, published in ASSETS.items():
        shutil.copy2(REPO / source, out / "assets" / published)
    # Pictures made for the site itself (site/assets/), next to the README's.
    for extra in sorted((HERE / "assets").glob("*")):
        shutil.copy2(extra, out / "assets" / extra.name)
    og = HERE / "og.jpg"
    if og.exists():
        shutil.copy2(og, out / "assets" / "og.jpg")
    # The machine-readable description of the protocol, at the site root too.
    shutil.copy2(REPO / "llms.txt", out / "llms.txt")

    urls = "\n".join(
        "  <url><loc>{}</loc>{}</url>".format(
            site_url + page_path(lang),
            "".join(f'<xhtml:link rel="alternate" hreflang="{HTML_LANG.get(l, l)}" href="{site_url}{page_path(l)}"/>' for l in LANGS))
        for lang in LANGS)
    (out / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        f"{urls}\n</urlset>\n", encoding="utf-8")
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {site_url}sitemap.xml\n", encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    print(f"built {len(LANGS)} languages into {out}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(REPO / "_site"))
    parser.add_argument("--url", default=SITE_URL)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--only", help="comma-separated languages, for a quick local preview")
    args = parser.parse_args()
    if args.only:
        LANGS[:] = [l for l in LANGS if l in args.only.split(",")]
    if args.check:
        load_dictionaries()
        print(f"translations OK: {len(LANGS)} languages")
        return
    url = args.url if args.url.endswith("/") else args.url + "/"
    build(Path(args.out), url)


if __name__ == "__main__":
    sys.exit(main())
