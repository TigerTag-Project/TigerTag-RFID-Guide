# Security Policy

TigerTag's authenticity guarantee rests on a single cryptographic claim:

> A tag carrying a valid TigerTag+ signature can only have been signed by TigerTag Corp,
> and any reader can verify this offline, with no network access.

Anything that weakens that claim is a security vulnerability, and we want to hear about it
before anyone else does.

---

## Reporting a vulnerability

**Do not open a public issue, pull request, or Discord message.**

Report privately, by either route:

1. **GitHub Security Advisory** (preferred) — use
   [Report a vulnerability](https://github.com/TigerTag-Project/TigerTag-RFID-Guide/security/advisories/new)
   on this repository. This creates a private thread visible only to maintainers.
2. **Email** — [security@tigertag.io](mailto:security@tigertag.io), copying
   [tigertag@tigertag.io](mailto:tigertag@tigertag.io).

If you believe the issue is being actively exploited, say so in the first line.

### What to include

- What you found, and what an attacker gains from it
- How to reproduce it — a chip dump, a script, a signature that verifies when it should not
- The spec version and tag format version involved (see [`VERSIONING.md`](VERSIONING.md))
- Whether you have disclosed it anywhere else

You do not need a working exploit. A credible description of a flaw in the signature scheme
is enough.

### What to expect

| Stage | Target |
|---|---|
| Acknowledgement of your report | 48 hours |
| Initial assessment — is it a vulnerability, and how severe | 7 days |
| Fix or mitigation plan communicated to you | 30 days |
| Public disclosure | Coordinated with you, normally after a fix is available |

We will credit you in the advisory unless you ask us not to. We do not currently operate a
paid bounty programme.

---

## In scope

Especially anything touching the signature or key handling:

- **Signature forgery** — producing a tag that verifies against a published public key
  without TigerTag Corp's private key
- **Signature bypass** — causing a reader that follows the specification to accept an
  unsigned or invalidly signed tag as TigerTag+
- **Weakness in the signed message construction** — the signed message is
  `SHA-256(uid[7B] ‖ id_tigertag[4B BE] ‖ id_product[4B BE])`. Collisions, length-extension,
  ambiguity in the concatenation, or any way to make two distinct tags produce the same
  digest are in scope.
- **Key exposure** — a private key, or material sufficient to derive one, present anywhere
  in this repository, in a published artefact, in the API, or in a shipped tool
- **Downgrade attacks** — forcing a reader to treat a TigerTag+ chip as an unsigned one, or
  to select a weaker tag format version
- **Public-key substitution** — any path by which a reader can be induced to verify against
  an attacker-controlled key rather than the ones in
  [`database/id_version.json`](database/id_version.json)
- **Specification defects** that lead a correct implementation into an insecure state.
  A flaw in this document is a vulnerability in every reader that implements it.
- Vulnerabilities in `Sample code/`, `SpoolmanDB/`, or `database/db_update.py`

## Out of scope

- **Cloning a chip.** TigerTag+ signs the tag's UID together with the product identity, so a
  signature is bound to one physical chip and does not transfer. Copying a UID requires a
  chip with a writable UID — this is a property of the NFC hardware market, not of the
  TigerTag protocol, and it is a known and accepted limitation.
- **Writing arbitrary data to a chip.** TigerTag chips are deliberately never write-locked,
  so that they can be reused after the spool is finished. Anyone with physical access can
  rewrite one. This is by design. What they cannot do is produce a valid TigerTag+ signature.
- **Reading a chip.** The data on a TigerTag chip is not secret.
- Vulnerabilities in third-party readers, printers, or slicers that implement the protocol
  incorrectly. Report those to their authors. If the specification led them there, that is
  in scope — tell us.
- Denial of service against `api.tigertag.io` — report to
  [tigertag@tigertag.io](mailto:tigertag@tigertag.io), not as a security advisory.
- Missing security headers or TLS configuration on the website.

---

## Key handling

- The TigerTag+ **private key is held solely by TigerTag Corp** and is never distributed,
  never present in this repository, and never present in any shipped tool or SDK.
- The corresponding **public keys are published** in
  [`database/id_version.json`](database/id_version.json), one per tag format version, in PEM
  form. They are in the public domain (CC0) and are intended to be embedded directly in
  readers.
- Verification is **ECDSA over NIST P-256 with SHA-256**, and is fully offline. A reader
  that requires a network call to verify a tag is not implementing this specification.
- **If you find a private key anywhere,** treat it as a critical vulnerability and report it
  immediately by the private routes above.

### Key rotation

A compromised or retired key is retired by **introducing a new tag format version** with a
new key pair, added to `id_version.json`. Existing readers continue to verify existing
chips against the old public key; chips issued after rotation carry the new version
identifier and verify against the new key.

Public keys are therefore append-only in practice: removing one would invalidate chips
already in the field. A key that must no longer be *trusted* — as opposed to merely no
longer *used* — is announced through a security advisory on this repository, and readers
are expected to treat tags bearing that version as unsigned.

---

## Supported versions

Security fixes are issued against the current specification version and the tag format
versions listed in `database/id_version.json`. See [`VERSIONING.md`](VERSIONING.md).

Because chips are physical objects with a long life, **no tag format version is ever
formally end-of-lifed.** A reader should expect to encounter a v1.0 chip indefinitely.

---

## Disclosure

We practise coordinated disclosure. We will not take legal action against a researcher who
reports a vulnerability in good faith through the routes above, who does not access or
modify data belonging to others, and who gives us reasonable time to issue a fix before
disclosing publicly.

Contact: [security@tigertag.io](mailto:security@tigertag.io)
