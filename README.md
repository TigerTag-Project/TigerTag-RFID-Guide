# TigerTag RFID Tag Guide

## 1. Overview

This document defines the data structure and format used in TigerTag-compatible RFID chips embedded in 3D printing filament spools. Unlike closed formats, TigerTag is **100% offline**, **open-source**, and **brand-neutral**, ensuring long-term stability and compatibility across ecosystems.

TigerTag uses the NTAG213 chip format with a total of 144 bytes of usable memory, structured from page 4 to page 39.

---

## 2. Data Structure: NTAG213 (TigerTag Format)

| Field             | Length   | Description                                     |
| ----------------- | -------- | ----------------------------------------------- |
| ID TigerTag       | 4 byte   | Format identifier (e.g. Maker : 1542820452)     |
| ID Product        | 4 bytes  | Fixed value (0xFFFFFFFF for Maker version)      |
| ID Material       | 2 byte   | Material Type (e.g. PLA, PETG, ABS...)          |
| ID Diameter       | 1 byte   | 56 = 1.75mm, 221 = 2.85mm                       |
| ID Aspect 1       | 1 byte   | First visual aspect                             |
| ID Aspect 2       | 1 byte   | Second visual aspect                            |
| ID Type           | 1 byte   | Type (e.g. 142 = Filament, 173 = Resin)         |
| ID Brand          | 2 byte   | Manufacturer/Brand ID                           |
| ID Unit           | 1 byte   | Measurement unit (e.g. 21 = grams, 79 = Liter)  |
| Color (RGBA)      | 4 bytes  | Red, Green, Blue, Alpha (1 byte each)           |
| Measure           | 3 byte   | Weight in grams , kilo , litter (e.g 1000 )     |
| Nozzle Temp Min   | 1 byte   | Minimum printing temperature (°C)               |
| Nozzle Temp Max   | 1 byte   | Maximum printing temperature (°C)               |
| Dry Temp          | 1 byte   | Drying temperature (°C)                         |
| Dry Time          | 1 byte   | Drying duration in hours                        |
| Bed Temp Min      | 1 byte   | Min bed temp (°C), optional                     |
| Bed Temp Max      | 1 byte   | Max bed temp (°C), optional                     |
| Time Stamp        | 4 bytes  | Seconds since 01/01/2000 GMT                    |
| Reserved          | 12 bytes | Reserved for future use                         |
| Emoji             | 4 bytes  | UTF-8 Emoji (if supported)                      |
| Custom Message    | 28 bytes | Free text (UTF-8 or ASCII, max 28 chars)        |
| Signature (ECDSA) | 64 bytes | Optional digital signature to authenticate data |

---

```md
## 2.1 ID TigerTag

**API Link:**  
[https://api.tigertag.io/api:tigertag/version/get/all](https://api.tigertag.io/api:tigertag/version/get/all)

**Examples:**  
- `1816240865` = TigerTag Init (Initialized)  
- `1542820452` = TigerTag Maker V1.0 (Offline)  
- `315515176`  = TigerTag Pro V1.0 (Hybrid Offline & Online Mode)

---

## 2.2 ID Product

**API Link:**  
`https://api.tigertag.io/api:tigertag/product/get?uid=$UID_Ntag213&product_id=$Id_Products`

**Example:**  
`https://api.tigertag.io/api:tigertag/product/get?uid=123456789&product_id=10`

**Values:**  
- `4294967295` = TigerTag Maker (Offline)  
- `XXXXX` = TigerTag Hybrid (Offline & Online Mode)

---

## 2.3 ID Material

**API Link:**  
[https://api.tigertag.io/api:tigertag/material/filament/get/all](https://api.tigertag.io/api:tigertag/material/filament/get/all)

**Examples:**  
- `38219` = PLA  
- `24629` = PLA High Speed  
- `20562` = ABS  
- `49074` = ABS-GF  
- etc.

---

## 2.4 ID Diameter

**API Link:**  
[https://api.tigertag.io/api:tigertag/diameter/filament/get/all](https://api.tigertag.io/api:tigertag/diameter/filament/get/all)

**Examples:**  
- `56` = 1.75mm  
- `221` = 2.85mm

---

## 2.5 ID Aspect 1 & 2

**API Link:**  
[https://api.tigertag.io/api:tigertag/aspect/get/all](https://api.tigertag.io/api:tigertag/aspect/get/all)

**Examples:**  
- `21` = Clear  
- `92` = Silk  
- `104` = Basix  
- `123` = Wood  
- etc.

---

## 2.6 ID Type

**API Link:**  
[https://api.tigertag.io/api:tigertag/type/get/all](https://api.tigertag.io/api:tigertag/type/get/all)

**Examples:**  
- `142` = Filament  
- `173` = Resin

---

## 2.7 ID Brand

**API Link:**  
[https://api.tigertag.io/api:tigertag/brand/get/all](https://api.tigertag.io/api:tigertag/brand/get/all)

**Examples:**  
- `50604` = Polymaker  
- `35123` = Bambu Lab  
- `26956` = Creality  
- `26956` = Rosa3D  
- `39652` = 3DXtech  
- `47930` = eSun  
- `48804` = R3D  
- `51857` = Sunlu  
- etc.

---

## 2.8 ID Unit

**API Link:**  
[https://api.tigertag.io/api:tigertag/measure_unit/get/all](https://api.tigertag.io/api:tigertag/measure_unit/get/all)

**Examples:**  
- `21` = g  
- `35` = Kg  
- `79` = L  
- `62` = cl  
- etc.
```

## 3. Page Mapping Overview

![TigerTag Mapping Diagram](Images/TigerTag%20Mapping%20RFID%20NXP213.png)

🔒 Pages 24–39 are reserved for optional use of a digital signature (ECDSA-P256 or similar) to verify the origin of Factory TigerTags created by filament manufacturers.

---

## 4. Verify Signature

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

## 5. Example: TigerTag Maker - Encoded Rosa3D Red PLA

| Field            | Value          | Notes                                      |
| ---------------- | -------------- | ------------------------------------------ |
| ID TigerTag      | 0x5C15E2E4     | TigerTag Maker V1.0 (Offline) = 1542820452 |
| Product ID       | 0xFFFFFFFF     | Maker version, (Always 0xFFFFFFFF)         |
| Material ID      | 38219          | PLA                                        |
| Diameter ID      | 56             | 1.75 mm                                    |
| Aspect1          | 104            | Basic                                      |
| Aspect2          | 0              | (none)                                     |
| Type ID          | 142            | Filament                                   |
| Brand ID         | 19961          | Rosa3D                                     |
| Unit ID          | 21             | grams                                      |
| Color RGBA       | FF0000FF       | Red                                        |
| Weight           | 1000           | weight value                               |
| Temp Min         | 195            | °C nozzle minimum                          |
| Temp Max         | 230            | °C nozzle maximum                          |
| Dry Temp         | 50             | °C                                         |
| Dry Time         | 5              | Time in hours                              |
| Bed Temp Min     | 50             | °C bed minimum                             |
| Bed Temp Max     | 60             | °C bed maximum                             |
| Timestamp        | 0x66061A5C     | Encoded as seconds since 01/01/2000        |
| Emoji            | 😀             | custom user UTF-8 encoded emoji (4 bytes)  |
| Message          | Starter Red    | custom user message                        |


---

## 5.1 Example: TigerTag Pro - Encoded Polymaker PolyTerra Arctic Teal

| Field            | Value          | Notes                                         |
| ---------------- | -------------- | --------------------------------------------- |
| ID TigerTag      | 0x12C4C408     | TigerTag Pro V1.0  = 3155151767               |
| Product ID       | 10             | Online sync enabled product                   |
| Material ID      | 38219          | PLA                                           |
| Diameter ID      | 56             | 1.75 mm                                       |
| Aspect1          | 134            | Matt                                          |
| Aspect2          | 0              | (none)                                        |
| Type ID          | 142            | Filament                                      |
| Brand ID         | 50604          | Polymaker                                     |
| Unit ID          | 35             | Kilograms                                     |
| Color RGBA       | 89D9D9FF       | Arctic Teal (hex color code to RGBA)          |
| Weight           | 1000           | grams                                         |
| Temp Min         | 190            | °C nozzle minimum                             |
| Temp Max         | 240            | °C nozzle maximum                             |
| Dry Temp         | 55             | °C                                            |
| Dry Time         | 6              | Time in hours                                 |
| Bed Temp Min     | 35             | °C bed minimum                                |
| Bed Temp Max     | 65             | °C bed maximum                                |
| Timestamp        | 0x66061E90     | Encoded as seconds since 01/01/2000           |
| Emoji            | 🌱             | custom user UTF-8 encoded emoji (4 bytes)     |
| Message          | Private msg    | custom user message                           |
| Signature R      | A6B3...D7DA1AA | 32-byte ECDSA signature part 1 (r), p24–31    |
| Signature S      | 91F4...F8AE29CE| 32-byte ECDSA signature part 2 (s), p32–39    |
---
Use the `public_key` together with the UID, block 4, and block 5 to verify the authenticity of a TigerTag. For details, see [Section 4: Verify Signature](#4-verify-signature) and the sample code in `verify_signature.py`.

📡 Online Data: To retrieve the full product metadata, send a GET request with both the RFID tag UID and the Product ID.

**Example:**  
[`https://api.tigertag.io/api:tigertag/product/get?uid=123456789&product_id=10`](https://api.tigertag.io/api:tigertag/product/get?uid=123456789&product_id=10)

---

## 5.2 Example: TigerTag Init - Blank Initialization Tag

| Field            | Value          | Notes                                      |
| ---------------- | -------------- | ------------------------------------------ |
| ID TigerTag      | 0x6C46A3C1     | TigerTag Init = 1816240865                 |
| Product ID       | 0              | Default offline value                      |
| Material ID      | 0              | Not defined                                |
| Diameter ID      | 0              | Not defined                                |
| Aspect1          | 0              | Not defined                                |
| Aspect2          | 0              | Not defined                                |
| Type ID          | 0              | Not defined                                |
| Brand ID         | 0              | Not defined                                |
| Unit ID          | 0              | Not defined                                |
| Color RGBA       | 00000000       | Default                                     |
| Weight           | 0              | 0 grams                                    |
| Temp Min         | 0              | °C nozzle minimum                          |
| Temp Max         | 0              | °C nozzle maximum                          |
| Dry Temp         | 0              | °C                                         |
| Dry Time         | 0              | Time in hours                              |
| Bed Temp Min     | 0              | °C bed minimum                             |
| Bed Temp Max     | 0              | °C bed maximum                             |
| Timestamp        | 0x00000000     | No timestamp                               |
| Emoji            | 0x00000000     | Default placeholder                        |
| Message          | Unprogrammed   | Placeholder message                        |

## 6. Trademark & Licensing

TigerTag™ is a registered trademark of TigerTag Corp.

You may use the protocol and logo **freely inside your application**, as long as:

* You **do not name your app or hardware 'TigerTag'**
* You clearly state compatibility only, not affiliation
* You follow logo usage guidelines provided in `/branding`

Contact: [tigertag@tigertag.io](mailto:tigertag@tigertag.io)

**License:** MIT (see LICENSE)

---

## 7. Version History

| Version | Date       | Description           | Author        |
| ------- | ---------- | --------------------- | ------------- |
| 1.0     | 2025-06-09 | Initial public format | TigerTag Team |

---

## 8. Contributions

Want to contribute improvements or integrations? Fork this repository and open a pull request.

For firmware integrations or manufacturer onboarding, contact the TigerTag core team.
