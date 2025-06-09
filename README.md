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
| ID Material       | 2 byte   | Materail Type (e.g. PLA, PETG, ABS...)          |
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

##2.1 ID TigerTag :

API Link : https://api.tigertag.io/api:tigertag#/version/get_version_get_all

Exemple :

1816240865 = TigerTag Init (Initialized)
1542820452 = TigerTag Maker V1.0 ( Offline )
315515176 = TigerTag Pro V1.0 ( Hybrid Offline & Online Mode )

##2.2 ID Product :

API Link : https://api.tigertag.io/api:tigertag/product/get?uid="$UID_Ntag213"&product_id="$Id_Products"
Exemple : https://api.tigertag.io/api:tigertag/product/get?uid=123456789&product_id=10

Exemple :

4294967295 = TigerTag Maker (Offline)
XXXXX = TigerTag Hybrid ( Offline & Online Mode )

##2.3 ID Material :

API Link : https://api.tigertag.io/api:tigertag/material/filament/get/all

Exemple :

38219 = PLA
24629 = PLA Hight Speed
20562 = ABS
49074 = ABS-GF
etc... 

##2.4 ID Diameter :

API Link : https://api.tigertag.io/api:tigertag/diameter/filament/get/all

Exemple : 
56 = 1.75mm
221 = 2.85mm   

##2.5 ID Aspect 1 & 2 :

API Link : https://api.tigertag.io/api:tigertag/aspect/get/all

Exemple : 
21 : Clear
92 = Silk
104 = Basix
123 = Wood
etc....

##2.6 ID Type :

API Link : https://api.tigertag.io/api:tigertag/type/get/all

142 = Filament
173 = Resin

##2.7 ID Brand :

API Link : https://api.tigertag.io/api:tigertag/brand/get/all

Exemple :

50604 = Polymaker
35123 = Bambu Lab
26956 = Creality
26956 = Rosa3D
39652 = 3DXtech
47930 = eSun
48804 = R3D
51857 = Sunlu
etc...

##2.7 ID Unit :

API Link : https://api.tigertag.io/api:tigertag/measure_unit/get/all

Exemple : 
21 = g
35 = Kg
79 = L
62 = cl
etc....

## 3. Page Mapping Overview

| Page  | Address (Hex) | Content                          |
| ----- | ------------- | -------------------------------- |
| 4     | 0x04–0x05     | ID TigerTag                      |
| 5     | 0x04–0x05     | ID Product                       |
| 6–7   | 0x06–0x07     | Material, Diameter, Aspect, Type |
| 8–9   | 0x08–0x09     | Color + Measure + Temps          |
| 10–11 | 0x0A–0x0B     | Bed Temps + Dry Temps + Unit     |
| 12    | 0x0C          | Timestamp                        |
| 13–15 | 0x0D–0x0F     | Reserved                         |
| 16    | 0x10          | Emoji                            |
| 17–23 | 0x11–0x17     | Custom Message (28 bytes)        |
| 24–39 | 0x18–0x27     | ECDSA Signature (64 bytes)       |

> 🔒 Pages 24–39 are intended for optional use of digital signature (ECDSA-P256 or similar). Signature covers pages 4–23.

---

## 4. Optional: Secure Signature (ECDSA)

TigerTag supports signing tag data to ensure its integrity and authenticity.

* Signature covers raw byte content from pages 4 to 23 (80 bytes).
* ECDSA (P-256) is recommended.
* Signature is stored from pages 24 to 39 (64 bytes).
* Public key can be embedded in firmware, app, or provided via API.

### Use Cases

* Manufacturer-grade anti-fraud
* Authenticity validation during import
* Optional for Maker version (not required)

---

## 5. Example: Encoded Red PLA Tag

| Field        | Value          |
| ------------ | -------------- |
| ID TigerTag  | 0x54           |
| Product ID   | 0xFFFFFFFF     |
| Material ID  | 0x23           |
| Diameter ID  | 0x01           |
| Aspect1      | 0x02           |
| Aspect2      | 0x00           |
| Type ID      | 0x01           |
| Brand ID     | 0x19           |
| Unit ID      | 0x15           |
| Color RGBA   | FF3700FF       |
| Weight       | 0xE8 (1000g)   |
| Temp Min     | 0x38 (56°C)    |
| Temp Max     | 0xC3 (195°C)   |
| Dry Temp     | 0xEB (235°C)   |
| Dry Time     | 0x32 (50h)     |
| Bed Temp Min | 0x28 (40°C)    |
| Bed Temp Max | 0x3C (60°C)    |
| Timestamp    | 0x66061A5C     |
| Emoji        | 😀             |
| Message      | Rainbow Candy  |

---

## 6. Trademark & Licensing

TigerTag™ is a registered trademark of 3D France (Atome3D).

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
