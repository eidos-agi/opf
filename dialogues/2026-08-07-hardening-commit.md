# Analysis of the 0.2.1 hardening commit

**Date:** 2026-08-07  
**Commit:** `ca9cc72` — "Harden OPF product and UX semantics"  
**Author:** Daniel Shanklin  
**Stats:** +922 / −216 across 21 files  
**Version:** 0.2.0 → 0.2.1

There are exactly two commits in the repository at the time of this note. The hardening landed ~10 minutes after the initial baseline.

## What changed

### Core semantics

- **Directed composition edges** replace the previous undirected connectivity check. Only specific composition fields establish membership/reachability from the product face. Back-references (`serves`, `of_surface`, `actor`, etc.) no longer hide orphans.
- **Typed target kinds** for every edge field (e.g. `problem` must point at a `problem` concept, `users` → `user`, `first_slice` → `slice`, etc.). Wrong kind is an error.
- **Distinct lifecycle gates**:
  - `shaping` — full structure + complete first-slice experience path
  - `validated` — requires at least one `acceptance` with `status: observed`
  - `operating` — requires observed `operational_proof`
  - `retired` — requires `retirement_reason`
  - Placeholders (`TBD`, `TODO`, `later`…) are rejected.
- **Mechanically complete first-slice UX path** is required:  
  `journey → moment → surface → state → interaction → proof/outcome`
- **Pinned external imports**: external refs must be of the form `emf|orf|okf:pack:object@revision` and declared in the face’s `imports` list. Strict mode fails unpinned or undeclared ones.
- **Explicit supersession**: bidirectional (`supersedes` / `superseded_by`), same kind, single live head.

### Example pack expanded

- `problem` and `promise` moved from inline strings on the face to proper concept documents.
- New concepts added: moment, interaction (completing the experience chain).
- All documents bumped to `opf_version: "0.2.1"`, external refs pinned, `imports` declared.

### Validator & tests

- YAML parser is now **fail-closed** (rejects tabs, duplicate keys, multiline scalars, lists of maps, unsupported constructs) and reports parse errors.
- Many more kind-specific requirements (journey needs `actor`/`outcome`/`moments`, surface needs `surface_kind`, state needs `allows` or `terminal: true`, interaction needs proof, acceptance needs condition/status + evidence when observed/failed, etc.).
- Tests roughly tripled in size and now include:
  - Full strict validation of the shipped example
  - Wrong target kinds, unpinned externals, incomplete experience chains, supersession errors, placeholder rejection, back-reference orphans, etc.

### Docs

SPEC, README, CHANGELOG, and AGENTS.md all updated to match the tighter contract.

## Assessment relative to the initial review

This commit directly addresses several of the gaps noted on the initial version:

- Undirected graph → directed composition reachability
- Thin tests → real example + many adversarial cases
- Weak external-ref handling → pinned + imported
- Missing kind-specific rules → substantially expanded
- Placeholder risk → rejected
- Parser ambiguity → explicit fail-closed behavior documented in SPEC

Still missing from this commit: a `LICENSE` file (MIT is only declared in `pyproject.toml`).

Overall this is a rapid, high-quality hardening of the format and validator less than an hour after the first public drop.
