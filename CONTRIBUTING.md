# Contributing to the TigerTag protocol

Thank you for wanting to improve TigerTag.

This repository is the **source of truth** for how data is stored on a TigerTag chip. Every
reader, writer, printer, slicer, and app in the field implements what is written here. That
makes it different from an ordinary software project, and it changes how contributions work.

---

## Please do not fork the specification

You are legally free to fork it — [`LICENSING.md`](LICENSING.md) does not stop you, and we
are not going to add a licence that does. We are asking you not to, because it does not
help you.

A fork of a program is a working program. A fork of a specification is a document
describing chips that nobody manufactures and no reader in the field understands. It cannot
be called TigerTag ([`TRADEMARK.md`](TRADEMARK.md)), it will drift out of date, and it
fragments the ecosystem for everyone including you.

If the spec is wrong, unclear, or missing something you need, **the fix is a proposal, and
the proposal will be read.** Over two million chips are in production; we take changes to
this document seriously and we would much rather have your change in the canonical spec
than in a fork.

---

## Two kinds of contribution

### 1. Corrections — just open a pull request

If something is factually wrong or unclear and the fix does not change the protocol, send a
PR directly. No process needed. This includes:

- Typos, broken links, incorrect hex values in examples
- Clarifying ambiguous wording that does not change behaviour
- Improving diagrams, adding translations
- Fixing bugs in `Sample code/` or `SpoolmanDB/`
- Adding a sample implementation in a new language

### 2. Protocol changes — open a TEP

Anything that changes what a conforming implementation must do goes through a **TEP
(TigerTag Enhancement Proposal)**. This includes:

- Adding, removing, or repurposing a field
- Changing a memory offset, an encoding, or a byte order
- Changing signature or verification behaviour
- Adding a new tag format version
- Anything that could make an existing reader misinterpret a chip

Open an issue using the
[**Protocol proposal**](https://github.com/TigerTag-Project/TigerTag-RFID-Guide/issues/new?template=protocol-proposal.yml)
template.

---

## The TEP process

A TEP is a GitHub issue. There is no separate repository, no numbering committee, and no
mailing list. Keep it light.

```
  Draft  ──►  Discussion  ──►  Accepted  ──►  Released
    │             │               │              │
    │             └──► Deferred   └──► Rejected  └──► spec version bump
    └──► Withdrawn
```

**1. Draft.** You open an issue from the template. It is labelled `tep` and `draft`. State
the problem before the solution. A TEP that describes a real problem badly is more useful
than one that describes an elegant solution to nothing.

**2. Discussion.** Public, in the issue thread. Expect questions about backward
compatibility above all else. The load-bearing question for almost every TEP is: *what does
an existing reader in the field do when it encounters a chip written under this proposal?*
If the answer is "misbehaves", the TEP needs a new tag format version, not a new field.

**3. Accepted / Deferred / Rejected.** A maintainer marks the outcome and says why in the
thread. Rejections come with a reason. "Deferred" means good idea, wrong time — usually
waiting on a version bump that is already planned.

**4. Released.** An accepted TEP is implemented in `README.md`, the version-history table
is updated, and the spec version is bumped per [`VERSIONING.md`](VERSIONING.md). The TEP
issue is closed with a link to the released version.

There is no fixed timeline. Chip-layout changes are slow by nature and that is correct.

---

## What makes a TEP likely to be accepted

- **It solves a problem someone actually has.** Ideally with a named product or workflow.
- **It is backward compatible**, or it is honest that it is not and proposes a version bump.
- **It fits the memory budget.** NTAG213 has 144 usable bytes. Space on the chip is the
  scarcest resource in this project; a TEP that needs four bytes should explain why two
  will not do.
- **It does not require a server.** Offline operation is a core property of TigerTag.
- **It does not weaken the signature.** See [`SECURITY.md`](SECURITY.md).

## What will be rejected

- Changes that break field-deployed readers without a version bump
- Fields that duplicate information already derivable from the chip or the public API
- Anything that makes an implementation depend on a network round-trip
- Anything that requires permission from TigerTag Corp to implement

---

## Reference-database entries

**Do not send pull requests adding entries to `database/*.json`.** These files are
generated from the TigerTag catalogue and are overwritten automatically by the sync
workflow — a PR against them will be silently reverted on the next sync.

To have a brand, material, aspect, or type added to the reference database, open a regular
issue describing the entry, or contact [tigertag@tigertag.io](mailto:tigertag@tigertag.io).

Corrections to `database/db_update.py` and the sync tooling are welcome as PRs.

---

## Security issues

Do **not** open a public issue for a vulnerability, especially one touching the TigerTag+
signature, key handling, or verification. See [`SECURITY.md`](SECURITY.md).

---

## Licensing of contributions

By contributing, you agree that your contribution is licensed under the same terms as the
material it modifies, as set out in [`LICENSING.md`](LICENSING.md):

| You are changing | Your contribution is licensed under |
|---|---|
| Specification text, `Images/`, `assets/` | `CC-BY-4.0` |
| `Sample code/`, `SpoolmanDB/`, `database/db_update.py` | `Apache-2.0` |
| Reference database content | `CC0-1.0` |

Apache-2.0 §5 means a code contribution carries an express patent grant. This is
intentional: it is what lets a manufacturer embed the sample code without a patent review.

You retain copyright in your contribution. There is no CLA.

---

## Code style

- Python: standard library only where possible, `Sample code/` must run with no
  dependencies beyond `cryptography` for signature verification.
- Every source file starts with an SPDX header:
  `# SPDX-License-Identifier: Apache-2.0`
- Keep examples runnable. If you change a hex value, verify it against a real dump.

---

## Questions

Open an issue, or find us on [Discord](https://discord.gg/3Qv5TSqnJH).
