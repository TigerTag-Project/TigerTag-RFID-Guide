# TigerTag RFID Tag Guide

## 1. Overview

This document defines the data structure and format used in TigerTag-compatible RFID chips embedded in 3D printing filament spools. Unlike closed formats, TigerTag is **100% offline**, **open-source**, and **brand-neutral**, ensuring long-term stability and compatibility across ecosystems.

TigerTag uses the NTAG213 chip format with a total of 144 bytes of usable memory, structured from page 4 to page 39.

The TigerTag protocol is also compatible with NTAG215 and NTAG216 chips. The binary layout is optimized to fit within the smaller NTAG213 user memory capacity, which ensures that all NTAG21x variants remain compatible.

## 1.1 TigerTag Page Mapping Overview

<img src="Images/TigerTag%20Mapping%20RFID%20NXP213.png" alt="TigerTag Mapping Diagram">

🔒 Pages 24–39 are reserved for optional use of a digital signature (ECDSA-P256 or similar) to verify the origin of Factory TigerTags created by filament manufacturers.


---


## 2. Data Structure: NTAG213 (TigerTag Format)

All multi-byte values are encoded in **big-endian** format.

| Page | Byte(s) | Offset | Size | Field | Type | Description |
| ---- | ------- | ------ | ---- | ----- | ---- | ----------- |
| `0x04` | `0-3` | `+0` | 4 bytes | ID TigerTag | u32 BE | Format identifier (Init / Offline / Cloud) |
| `0x05` | `0-3` | `+4` | 4 bytes | ID Product | u32 BE | `0xFFFFFFFF` for Maker offline, else cloud product ID |
| `0x06` | `0-1` | `+8` | 2 bytes | ID Material | u16 BE | Material type ID (see section 2.3) |
| `0x06` | `2` | `+10` | 1 byte | ID Aspect 1 | u8 | Primary visual aspect (see section 2.5) |
| `0x06` | `3` | `+11` | 1 byte | ID Aspect 2 | u8 | Secondary visual aspect (see section 2.5) |
| `0x07` | `0` | `+12` | 1 byte | ID Type | u8 | `0x8E`=Filament, `0xAD`=Resin (see section 2.6) |
| `0x07` | `1` | `+13` | 1 byte | ID Diameter | u8 | `0x38`=1.75mm, `0xDD`=2.85mm (see section 2.4) |
| `0x07` | `2-3` | `+14` | 2 bytes | ID Brand | u16 BE | Manufacturer/Brand ID (see section 2.7) |
| `0x08` | `0-3` | `+16` | 4 bytes | Color 1 (RGBA) | bytes | Primary color R/G/B/A |
| `0x09` | `0-2` | `+20` | 3 bytes | Measure | u24 BE | Quantity at manufacturing (see ID Unit) |
| `0x09` | `3` | `+23` | 1 byte | ID Unit | u8 | Measurement unit (see section 2.8) |
| `0x0A` | `0-1` | `+24` | 2 bytes | Nozzle Temp Min | u16 BE | Minimum nozzle temperature (°C) |
| `0x0A` | `2-3` | `+26` | 2 bytes | Nozzle Temp Max | u16 BE | Maximum nozzle temperature (°C) |
| `0x0B` | `0` | `+28` | 1 byte | Dry Temp | u8 | Drying temperature (°C) |
| `0x0B` | `1` | `+29` | 1 byte | Dry Time | u8 | Drying duration (hours) |
| `0x0B` | `2` | `+30` | 1 byte | Bed Temp Min | u8 | Minimum bed temperature (°C) |
| `0x0B` | `3` | `+31` | 1 byte | Bed Temp Max | u8 | Maximum bed temperature (°C) |
| `0x0C` | `0-3` | `+32` | 4 bytes | Twin Tag ID & Timestamp | u32 BE | Seconds since 2000-01-01 GMT + twin tag pairing ID (see section 2.9) |
| `0x0D` | `0-2` | `+36` | 3 bytes | Color 2 (RGB) | bytes | Secondary color R/G/B |
| `0x0D` | `3` | `+39` | 1 byte | Reserved | u8 | Must be `0x00` |
| `0x0E` | `0-2` | `+40` | 3 bytes | Color 3 (RGB) | bytes | Tertiary color R/G/B |
| `0x0E` | `3` | `+43` | 1 byte | Reserved | u8 | Must be `0x00` |
| `0x0F` | `0-1` | `+44` | 2 bytes | TD (HueForge) | u16 BE | HueForge Transmission Distance × 10 (see section 2.10) |
| `0x0F` | `2-3` | `+46` | 2 bytes | Reserved | u16 | Must be `0x0000` |
| `0x10`-`0x16` | all | `+48` | 28 bytes | Custom Message | UTF-8 | Free text up to 28 bytes (emoji allowed) |
| `0x17` | `0-2` | `+76` | 3 bytes | Measure Available | u24 BE | Remaining quantity (updated by Tiger Scale) |
| `0x17` | `3` | `+79` | 1 byte | Reserved | u8 | Must be `0x00` |
| `0x18`-`0x1F` | all | `+80` | 32 bytes | Signature R (ECDSA) | bytes | ECDSA signature part r (optional, see section 3) |
| `0x20`-`0x27` | all | `+112` | 32 bytes | Signature S (ECDSA) | bytes | ECDSA signature part s (optional, see section 3) |

> **Capacity check** : 80 bytes user data (pages `0x04`-`0x17`) + 64 bytes signature (pages `0x18`-`0x27`) = **144 bytes** = full NTAG213 user memory capacity.
>
> **Implementer's note** : the page/byte/offset columns above are normative. Any parser MUST use these exact offsets. The visual mapping in `Images/TigerTag Mapping RFID NXP213.png` is provided for human reference and matches this table.

---


## 2.0 Database Last Update

Sidecar metadata file that exposes the **server-side last-modification timestamp** of every reference dataset listed below (sections 2.1, 2.3–2.8). Useful for cache invalidation: clients can fetch this small file first and only re-download the JSON references whose timestamp has changed since their last sync.

**GitHub Json**  
<a href="https://github.com/TigerTag-Project/TigerTag-RFID-Guide/blob/main/database/last_update.json" target="_blank">View JSON reference on GitHub</a>

🔗 Raw JSON link: https://raw.githubusercontent.com/TigerTag-Project/TigerTag-RFID-Guide/main/database/last_update.json

**API Link:**  
<a href="https://api.tigertag.io/api:tigertag/all/last_update" target="_blank">https://api.tigertag.io/api:tigertag/all/last_update</a>

**Format:** JSON object — one entry per dataset, value is a Unix epoch in **milliseconds** (UTC).

**Example response** *(comments shown for clarity — the real API returns plain JSON)*:
```jsonc
{
  "versions":           1763073059935,  // 2025-11-13 22:30:59 UTC
  "types":              1777884684291,  // 2026-05-04 08:51:24 UTC
  "brands":             1777885837902,  // 2026-05-04 09:10:37 UTC
  "filament_diameters": 1777895560487,  // 2026-05-04 11:52:40 UTC
  "filament_materials": 1777972858568,  // 2026-05-05 09:20:58 UTC
  "aspects":            1777894570720,  // 2026-05-04 11:36:10 UTC
  "measure_units":      1777896731691   // 2026-05-04 12:12:11 UTC
}
```

**Decoding a timestamp:**
- JavaScript: `new Date(1763073059935).toISOString()` → `"2025-11-13T22:30:59.935Z"`
- Python: `datetime.fromtimestamp(1763073059935 / 1000, tz=timezone.utc)`

**Key mapping:**
- `versions` → `id_version.json`
- `types` → `id_type.json`
- `brands` → `id_brand.json`
- `filament_diameters` → `id_diameter.json`
- `filament_materials` → `id_material.json`
- `aspects` → `id_aspect.json`
- `measure_units` → `id_measure_unit.json`

**Reference implementations:** ready-to-run Python scripts implementing the smart-diff sync described above are available in [`Sample code/`](Sample%20code/):

- [`sync_id_database_api.py`](Sample%20code/sync_id_database_api.py) — live TigerTag API (real-time freshness).
- [`sync_id_database_github.py`](Sample%20code/sync_id_database_github.py) — GitHub mirror (auto-synced every 6 h, ~6 h stale, no API traffic).
- [`sync_id_database_api_or_github.py`](Sample%20code/sync_id_database_api_or_github.py) — API primary with automatic GitHub fallback when the API is unreachable.

Drop one of these next to where you want the JSON files and run it — first run downloads everything, subsequent runs are no-ops when nothing has changed server-side.

---

## 2.1 ID TigerTag

**GitHub Json**  
<a href="https://github.com/TigerTag-Project/TigerTag-RFID-Guide/blob/main/database/id_version.json" target="_blank">View JSON reference on GitHub</a>

🔗 Raw JSON link: https://raw.githubusercontent.com/TigerTag-Project/TigerTag-RFID-Guide/main/database/id_version.json

**API Link:**  
<a href="https://api.tigertag.io/api:tigertag/version/get/all" target="_blank">https://api.tigertag.io/api:tigertag/version/get/all</a>

**Examples:**  
- `0x6C41A2E1` = `1816240865` → TigerTag Init (Initialized)  
- `0x5BF59264` = `1542820452` → TigerTag (100% Offline)  
- `0xBC0FCB97` = `3155151767` → TigerTag+ (100% Offline + Optional Cloud)

---

## 2.2 ID Product

**API Link:**  
<a href="https://api.tigertag.io/api:tigertag/product/get?uid=$UID_Ntag213&product_id=$Id_Products" target="_blank">https://api.tigertag.io/api:tigertag/product/get?uid=$UID_Ntag213&product_id=$Id_Products</a>

**Example:**  
<a href="https://api.tigertag.io/api:tigertag/product/get?uid=123456789&product_id=10" target="_blank">https://api.tigertag.io/api:tigertag/product/get?uid=123456789&product_id=10</a>

- `0x00000000` = `0` → Reserved (Init / blank product)
- `0xFFFFFFFF` = `4294967295` → Reserved for all TigerTag (Offline)
- `0x00000001`–`0xFFFFFFFE` = `1–4294967294` → TigerTag+ Product IDs (Offline + Cloud)

---

## 2.3 ID Material

**GitHub Json**  
<a href="https://github.com/TigerTag-Project/TigerTag-RFID-Guide/blob/main/database/id_material.json" target="_blank">View JSON reference on GitHub</a>

🔗 Raw JSON link: https://raw.githubusercontent.com/TigerTag-Project/TigerTag-RFID-Guide/main/database/id_material.json

**API Link:**  
<a href="https://api.tigertag.io/api:tigertag/material/get/all" target="_blank">https://api.tigertag.io/api:tigertag/material/get/all</a>

**Examples:**  
- `0x954B` = `38219` → PLA  
- `0x6025` = `24613` → PLA High Speed  
- `0x5042` = `20562` → ABS  
- `0xBF92` = `49074` → ABS-GF  
- etc.

---

## 2.4 ID Diameter

**GitHub Json**  
<a href="https://github.com/TigerTag-Project/TigerTag-RFID-Guide/blob/main/database/id_diameter.json" target="_blank">View JSON reference on GitHub</a>

🔗 Raw JSON link: https://raw.githubusercontent.com/TigerTag-Project/TigerTag-RFID-Guide/main/database/id_diameter.json

**API Link:**  
<a href="https://api.tigertag.io/api:tigertag/diameter/filament/get/all" target="_blank">https://api.tigertag.io/api:tigertag/diameter/filament/get/all</a>

**Examples:**  
- `0x38` = `56` → 1.75mm  
- `0xDD` = `221` → 2.85mm

---

## 2.5 ID Aspect 1 & 2
**GitHub Json**
<br><a href="https://github.com/TigerTag-Project/TigerTag-RFID-Guide/blob/main/database/id_aspect.json" target="_blank">View JSON reference on GitHub</a>

🔗 Raw JSON link: https://raw.githubusercontent.com/TigerTag-Project/TigerTag-RFID-Guide/main/database/id_aspect.json

**API Link:**  
<a href="https://api.tigertag.io/api:tigertag/aspect/get/all" target="_blank">https://api.tigertag.io/api:tigertag/aspect/get/all</a>


**Examples:**  
- `0x15` = `21` → Clear  
- `0x5C` = `92` → Silk  
- `0x68` = `104` → Basix  
- `0x7B` = `123` → Wood  
- etc.

---

## 2.6 ID Type
**GitHub Json**  
<a href="https://github.com/TigerTag-Project/TigerTag-RFID-Guide/blob/main/database/id_type.json" target="_blank">View JSON reference on GitHub</a>

🔗 Raw JSON link: https://raw.githubusercontent.com/TigerTag-Project/TigerTag-RFID-Guide/main/database/id_type.json

**API Link:**  
<a href="https://api.tigertag.io/api:tigertag/type/get/all" target="_blank">https://api.tigertag.io/api:tigertag/type/get/all</a>

**Examples:**  
- `0x8E` = `142` → Filament  
- `0xAD` = `173` → Resin

---

## 2.7 ID Brand

**GitHub Json**  
<a href="https://github.com/TigerTag-Project/TigerTag-RFID-Guide/blob/main/database/id_brand.json" target="_blank">View JSON reference on GitHub</a>

🔗 Raw JSON link: https://raw.githubusercontent.com/TigerTag-Project/TigerTag-RFID-Guide/main/database/id_brand.json

**API Link:**  
<a href="https://api.tigertag.io/api:tigertag/brand/get/all" target="_blank">https://api.tigertag.io/api:tigertag/brand/get/all</a>


**Examples:**  
- `0xC5DC` = `50652` → Polymaker  
- `0x8933` = `35123` → Bambu Lab  
- `0x694C` = `26956` → Creality  
- `0x4E19` = `19961` → Rosa3D  
- `0xBBFA` = `48058` → 3DXtech  
- `0xBBDA` = `48026` → eSun  
- `0xBE94` = `48788` → R3D  
- `0xCA91` = `51857` → Sunlu  
- etc.

---

## 2.8 ID Unit

**GitHub Json**  
<a href="https://github.com/TigerTag-Project/TigerTag-RFID-Guide/blob/main/database/id_measure_unit.json" target="_blank">View JSON reference on GitHub</a>

🔗 Raw JSON link: https://raw.githubusercontent.com/TigerTag-Project/TigerTag-RFID-Guide/main/database/id_measure_unit.json

**API Link:**  
<a href="https://api.tigertag.io/api:tigertag/measure_unit/get/all" target="_blank">https://api.tigertag.io/api:tigertag/measure_unit/get/all</a>


**Examples:**  
- `0x15` = `21` → g  
- `0x23` = `35` → Kg  
- `0x4F` = `79` → L  
- `0x3E` = `62` → cl  
- etc.


## 2.9 Timestamp & Unique Pairing Identifier

The `Time Stamp` field in the TigerTag format serves a **dual purpose** that adds both traceability and pairing functionality:

## 2.10 Transmission Distance (TD) – HueForge Value

In the TigerTag format, the field `TD` is reserved to store the **HueForge Transmission Distance Value**.  
⚠️ This field is an optical/material parameter used by HueForge for rendering and simulation.

**Purpose:**
- Defines how light passes through or is attenuated by the material in HueForge’s simulation.
- Enables more realistic previews of prints, especially for lithophanes or color-sensitive layers.

**Encoding:**
- Length: **2 bytes** (unsigned, big-endian)
- TD : **value / 10**
- Valid range: **0.1–100.0** (encoded **10–1000**); values outside this range are invalid

**Examples:**
- `0x0000` → Undefined (no HueForge TD specified)
- `0x0001` = 1 → **0.1** (minimum allowed) = Opaque
- `0x00E6` = 230 → **23.0**
- `0x03E8` = 1000 → **100.0** (maximum allowed) = Translucent

**Identification / Measurement Tools:**
- Users can determine a material’s HueForge TD using a **TD1S** device.
- TD1S hardware (AJAX TD1S V1.0) available 
    - Atome3D.com — https://www.atome3d.com/products/biqu-ajax-td1s-v1-0
    - Tigertag.io : https://tigertag.io/fr/products/biqu-ajax-td1s-v1-0

### 1. Manufacturing Timestamp
This 4-byte field stores the number of seconds elapsed since 01/01/2000 GMT, providing a reliable, encoded date of fabrication for the spool. This information can be decoded by any compliant reader or software to determine when the filament was produced or packaged.

### 2. Twin Tag Linking (Left & Right Tags)
In addition to tracking production time, the `Time Stamp` acts as a **spool pairing identifier**. When two TigerTag RFID chips are written simultaneously for the left and right sides of the same spool, they receive the exact same timestamp value.

This shared value enables:
- Identifying both tags as part of the same spool.
- Supporting redundancy: if one tag fails or is unreadable, the twin can still provide valid metadata.
- Visual matching in user interfaces or spool management systems (e.g. “Left/Right tag matched” indicators).

🧠 Think of the `Time Stamp` as a **"twin tag ID"** in addition to being a clock — a clever way to bind two tags using time as the key.



---

## 3. Verify Signature

### TigerTag Signature Verification – Introduction for Users

TigerTag is a smart RFID-based tagging system used for identifying and authenticating 3D printer filament spools. To ensure the authenticity of a TigerTag, each tag stores a digital signature that proves it was created by a trusted source.

This document explains the verification process in a simple way:

#### 1. What is a Signature?

A digital signature is like a unique stamp made using a private key. Only the original tag maker knows this key, so if the stamp is valid, you can be sure the tag is genuine.

#### 2. What Do We Verify?

To check if the tag is authentic, we combine three parts:
- The tag's unique ID (called UID)
- The header block (block 4)
- An extra data block (block 5)

These are concatenated and hashed using SHA-256.

#### 3. What is Stored on the Tag?

- The UID (read-only and unique per tag)
- Block 4 and Block 5 (standard data for identification)
- A 64-byte signature (split into two parts: r and s), stored in memory pages starting from page 24

#### 4. How Does Verification Work?

1. The tag is scanned.
2. The UID, block 4, and block 5 are read.
3. The 64-byte signature (r + s) is read.
4. The software recreates the message: UID + block4 + block5.
5. This message is hashed using SHA-256.
6. The public key (freely available) is used to verify the hash against the signature.

✅ If everything matches, the tag is declared authentic.

#### Why is this Important?

Without signature verification, anyone could clone a tag. This process protects your supply chain and ensures you're using trusted materials.

#### Still Curious?

- The private key is never shared and only used to sign tags.
- The public key is embedded in the software to verify signatures.
- The ECDSA (Elliptic Curve Digital Signature Algorithm) is the method used here.

🔐 With this system, you get security, authenticity, and peace of mind for every TigerTag spool.
---

## 4. Example: TigerTag - Encoded Rosa3D Red PLA

| Field            | Hex           | Decimal        | Notes                                      |
| ---------------- | ------------- | -------------- | ------------------------------------------ |
| ID TigerTag      | 0x5C15E2E4    | 1542820452     | TigerTag V1.0 (Offline)              |
| Product ID       | 0xFFFFFFFF    | 4294967295     | Maker version, (Always 0xFFFFFFFF)         |
| Material ID      | 0x954B        | 38219          | PLA                                       |
| Aspect1          | 0x68          | 104            | Basic                                     |
| Aspect2          | 0x00          | 0              | (none)                                    |
| Type ID          | 0x8E          | 142            | Filament                                  |
| Diameter ID      | 0x38          | 56             | 1.75 mm                                   |
| Brand ID         | 0x4E19        | 19961          | Rosa3D                                    |
| Color RGBA       | 0xFF0000FF    | 4278190335     | Red                                       |
| Weight           | 0x0003E8      | 1000           | weight value                              |
| Unit ID          | 0x15          | 21             | grams                                     |
| Temp Min         | 0x00C3        | 195            | °C nozzle minimum                         |
| Temp Max         | 0x00E6        | 230            | °C nozzle maximum                         |
| Dry Temp         | 0x32          | 50             | °C                                        |
| Dry Time         | 0x05          | 5              | Time in hours                             |
| Bed Temp Min     | 0x32          | 50             | °C bed minimum                            |
| Bed Temp Max     | 0x3C          | 60             | °C bed maximum                            |
| Timestamp        | 0x66061A5C    | 1711492444     | Encoded as seconds since 01/01/2000 & twin tag ID     |
| Color2 RGB       | 0x00000000    | 0             | Default                                    |
| Color3 RGB       | 0x00000000.   | 0             | Default                                    |
| TD               | 0x0000        | 0             | Default                                    |
| Message          | Starter Red   | Starter Red    | custom user message (28 bytes max, may include emoji) |
| Measure Available | 0x0003E8      | 1000           | remaining quantity                         |
---

## 4.1 Example: TigerTag+ - Encoded Polymaker PolyTerra Arctic Teal

| Field         | Hex Value    | Decimal Value | Notes                                         |
| ------------- | ------------ | ------------- | --------------------------------------------- |
| ID TigerTag   | 0x12C4C408   | 315515176     | TigerTag+ V1.0                             |
| Product ID    | 0x0000000A   | 10            | Online sync enabled product                   |
| Material ID   | 0x954B       | 38219         | PLA                                           |
| Aspect1       | 0x86         | 134           | Matt                                          |
| Aspect2       | 0x00         | 0             | (none)                                        |
| Type ID       | 0x8E         | 142           | Filament                                      |
| Diameter ID   | 0x38         | 56            | 1.75 mm                                       |
| Brand ID      | 0xC5DC       | 50652         | Polymaker                                     |
| Color RGBA    | 0x89D9D9FF   | 2310590719    | Arctic Teal (hex color code to RGBA)          |
| Weight        | 0x0003E8     | 1000          | grams                                         |
| Unit ID       | 0x23         | 35            | Kilograms                                     |
| Temp Min      | 0x00BE       | 190           | °C nozzle minimum                             |
| Temp Max      | 0x00F0       | 240           | °C nozzle maximum                             |
| Dry Temp      | 0x37         | 55            | °C                                            |
| Dry Time      | 0x06         | 6             | Time in hours                                 |
| Bed Temp Min  | 0x23         | 35            | °C bed minimum                                |
| Bed Temp Max  | 0x41         | 65            | °C bed maximum                                |
| Timestamp     | 0x66061E90   | 1711493264    | Encoded as seconds since 01/01/2000           |
| Color2 RGB    | 0x00000000   | 0             | Default                                       |
| Color3 RGB    | 0x00000000   | 0             | Default                                       |
| TD            | 0x0000       | 0             | Default                                       |
| Message       | Private msg  | Private msg   | custom user message (28 bytes max, may include emoji) |
| Measure Available | 0x0003E8     | 1000          | remaining quantity                           |
| Signature R   | A6B3...D7DA1AA | A6B3...D7DA1AA            | 32-byte ECDSA signature part 1 (r), p24–31    |
| Signature S   | 91F4...F8AE29CE| 91F4...F8AE29CE  | 32-byte ECDSA signature part 2 (s), p32–39    |
---
Use the `public_key` together with the UID, block 4, and block 5 to verify the authenticity of a TigerTag. For details, see <a href="#4-verify-signature">Section 4: Verify Signature</a> and the sample code in `verify_signature.py`.

📡 Online Data: To retrieve the full product metadata, send a GET request with both the RFID tag UID and the Product ID.

**Example:**  
<a href="https://api.tigertag.io/api:tigertag/product/get?uid=123456789&product_id=10" target="_blank">https://api.tigertag.io/api:tigertag/product/get?uid=123456789&product_id=10</a>

---

## 4.2 Example: TigerTag Init - Blank Initialization Tag

| Field            | Hex Value    | Decimal Value | Notes                                      |
| ---------------- | ------------ | ------------- | ------------------------------------------ |
| ID TigerTag      | 0x6C46A3C1   | 1816240865    | TigerTag Init                              |
| Product ID       | 0x00000000   | 0             | Default offline value                      |
| Material ID      | 0x0000       | 0             | Not defined                                |
| Aspect1          | 0x00         | 0             | Not defined                                |
| Aspect2          | 0x00         | 0             | Not defined                                |
| Type ID          | 0x00         | 0             | Not defined                                |
| Diameter ID      | 0x00         | 0             | Not defined                                |
| Brand ID         | 0x0000       | 0             | Not defined                                |
| Color1 RGBA      | 0x00000000   | 0             | Default                                    |
| Weight           | 0x000000     | 0             | 0 grams                                    |
| Unit ID          | 0x00         | 0             | Not defined                                |
| Temp Min         | 0x0000       | 0             | °C nozzle minimum                          |
| Temp Max         | 0x0000       | 0             | °C nozzle maximum                          |
| Dry Temp         | 0x00         | 0             | °C                                         |
| Dry Time         | 0x00         | 0             | Time in hours                              |
| Bed Temp Min     | 0x00         | 0             | °C bed minimum                             |
| Bed Temp Max     | 0x00         | 0             | °C bed maximum                             |
| Timestamp        | 0x00000000   | 0             | No timestamp                               |
| Color2 RGB       | 0x00000000   | 0             | Default                                    |
| Color3 RGB       | 0x00000000   | 0             | Default                                    |
| TD               | 0x0000       | 0             | Default                                    |
| Message          | Unprogrammed | Unprogrammed  | Placeholder message (28 bytes max)         |
| Measure Available | 0x000000     | 0             | remaining quantity                          |

## 5. Commercial License & Trademark Usage

TigerTag™ is a registered trademark of TigerTag Corp.

TigerTag is provided under a dual-licensing model:

---

### A. TigerTag OEM Commercial License

The TigerTag Commercial License is intended for OEM (Original Equipment Manufacturer) use cases. This license is applicable when you plan to integrate TigerTag technology into products or systems distributed commercially.

**OEM Use Cases Include (but are not limited to):**
- Embedding TigerTag chips into 3D filament spools or packaging.
- Integrating TigerTag software in commercial slicers, printers, or platforms.
- Using TigerTag as part of a branded or white-labeled product offering.

**Key Points:**
- A license fee may apply and will be agreed between parties.
- This license allows binary redistribution, branding, and commercial deployment.
- Licensee may create derivative works for internal use but may not redistribute them without consent.

Please contact us at [tigertag@tigertag.io](mailto:tigertag@tigertag.io) for licensing terms and commercial integration options.

---

### B. Open-Source Use (GPLv3 License)

If you are a hobbyist, developer, or non-commercial user, you may use TigerTag under the terms of the **GNU General Public License v3.0 (GPLv3)** for personal or open-source projects.

**GPLv3 License Summary:**
- Free use in non-commercial and open-source projects.
- Full source code must be made available if redistributed or modified.
- Any derivative works must also be licensed under GPLv3.
- No warranty or liability is provided.

For the full license text, see <a href="https://www.gnu.org/licenses/gpl-3.0.txt" target="_blank">https://www.gnu.org/licenses/gpl-3.0.txt</a>

---

### C. Logo Usage Guidelines

TigerTag branding and logo are protected by copyright and must follow the usage policy:

- ✅ Permitted for use in apps or documentation referencing TigerTag compatibility.
- ❌ Not permitted in product or app names (e.g., do not name your app "TigerTag Reader").
- ❌ Not allowed for deceptive marketing or implying affiliation without permission.
- 🔄 Logo must remain unmodified and clearly distinguishable.

This policy applies to both GPLv3 and OEM licensees.

---

To request commercial rights, OEM access, or brand guidelines, please contact us directly.

**Contact:** [tigertag@tigertag.io](mailto:tigertag@tigertag.io)

---


## 5.0 Apps & Tools

TigerTag is built around an open protocol and a free public API. Below are the official **TigerTag-Project apps and tools** — all open-source where indicated — that consume that API. For developer references, the protocol specification is the rest of this document; the API is documented at [https://api.tigertag.io/api:tigertag](https://api.tigertag.io/api:tigertag), and the project website is [https://tigertag.io](https://tigertag.io).

## 5.1 TigerTag Studio Manager (Open Source)

Desktop application for **Windows, macOS, and Linux** that manages your 3D-printing filament inventory. It reads RFID spool tags through an ACR122U NFC reader, tracks remaining weight, and surfaces print temperatures, MSDS/TDS links, and product details. Auto-updates via GitHub Releases.

🔗 [TigerTag-Project/TigerTag-Studio-Manager](https://github.com/TigerTag-Project/TigerTag-Studio-Manager) — built with Electron.

## 5.2 Tiger Scale (Open Source)

DIY smart scale (~30 € BoM) that identifies which spool sits on it. Drop a spool with a TigerTag NFC sticker on the platform — the scale reads the tag, weighs the spool, computes the **net filament weight** (subtracting the empty spool), and syncs the result to your TigerTag account in real time. Dual RC522 RFID readers for twin-tag spools, HX711 + 5 kg load cell, OLED display, mobile-friendly web UI served by the ESP32 itself, 9-language UI.

🔗 [TigerTag-Project/Tiger_Scale](https://github.com/TigerTag-Project/Tiger_Scale) — ESP32 / Arduino / PlatformIO, with a one-click [Web Installer](https://tigertag-project.github.io/Tiger_Scale/) (Chrome/Edge).

## 5.3 TigerTag RFID Connect — Mobile Apps (iOS & Android)

The official TigerTag mobile app (iOS and Android) is a **closed-source proof of concept** provided for convenience. It demonstrates how TigerTag tags can be read and written using the open protocol.

However, **any developer or manufacturer is free to build their own applications**—desktop, mobile, or embedded—by following the TigerTag specification.

✅ The protocol is open and documented  
✅ The API and official apps are **free to use** for end users and developers  
🔒 The source code of the mobile app is **not open-source**, but the tools and specs to create your own app are available

The TigerTag mobile app uses only the **free public API** to ensure fair access and maintain a balanced relationship between TigerTag and third-party developers. This guarantees interoperability and prevents vendor lock-in.

For protocol details, refer to the sections above or contact us for technical guidance.

### 📱 Mobile Apps

<img src="https://raw.githubusercontent.com/TigerTag-Project/TigerTag-RFID-Guide/main/Images/TigerTag_RFID_Connect_Apps.png" alt="TigerTag Mobile Apps">

- 🧭 iOS App: [https://apps.apple.com/fr/app/tigertag-rfid-connect/id6745437963](https://apps.apple.com/fr/app/tigertag-rfid-connect/id6745437963)
- 🤖 Android App: [https://play.google.com/store/apps/details?id=com.tigertag.connect](https://play.google.com/store/apps/details?id=com.tigertag.connect)

---

## 6. Community Integrations & Acknowledgments

Third-party projects built on the TigerTag protocol or the public API. These are independent community efforts — they are **not officially maintained or endorsed by TigerTag Project** — and we list them here as a thank-you to their authors for extending the TigerTag ecosystem.

## 6.1 OpenRFID

RFID controller and parsing library for common 3D-printing filament tags, with native support for the **TigerTag** format (alongside OpenSpool, OpenTag3D, and others). Marked by the author as a work in progress.

🔗 [suchmememanyskill/OpenRFID](https://github.com/suchmememanyskill/OpenRFID) — author: [@suchmememanyskill](https://github.com/suchmememanyskill). Python.

## 6.2 Snapmaker U1 Extended Firmware

Custom and repackaged firmware for the **Snapmaker U1** 3D printer, adding debug features (SSH access) and extended capabilities. RFID filament-tag support is provided via an embedded **OpenRFID** module, which is what brings TigerTag parsing to the printer.

🔗 [paxx12-snapmaker-u1/SnapmakerU1-Extended-Firmware](https://github.com/paxx12-snapmaker-u1/SnapmakerU1-Extended-Firmware) — author: [@paxx12](https://github.com/paxx12). Independent of, and not affiliated with, Snapmaker.

## 6.3 TigerTag — Home Assistant Integration

HACS-compatible custom integration that synchronises your TigerTag filament inventory into **Home Assistant**: sensors and number entities per spool, custom Lovelace card, twin-tag deduplication, rack/level/position assignment, optional integration with [ha-bambulab](https://github.com/greghesp/ha-bambulab) to push filament configuration to a Bambu Lab AMS.

🔗 [Kenny3231/TigerTag](https://github.com/Kenny3231/TigerTag) — author: [@Kenny3231](https://github.com/Kenny3231). Per its own README, this is a community project **not officially affiliated with TigerTag Project**.

## 7. Version History

| Version | Date       | Description           | Author        |
| ------- | ---------- | --------------------- | ------------- |
| 1.0     | 2025-06-09 | Initial public format | TigerTag Team |
| 2.0     | 2026-03-11 | Corrected binary memory layout and NTAG213 capacity alignment | TigerTag Team |

---

## 8. Contributions

Want to contribute improvements or integrations? Fork this repository and open a pull request.

For firmware integrations or manufacturer onboarding, contact the TigerTag core team.
