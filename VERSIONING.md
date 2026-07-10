# Versioning

TigerTag has **two independent version numbers**, and conflating them causes bugs. This
page explains what each one is, who bumps it, and how they relate.

| | Specification version | Tag format version |
|---|---|---|
| **What it versions** | This document — the prose, the diagrams, the examples | The bytes on the chip |
| **Where it lives** | `README.md`, version-history table, the badge | [`database/id_version.json`](database/id_version.json) |
| **Current value** | `2.1` | `0.0`, `1.0` |
| **Read by** | Humans | Readers, at runtime, from the chip |
| **Changes when** | The document changes | The on-chip layout or key changes |

A reader **never** parses the specification version. It reads the `id_tigertag` field from
the chip, looks it up in `id_version.json`, and learns which layout to expect and which
public key to verify against.

---

## 1. Specification version

The version of *this document*. It follows semantic versioning, applied to the protocol as
a contract:

- **Major** (`2.0` → `3.0`) — an existing conforming reader would misinterpret a chip
  written under the new spec. A field moved, an encoding changed, a byte order flipped.
  A major bump requires a new tag format version (§2) so that old readers can detect and
  refuse chips they cannot parse.
- **Minor** (`2.0` → `2.1`) — new material that does not change how an existing reader
  behaves on an existing chip. A previously reserved byte given a meaning, a new optional
  field in unused space, new documentation of behaviour that was always true.
- **Patch** (`2.1` → `2.1.1`) — the protocol did not change. Typos, corrected example hex
  values, clarified wording, new diagrams, translations.

The current specification version is stated in the badge at the top of `README.md` and in
the version-history table in §7. Both must be updated together.

### History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2025-06-09 | Initial public format |
| 2.0 | 2026-03-11 | Corrected binary memory layout and NTAG21x capacity alignment |
| 2.1 | 2026-05-18 | Add UID documentation, system pages layout, fix example hex values |

Note that `2.0` corrected the *documentation* of the layout. Chips in the field were not
re-encoded.

---

## 2. Tag format version

The value written on the chip, in the `id_tigertag` field. It is a `u32` big-endian
identifier, not a human-readable string, and every entry is registered in
[`database/id_version.json`](database/id_version.json):

| `id` | `version` | `name` | `tag` | Signed |
|---|---|---|---|---|
| `0` | `0.0` | RFID Empty | `TIGER_TAG_UNINITIALIZED` | — |
| `1542820452` | `1.0` | TigerTag | `TIGER_TAG_MAKER_V1.0` | Yes |
| `1816240865` | `1.0` | TigerTag Init | `TIGER_TAG_INIT` | Yes |
| `3155151767` | `1.0` | TigerTag+ | `TIGER_TAG_PRO_V1.0` | Yes |

Each signed entry carries the **public key** used to verify chips of that version, in PEM
form, in the `public_key` field. This is the mechanism that makes offline verification
possible: a reader ships with `id_version.json` embedded, reads `id_tigertag` off the chip,
selects the matching key, and verifies. No network.

### Rules

1. **`id_version.json` is append-only.** Chips are physical and long-lived. Removing an
   entry orphans every chip already in the field. Entries are never deleted and their `id`
   values are never reused.
2. **A new entry is required whenever an existing reader would get it wrong.** New layout,
   new key, new signature scheme.
3. **`id` values are opaque.** Do not infer ordering, recency, or capability from the
   numeric value. Look the entry up.
4. **A reader encountering an unknown `id_tigertag` must fail closed** — treat the chip as
   unrecognised, not as unsigned-but-valid. It may be a format from the future.
5. **Key rotation happens by adding a version**, never by editing a key in place. See
   [`SECURITY.md`](SECURITY.md#key-rotation).

### How `id_version.json` is maintained

`database/*.json` is generated from the TigerTag catalogue and synchronised into this
repository automatically by `.github/workflows/sync-database.yml`. **Do not edit it by
hand, and do not send pull requests against it** — see [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## 3. How the two relate

- A **patch or minor** specification bump leaves `id_version.json` untouched.
- A **major** specification bump adds a new entry to `id_version.json`. The old entries
  stay. Chips written before the bump keep working, forever, unchanged.
- A **new tag format version** may be added without a major specification bump — for
  example, to rotate a key while the layout is unchanged. In that case the specification
  takes a minor bump to document the new entry.

Consequently: the specification version tells you *which document you are reading*. It does
not tell you what any given chip contains. Only the chip does.

---

## 4. Changing the specification

Protocol changes arrive as TEPs (TigerTag Enhancement Proposals), not as forks. An accepted
TEP is what triggers a version bump. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

When a TEP is released:

1. `README.md` is updated with the change.
2. The version-history table in `README.md` §7 gains a row.
3. The protocol badge at the top of `README.md` is updated.
4. The table in §1 of this file gains a row.
5. If the on-chip layout or a key changed, a new entry is registered in the TigerTag
   catalogue and appears in `id_version.json` on the next sync.
6. A git tag `spec-vX.Y.Z` is pushed, and a GitHub release is cut against it.

---

## 5. Stability guarantee

The commitment implied by the above, stated plainly:

> A chip written today will be readable by a conforming TigerTag reader indefinitely. Field
> layouts, once released under a tag format version, are never redefined. New capability
> arrives as a new tag format version, not as a redefinition of an old one.

This is the property that makes it safe for a printer manufacturer to burn a TigerTag reader
into firmware that will ship for a decade.
