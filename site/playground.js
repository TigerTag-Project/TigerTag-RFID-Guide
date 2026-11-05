/* The TigerTag playground: build a chip from the catalogue or by hand, or decode
   one, and see every byte. Everything runs in the browser; the reference tables
   and the per-brand catalogue files are static JSON published with the site.

   The encoder mirrors the JavaScript SDK byte for byte (TigerTag.create /
   fromCatalogEntry / toBytes in TigerTag-SDK-JS src/tag.js). Words come from the
   page's own language (the #pg-i18n block written by site/build.py). */
(function () {
  "use strict";
  const root = document.getElementById("playground");
  if (!root) return;
  const T = JSON.parse(document.getElementById("pg-i18n").textContent);
  const DATA = root.dataset.data;                       // "data/" or "../data/"
  const DEFAULT_PRODUCT = JSON.parse(document.getElementById("pg-default").textContent);

  const ID_TIGERTAG = 0x5BF59264, ID_PLUS = 0xBC0FCB97, ID_INIT = 0x6C41A2E1;
  const MAKER_PRODUCT = 0xFFFFFFFF;
  const EPOCH_MS = Date.UTC(2000, 0, 1);

  /* The 80 data bytes, field by field (README section 2). `group` gives the colour. */
  const FIELDS = [
    { key: "id_tigertag", off: 0, len: 4, group: "id" },
    { key: "id_product", off: 4, len: 4, group: "id" },
    { key: "id_material", off: 8, len: 2, group: "mat" },
    { key: "id_aspect1", off: 10, len: 1, group: "mat" },
    { key: "id_aspect2", off: 11, len: 1, group: "mat" },
    { key: "id_type", off: 12, len: 1, group: "mat" },
    { key: "id_diameter", off: 13, len: 1, group: "mat" },
    { key: "id_brand", off: 14, len: 2, group: "mat" },
    { key: "color1", off: 16, len: 4, group: "col" },
    { key: "measure", off: 20, len: 3, group: "qty" },
    { key: "id_unit", off: 23, len: 1, group: "qty" },
    { key: "nozzle_min", off: 24, len: 2, group: "set" },
    { key: "nozzle_max", off: 26, len: 2, group: "set" },
    { key: "dry_temp", off: 28, len: 1, group: "set" },
    { key: "dry_time", off: 29, len: 1, group: "set" },
    { key: "bed_min", off: 30, len: 1, group: "set" },
    { key: "bed_max", off: 31, len: 1, group: "set" },
    { key: "timestamp", off: 32, len: 4, group: "twin" },
    { key: "color2", off: 36, len: 3, group: "col" },
    { key: "tag_info", off: 39, len: 1, group: "twin" },
    { key: "color3", off: 40, len: 3, group: "col" },
    { key: "reserved", off: 43, len: 1, group: "res" },
    { key: "td", off: 44, len: 2, group: "set" },
    { key: "reserved", off: 46, len: 2, group: "res" },
    { key: "message", off: 48, len: 28, group: "msg" },
    { key: "measure_available", off: 76, len: 3, group: "qty" },
    { key: "reserved", off: 79, len: 1, group: "res" },
    { key: "signature", off: 80, len: 64, group: "sig" },
  ];

  const $ = (sel) => root.querySelector(sel);
  const tables = { brand: new Map(), material: new Map(), aspect: new Map(), type: new Map(), diameter: new Map(), unit: new Map() };
  let materials = [];
  let brandIndex = [];
  const brandFiles = new Map();
  let current = null;           // the TigerTag fields shown
  let previous = null;          // the previous bytes, to flash the ones that changed
  let selected = null;          // the selected field index

  /* ── Encoding (SDK parity) ─────────────────────────────────────────────── */
  function encode(f) {
    const b = new Uint8Array(144);
    const dv = new DataView(b.buffer);
    dv.setUint32(0, f.idTigertag >>> 0);
    dv.setUint32(4, f.idProduct >>> 0);
    dv.setUint16(8, f.idMaterial & 0xFFFF);
    b[10] = f.idAspect1 & 0xFF; b[11] = f.idAspect2 & 0xFF;
    b[12] = f.idType & 0xFF; b[13] = f.idDiameter & 0xFF;
    dv.setUint16(14, f.idBrand & 0xFFFF);
    b[16] = f.c1[0]; b[17] = f.c1[1]; b[18] = f.c1[2]; b[19] = f.c1[3];
    const m = f.measure & 0xFFFFFF; b[20] = m >> 16; b[21] = (m >> 8) & 0xFF; b[22] = m & 0xFF;
    b[23] = f.idUnit & 0xFF;
    dv.setUint16(24, f.nozzleMin & 0xFFFF); dv.setUint16(26, f.nozzleMax & 0xFFFF);
    b[28] = f.dryTemp & 0xFF; b[29] = f.dryTime & 0xFF; b[30] = f.bedMin & 0xFF; b[31] = f.bedMax & 0xFF;
    dv.setUint32(32, f.timestamp >>> 0);
    b[36] = f.c2[0]; b[37] = f.c2[1]; b[38] = f.c2[2];
    b[39] = ((f.tagIndex & 0x0F) << 4) | (f.tagCount & 0x0F);
    b[40] = f.c3[0]; b[41] = f.c3[1]; b[42] = f.c3[2];
    dv.setUint16(44, f.tdRaw & 0xFFFF);
    b.set(new TextEncoder().encode(f.message || "").subarray(0, 28), 48);
    const ma = f.measureAvailable & 0xFFFFFF; b[76] = ma >> 16; b[77] = (ma >> 8) & 0xFF; b[78] = ma & 0xFF;
    if (f.signature) b.set(f.signature.subarray(0, 64), 80);
    return b;
  }

  function decode(b) {
    const dv = new DataView(b.buffer, b.byteOffset, b.byteLength);
    const u24 = (o) => (b[o] << 16) | (b[o + 1] << 8) | b[o + 2];
    let msgEnd = 48; while (msgEnd < 76 && b[msgEnd]) msgEnd++;
    const sig = b.length >= 144 ? b.slice(80, 144) : new Uint8Array(64);
    return {
      idTigertag: dv.getUint32(0), idProduct: dv.getUint32(4), idMaterial: dv.getUint16(8),
      idAspect1: b[10], idAspect2: b[11], idType: b[12], idDiameter: b[13], idBrand: dv.getUint16(14),
      c1: [b[16], b[17], b[18], b[19]], measure: u24(20), idUnit: b[23],
      nozzleMin: dv.getUint16(24), nozzleMax: dv.getUint16(26), dryTemp: b[28], dryTime: b[29],
      bedMin: b[30], bedMax: b[31], timestamp: dv.getUint32(32),
      c2: [b[36], b[37], b[38]], tagIndex: b[39] >> 4, tagCount: b[39] & 0x0F, c3: [b[40], b[41], b[42]],
      tdRaw: dv.getUint16(44), message: new TextDecoder().decode(b.slice(48, msgEnd)),
      measureAvailable: u24(76), signature: sig.some((x) => x) ? sig : null,
    };
  }

  const nowTs = () => Math.max(0, Math.floor((Date.now() - EPOCH_MS) / 1000));
  const hexRgb = (h) => {
    const m = /^#?([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})/i.exec(h || "");
    return m ? [parseInt(m[1], 16), parseInt(m[2], 16), parseInt(m[3], 16)] : [0, 0, 0];
  };
  const rgbHex = (c) => "#" + c.slice(0, 3).map((x) => x.toString(16).padStart(2, "0")).join("");

  /* TigerTag.fromCatalogEntry: data1 = diameter, data2/3 = nozzle, data4/5 = drying, data6/7 = bed. */
  function fromCatalog(entry) {
    const r = entry.RFID_Data || {};
    const n = (v) => (v == null ? 0 : Number(v));
    const colors = (entry.color_info && entry.color_info.colors) || [];
    const c2 = r.color_r2 != null ? [n(r.color_r2), n(r.color_g2), n(r.color_b2)] : colors[1] ? hexRgb(colors[1]) : [0, 0, 0];
    const c3 = r.color_r3 != null ? [n(r.color_r3), n(r.color_g3), n(r.color_b3)] : colors[2] ? hexRgb(colors[2]) : [0, 0, 0];
    return {
      idTigertag: ID_PLUS, idProduct: Number(entry.id) >>> 0,
      idMaterial: n(r.id_material), idAspect1: n(r.id_aspect1), idAspect2: n(r.id_aspect2),
      idType: n(r.id_type), idDiameter: n(r.data1), idBrand: n(r.id_brand),
      c1: [n(r.color_r), n(r.color_g), n(r.color_b), r.color_a == null ? 255 : n(r.color_a)], c2, c3,
      measure: n(r.measure), idUnit: n(r.id_unit), measureAvailable: n(r.measure),
      nozzleMin: n(r.data2), nozzleMax: n(r.data3), dryTemp: n(r.data4), dryTime: n(r.data5),
      bedMin: n(r.data6), bedMax: n(r.data7), timestamp: nowTs(), tagIndex: 0, tagCount: 0,
      tdRaw: 0, message: "", signature: null, entry,
    };
  }

  /* ── Words ─────────────────────────────────────────────────────────────── */
  const label = (map, id) => (map.get(id) || (id ? "#" + id : "—"));
  function typeName(id) {
    if (id === ID_TIGERTAG) return "TigerTag";
    if (id === ID_PLUS) return "TigerTag+";
    if (id === ID_INIT) return "TigerTag Init";
    return T.unknown;
  }
  function value(i, f) {
    const fld = FIELDS[i];
    switch (fld.key) {
      case "id_tigertag": return typeName(f.idTigertag);
      case "id_product": return f.idProduct === MAKER_PRODUCT ? T.no_product : String(f.idProduct);
      case "id_material": return label(tables.material, f.idMaterial);
      case "id_aspect1": return label(tables.aspect, f.idAspect1);
      case "id_aspect2": return label(tables.aspect, f.idAspect2);
      case "id_type": return label(tables.type, f.idType);
      case "id_diameter": return tables.diameter.has(f.idDiameter) ? tables.diameter.get(f.idDiameter) + " mm" : label(tables.diameter, f.idDiameter);
      case "id_brand": return label(tables.brand, f.idBrand);
      case "color1": return rgbHex(f.c1).toUpperCase() + " · α " + f.c1[3];
      case "color2": return f.c2.some((x) => x) ? rgbHex(f.c2).toUpperCase() : "—";
      case "color3": return f.c3.some((x) => x) ? rgbHex(f.c3).toUpperCase() : "—";
      case "measure": return String(f.measure);
      case "id_unit": return label(tables.unit, f.idUnit);
      case "measure_available": return f.measureAvailable + " " + (tables.unit.get(f.idUnit) || "");
      case "nozzle_min": return f.nozzleMin + " °C";
      case "nozzle_max": return f.nozzleMax + " °C";
      case "dry_temp": return f.dryTemp + " °C";
      case "dry_time": return f.dryTime + " h";
      case "bed_min": return f.bedMin + " °C";
      case "bed_max": return f.bedMax + " °C";
      case "timestamp": return new Date(EPOCH_MS + f.timestamp * 1000).toISOString().slice(0, 16).replace("T", " ") + " UTC";
      case "tag_info": return f.tagCount ? T.tag_of.replace("{i}", f.tagIndex || "?").replace("{n}", f.tagCount) : T.unknown;
      case "td": return f.tdRaw ? (f.tdRaw / 10).toFixed(1) : "—";
      case "message": return f.message || "—";
      case "signature": return f.signature ? T.signed : T.not_signed;
      default: return "—";
    }
  }

  /* ── Rendering ─────────────────────────────────────────────────────────── */
  const fieldOf = new Array(144);
  FIELDS.forEach((fld, i) => { for (let k = 0; k < fld.len; k++) fieldOf[fld.off + k] = i; });

  function render() {
    if (!current) return;
    const bytes = encode(current);
    const grid = $(".pg-bytes");
    const cells = [];
    for (let p = 0; p < 36; p++) {
      const row = [`<span class="pg-page">${(p + 4).toString(16).toUpperCase().padStart(2, "0")}</span>`];
      for (let k = 0; k < 4; k++) {
        const o = p * 4 + k, i = fieldOf[o];
        const changed = previous && previous[o] !== bytes[o] ? " pg-changed" : "";
        const sel = selected === i ? " pg-sel" : "";
        row.push(`<button type="button" class="pg-b g-${FIELDS[i].group}${sel}${changed}" data-f="${i}" title="${T["f_" + FIELDS[i].key]} · +${o}">${bytes[o].toString(16).toUpperCase().padStart(2, "0")}</button>`);
      }
      cells.push(`<div class="pg-row">${row.join("")}</div>`);
    }
    grid.innerHTML = cells.join("");

    const rows = FIELDS.map((fld, i) => {
      const hex = Array.from(bytes.slice(fld.off, fld.off + fld.len), (x) => x.toString(16).toUpperCase().padStart(2, "0")).join(" ");
      const shown = fld.len > 8 ? hex.slice(0, 23) + " …" : hex;
      const sw = /^color/.test(fld.key) ? `<i class="pg-sw" style="background:${rgbHex(fld.key === "color1" ? current.c1 : fld.key === "color2" ? current.c2 : current.c3)}"></i>` : "";
      return `<tr data-f="${i}" class="g-${fld.group}${selected === i ? " pg-sel" : ""}"><td><span class="pg-dot"></span>${T["f_" + fld.key]}</td><td class="pg-mono">+${fld.off}${fld.len > 1 ? "–" + (fld.off + fld.len - 1) : ""}</td><td class="pg-mono">${shown}</td><td>${sw}${escapeHtml(value(i, current))}</td></tr>`;
    });
    $(".pg-fields tbody").innerHTML = rows.join("");

    // The chip's own colours, painted with the same convention as the catalogue list.
    $(".pg-spool").style.background = current.entry ? colorBg(entryRow(current.entry)) : colorBg(chipRow(current));
    $(".pg-summary").textContent = summary(current);
    $(".pg-hex").value = Array.from(bytes, (x) => x.toString(16).toUpperCase().padStart(2, "0")).join("");
    previous = bytes;
  }

  function summary(f) {
    const parts = [typeName(f.idTigertag), label(tables.brand, f.idBrand), label(tables.material, f.idMaterial)];
    if (f.idAspect1) parts.push(label(tables.aspect, f.idAspect1));
    let s = parts.join(" · ");
    s += " · " + f.measureAvailable + "/" + f.measure + " " + (tables.unit.get(f.idUnit) || "");
    if (f.nozzleMin || f.nozzleMax) s += " · " + f.nozzleMin + "–" + f.nozzleMax + " °C";
    return s;
  }

  function escapeHtml(s) { return String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])); }

  function select(i) {
    selected = selected === i ? null : i;
    const keep = previous; previous = null; render(); previous = keep;
    const fld = selected != null ? FIELDS[selected] : null;
    $(".pg-explain").textContent = fld ? T["f_" + fld.key] + " — " + T["x_" + fld.group] : T.pick_byte;
  }

  /* ── Data loading ──────────────────────────────────────────────────────── */
  async function loadJSON(path) {
    const r = await fetch(DATA + path);
    if (!r.ok) throw new Error(path + " " + r.status);
    return r.json();
  }

  async function loadTables() {
    const [brands, mats, aspects, types, diams, units, index] = await Promise.all([
      loadJSON("id_brand.json"), loadJSON("id_material.json"), loadJSON("id_aspect.json"),
      loadJSON("id_type.json"), loadJSON("id_diameter.json"), loadJSON("id_measure_unit.json"),
      loadJSON("brands/index.json"),
    ]);
    brands.forEach((x) => tables.brand.set(x.id, x.name));
    mats.forEach((x) => tables.material.set(x.id, x.label));
    aspects.forEach((x) => tables.aspect.set(x.id, x.label));
    types.forEach((x) => tables.type.set(x.id, x.label));
    diams.forEach((x) => tables.diameter.set(x.id, x.label));
    units.forEach((x) => tables.unit.set(x.id, x.label));
    materials = mats.slice().sort((a, b) => a.label.localeCompare(b.label));
    brandIndex = index.brands;
    fillSelects(brands, aspects, types, diams, units);
  }

  /* The CDN serves each product photo in several sizes (as in Tiger Studio Manager):
     ask for the one that covers the slot, never the full-size default. */
  const CDN_SIZES = [[16, "icon"], [32, "thumb"], [64, "small"], [128, "compact"], [256, "medium"], [512, "large"], [1024, "master"]];
  function cdnImg(url, cssPx) {
    if (!url || !/^https?:\/\/cdn\.tigertag\.io\/img\b/i.test(url) || /[?&]size=/.test(url)) return url || "";
    const need = cssPx * (window.devicePixelRatio || 1);
    const size = (CDN_SIZES.find(([px]) => need <= px * 1.1) || CDN_SIZES[CDN_SIZES.length - 1])[1];
    return url + (url.includes("?") ? "&" : "?") + "size=" + size;
  }

  /* The spool colour, painted exactly as every Tiger app paints it: a port of
     colorBg() in Tiger Studio Manager (renderer/inventory.js, swatch convention
     v1.2, TigerSystem-Docs material-swatch.md). Keyed on aspect ids, never labels. */
  const RAMP_ANGLE = "135deg", SPLIT_BLEND = 20;
  const ASPECT_ID = { TRICOLOR: 24, RAINBOW: 145, BICOLOR: 252 };
  const pieSplit = (colors) => {
    if (colors.length <= 3) {
      const seg = 100 / colors.length, h = SPLIT_BLEND / 2;
      const stops = colors.map((c, i) => `${c} ${+Math.max(0, i * seg + (i ? h : 0)).toFixed(2)}% ${+Math.min(100, (i + 1) * seg - (i < colors.length - 1 ? h : 0)).toFixed(2)}%`);
      return `linear-gradient(${RAMP_ANGLE}, ${stops.join(", ")})`;
    }
    const step = 360 / colors.length;
    return `conic-gradient(${colors.map((c, i) => `${c} ${i * step}deg ${(i + 1) * step}deg`).join(", ")})`;
  };
  const conicSweep = (colors) => `conic-gradient(from 0deg, ${colors.join(", ")}, ${colors[0]})`;
  function colorBg(row) {
    const ids = [row.aspect1Id, row.aspect2Id].map(Number);
    const isRainbow = ids.includes(ASPECT_ID.RAINBOW), isTricolor = ids.includes(ASPECT_ID.TRICOLOR), isBicolor = ids.includes(ASPECT_ID.BICOLOR);
    const norm = (c) => { const x = (c || "").trim().replace(/^#/, ""); const h = x.length === 8 ? x.slice(0, 6) : x; return /^[0-9a-fA-F]{6}$/.test(h) ? "#" + h : null; };
    const cls = (row.colorList || []).map(norm).filter(Boolean);
    const type = row.colorType || "";
    const own = [row.colorHex, row.colorHex2, row.colorHex3].filter(Boolean);
    if (cls.length >= 2 && type === "conic_gradient") return conicSweep(cls);
    if (cls.length >= 2 && type === "gradient") return `linear-gradient(${RAMP_ANGLE}, ${cls.join(", ")})`;
    if (cls.length >= 3 && isTricolor && !isRainbow) return conicSweep(cls);
    if (cls.length >= 2) return pieSplit(cls);
    if (cls.length === 1) return cls[0];
    if (isRainbow && isTricolor) { const [a = "#ff4d4d", b = "#ffd93d", c = "#4da3ff"] = cls; return `linear-gradient(${RAMP_ANGLE}, ${a} 0%, ${b} 50%, ${c} 100%)`; }
    if (isRainbow && isBicolor) { const [a = "#ff7a00", b = "#8a2be2"] = cls; return `linear-gradient(${RAMP_ANGLE}, ${a} 0%, ${b} 100%)`; }
    if (isRainbow) {
      if (own.length >= 2) return `linear-gradient(${RAMP_ANGLE}, ${own.join(", ")})`;
      if (own.length === 1) return own[0];
      return `linear-gradient(${RAMP_ANGLE}, #ff0000, #ff8800, #ffff00, #00cc00, #0000ff, #8b00ff)`;
    }
    if (isTricolor) { const [a = "#cccccc", b = "#888888", c] = own; return c ? conicSweep([a, b, c]) : pieSplit([a, b]); }
    if (isBicolor) { const [a = "#cccccc", b = "#ffffff"] = own; return pieSplit([a, b]); }
    return row.colorHex || "#1c2030";
  }
  /* A catalogue entry, or the chip being shown, as colorBg() reads it. */
  function entryRow(p) {
    const r = p.RFID_Data || {};
    return { colorList: (p.color_info && p.color_info.colors) || [], colorType: p.color_info && p.color_info.type,
             aspect1Id: r.id_aspect1, aspect2Id: r.id_aspect2, colorHex: p.color };
  }
  function chipRow(f) {
    const hex = (c) => (c && c.some((x) => x) ? rgbHex(c) : null);
    return { colorList: [], aspect1Id: f.idAspect1, aspect2Id: f.idAspect2,
             colorHex: rgbHex(f.c1), colorHex2: hex(f.c2), colorHex3: hex(f.c3) };
  }

  /* Hover a product photo: a larger preview beside it, after a short delay so a
     sweep down the list does not flash one per row (Tiger Studio Manager's thumb zoom). */
  const ZOOM_PX = 220;
  let zoomEl = null, zoomTimer = 0, zoomFor = null;
  function hideZoom() { clearTimeout(zoomTimer); zoomFor = null; if (zoomEl) zoomEl.classList.remove("is-on"); }
  function showZoom(wrap) {
    if (!zoomEl) {
      zoomEl = document.createElement("div");
      zoomEl.className = "pg-zoom"; zoomEl.setAttribute("aria-hidden", "true"); zoomEl.innerHTML = "<img alt=\"\">";
      document.body.appendChild(zoomEl);
    }
    const img = zoomEl.firstChild;
    if (img.getAttribute("src") !== wrap.dataset.zoom) img.src = wrap.dataset.zoom;
    zoomEl.style.setProperty("--spool-bg", wrap.style.getPropertyValue("--spool-bg") || "transparent");
    const r = wrap.getBoundingClientRect(), size = ZOOM_PX + 12, gap = 12;
    const left = r.right + gap + size < innerWidth ? r.right + gap : Math.max(8, r.left - gap - size);
    const top = Math.min(Math.max(8, r.top + r.height / 2 - size / 2), innerHeight - size - 8);
    zoomEl.style.left = left + "px"; zoomEl.style.top = top + "px";
    zoomEl.classList.add("is-on");
  }
  if (window.matchMedia("(hover: hover)").matches) {
    document.addEventListener("mouseover", (e) => {
      const wrap = e.target.closest && e.target.closest(".pg-thumb[data-zoom]");
      if (wrap === zoomFor) return;
      hideZoom();
      if (!wrap) return;
      zoomFor = wrap;
      zoomTimer = setTimeout(() => { if (zoomFor === wrap && wrap.isConnected) showZoom(wrap); }, 220);
    });
    document.addEventListener("scroll", hideZoom, true);
    document.addEventListener("mousedown", hideZoom, true);
  }

  function opt(v, t, sel) { return `<option value="${v}"${sel ? " selected" : ""}>${escapeHtml(t)}</option>`; }

  function fillSelects(brands, aspects, types, diams, units) {
    $("#pg-cat-brand").innerHTML = opt("", T.choose_brand) + brandIndex.map((b) => opt(b.file, `${b.brand} (${b.entries})`)).join("");
    const byName = (a, b) => (a.name || a.label).localeCompare(b.name || b.label);
    $("#pg-c-brand").innerHTML = brands.slice().sort(byName).map((b) => opt(b.id, b.name)).join("");
    $("#pg-c-material").innerHTML = materials.map((m) => opt(m.id, m.label)).join("");
    $("#pg-c-aspect1").innerHTML = aspects.map((a) => opt(a.id, a.label)).join("");
    $("#pg-c-aspect2").innerHTML = aspects.map((a) => opt(a.id, a.label)).join("");
    $("#pg-c-type").innerHTML = types.map((a) => opt(a.id, a.label)).join("");
    $("#pg-c-diameter").innerHTML = diams.map((a) => opt(a.id, a.label + " mm")).join("");
    $("#pg-c-unit").innerHTML = units.map((a) => opt(a.id, a.label)).join("");
  }

  async function brandProducts(file) {
    if (!brandFiles.has(file)) brandFiles.set(file, loadJSON("brands/" + file));
    return brandFiles.get(file);
  }

  /* ── Catalogue tab ─────────────────────────────────────────────────────── */
  let products = [];
  async function onBrand() {
    const file = $("#pg-cat-brand").value;
    $("#pg-cat-list").innerHTML = "";
    products = [];
    if (!file) return;
    $("#pg-cat-list").innerHTML = `<li class="pg-muted">${T.loading}</li>`;
    try { products = await brandProducts(file); } catch (e) { $("#pg-cat-list").innerHTML = `<li class="pg-muted">${T.load_error}</li>`; return; }
    listProducts();
  }
  function listProducts() {
    const q = $("#pg-cat-search").value.trim().toLowerCase();
    const hits = products.filter((p) => !q || [p.title, p.sku, p.barcode, p.material, p.series].some((v) => v && String(v).toLowerCase().includes(q)));
    $("#pg-cat-list").innerHTML = hits.slice(0, 60).map((p) =>
      `<li><button type="button" data-k="${products.indexOf(p)}"><span class="pg-thumb" style="--spool-bg:${escapeHtml(colorBg(entryRow(p)))}"${p.img_src ? ` data-zoom="${escapeHtml(cdnImg(p.img_src, ZOOM_PX))}"` : ""}>`
      + (p.img_src ? `<img src="${escapeHtml(cdnImg(p.img_src, 56))}" alt="" width="56" height="56" loading="lazy" decoding="async">` : "")
      + `</span><span class="pg-ptxt"><b>${escapeHtml(p.title)}</b><small>${escapeHtml([p.brand, p.material, p.measure].filter(Boolean).join(" · "))}</small></span></button></li>`).join("")
      + (hits.length > 60 ? `<li class="pg-muted">${T.more.replace("{n}", hits.length - 60)}</li>` : "")
      + (!hits.length ? `<li class="pg-muted">${T.no_match}</li>` : "");
  }
  function showProduct(entry) {
    const card = $(".pg-product");
    card.hidden = false;
    card.querySelector("img").src = cdnImg(entry.img_src, 72);
    const frame = card.querySelector(".pg-thumb");
    frame.style.setProperty("--spool-bg", colorBg(entryRow(entry)));
    if (entry.img_src) frame.dataset.zoom = cdnImg(entry.img_src, ZOOM_PX); else delete frame.dataset.zoom;
    card.querySelector("img").alt = entry.title || "";
    card.querySelector(".pg-ptitle").textContent = `${entry.brand} · ${entry.title}`;
    card.querySelector(".pg-pmeta").textContent = [entry.material, entry.measure, entry.sku, entry.barcode].filter(Boolean).join(" · ");
    current = applyCommon(fromCatalog(entry));
    render();
  }

  /* ── Custom tab ────────────────────────────────────────────────────────── */
  function readCustom() {
    const v = (id) => $(id).value;
    const num = (id) => Number(v(id)) || 0;
    const ncol = num("#pg-c-ncolors") || 1;
    return applyCommon({
      idTigertag: ID_TIGERTAG, idProduct: MAKER_PRODUCT,
      idMaterial: num("#pg-c-material"), idAspect1: num("#pg-c-aspect1"), idAspect2: num("#pg-c-aspect2"),
      idType: num("#pg-c-type"), idDiameter: num("#pg-c-diameter"), idBrand: num("#pg-c-brand"),
      c1: hexRgb(v("#pg-c-col1")).concat([255]), c2: ncol >= 2 ? hexRgb(v("#pg-c-col2")) : [0, 0, 0], c3: ncol >= 3 ? hexRgb(v("#pg-c-col3")) : [0, 0, 0],
      measure: num("#pg-c-measure"), idUnit: num("#pg-c-unit"), measureAvailable: num("#pg-c-measure"),
      nozzleMin: num("#pg-c-nmin"), nozzleMax: num("#pg-c-nmax"), dryTemp: num("#pg-c-dtemp"), dryTime: num("#pg-c-dtime"),
      bedMin: num("#pg-c-bmin"), bedMax: num("#pg-c-bmax"), timestamp: current ? current.timestamp : nowTs(),
      tdRaw: Math.round(Number(v("#pg-c-td")) * 10) || 0, message: v("#pg-c-msg"), signature: null,
    });
  }
  function onMaterial() {
    const m = materials.find((x) => String(x.id) === $("#pg-c-material").value);
    const r = m && m.recommended;
    if (r) {
      $("#pg-c-nmin").value = r.nozzleTempMin || 0; $("#pg-c-nmax").value = r.nozzleTempMax || 0;
      $("#pg-c-dtemp").value = r.dryTemp || 0; $("#pg-c-dtime").value = r.dryTime || 0;
      $("#pg-c-bmin").value = r.bedTempMin || 0; $("#pg-c-bmax").value = r.bedTempMax || 0;
    }
    if (m && m.product_type_id) $("#pg-c-type").value = m.product_type_id;
    current = readCustom(); render();
  }

  /* ── Common controls: twin tags and remaining quantity ─────────────────── */
  function applyCommon(f) {
    const twin = $("#pg-twin").value;            // "0", "1" (single), "1/2", "2/2"
    if (twin === "1") { f.tagCount = 1; f.tagIndex = 1; }
    else if (twin === "1/2") { f.tagCount = 2; f.tagIndex = 1; }
    else if (twin === "2/2") { f.tagCount = 2; f.tagIndex = 2; }
    else { f.tagCount = 0; f.tagIndex = 0; }
    const pct = Number($("#pg-left").value);
    f.measureAvailable = Math.round(f.measure * pct / 100);
    $("#pg-left-out").textContent = pct + " %";
    return f;
  }
  function onCommon() {
    if (!current) return;
    if (mode === "custom") current = readCustom();
    else if (current.entry) current = applyCommon(fromCatalog(current.entry));
    else current = applyCommon(current);
    current.timestamp = current.timestamp || nowTs();
    render();
  }

  /* ── Decode tab ────────────────────────────────────────────────────────── */
  function decodeHex(text) {
    const hex = text.replace(/0x/gi, "").replace(/[^0-9a-f]/gi, "");
    if (!hex || hex.length % 2) return show(T.bad_hex);
    let b = new Uint8Array(hex.match(/../g).map((h) => parseInt(h, 16)));
    if (b.length === 180) b = b.slice(16, 160);         // full dump: user pages start at page 4
    if (b.length !== 80 && b.length !== 144) return show(T.bad_len.replace("{n}", b.length));
    current = decode(b); show(""); render();
    function show(msg) { $(".pg-error").textContent = msg; }
  }

  /* ── Wiring ────────────────────────────────────────────────────────────── */
  let mode = "catalogue";
  function setMode(m) {
    mode = m;
    root.querySelectorAll(".pg-tab").forEach((b) => b.setAttribute("aria-selected", String(b.dataset.mode === m)));
    root.querySelectorAll(".pg-panel").forEach((p) => { p.hidden = p.dataset.mode !== m; });
    root.querySelector(".pg-common").hidden = m === "decode";
    if (m === "custom") { current = readCustom(); render(); }
  }

  function wire() {
    root.querySelectorAll(".pg-tab").forEach((b) => b.addEventListener("click", () => setMode(b.dataset.mode)));
    $("#pg-cat-brand").addEventListener("change", onBrand);
    $("#pg-cat-search").addEventListener("input", listProducts);
    $("#pg-cat-list").addEventListener("click", (e) => {
      const b = e.target.closest("button[data-k]"); if (b) showProduct(products[Number(b.dataset.k)]);
    });
    root.querySelectorAll(".pg-panel[data-mode=custom] input, .pg-panel[data-mode=custom] select").forEach((el) =>
      el.addEventListener(el.id === "pg-c-material" ? "change" : "input", el.id === "pg-c-material" ? onMaterial : () => { current = readCustom(); render(); }));
    $("#pg-twin").addEventListener("change", onCommon);
    $("#pg-left").addEventListener("input", onCommon);
    $("#pg-decode-btn").addEventListener("click", () => decodeHex($("#pg-decode-in").value));
    $("#pg-file").addEventListener("change", async (e) => {
      const file = e.target.files[0]; if (!file) return;
      const buf = new Uint8Array(await file.arrayBuffer());
      $("#pg-decode-in").value = Array.from(buf, (x) => x.toString(16).padStart(2, "0")).join(" ");
      decodeHex($("#pg-decode-in").value);
    });
    root.addEventListener("click", (e) => {
      const el = e.target.closest("[data-f]"); if (el && root.contains(el)) select(Number(el.dataset.f));
    });
    $("#pg-copy").addEventListener("click", async () => {
      try { await navigator.clipboard.writeText($(".pg-hex").value); flash($("#pg-copy"), T.copied); } catch (e) { $(".pg-hex").select(); }
    });
    $("#pg-download").addEventListener("click", () => {
      const bytes = encode(current);
      const a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([bytes], { type: "application/octet-stream" }));
      a.download = "tigertag-" + (current.idProduct === MAKER_PRODUCT ? "custom" : current.idProduct) + ".bin";
      document.body.appendChild(a); a.click(); a.remove();
    });
    root.querySelectorAll("[data-example]").forEach((b) => b.addEventListener("click", () => example(b.dataset.example)));
  }
  function flash(btn, text) { const t = btn.textContent; btn.textContent = text; setTimeout(() => { btn.textContent = t; }, 1400); }

  function example(name) {
    if (name === "twin") { $("#pg-twin").value = $("#pg-twin").value === "1/2" ? "2/2" : "1/2"; onCommon(); select(FIELDS.findIndex((f) => f.key === "tag_info")); }
  }

  /* The codec, for anyone curious in the browser console (and for the parity tests). */
  window.TigerTagPlayground = { encode, decode, fromCatalog, fields: FIELDS };

  async function start() {
    wire();
    try { await loadTables(); } catch (e) { $(".pg-error").textContent = T.load_error; }
    $("#pg-c-material").value = String(DEFAULT_PRODUCT.RFID_Data.id_material);
    $("#pg-c-brand").value = String(DEFAULT_PRODUCT.RFID_Data.id_brand);
    $("#pg-c-unit").value = "21";                        // grams
    $("#pg-c-diameter").value = String(DEFAULT_PRODUCT.RFID_Data.data1 || 56);   // 1.75 mm
    onMaterial();
    setMode("catalogue");
    showProduct(DEFAULT_PRODUCT);
    previous = null; render();
    $(".pg-explain").textContent = T.pick_byte;
  }
  start();
})();
