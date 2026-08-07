# Design: open_question (replace placeholder denylist)

**Status:** proposed for 0.2.2
**Priority:** 3 from multi-model review

## Problem

Banning TBD/TODO/later does not make the unknown known. Under delivery
pressure it produces confident filler that passes the regex. A TBD is
greppable; filler is not. This is Goodhart applied to the linter.

## Proposal

1. Stop treating placeholder tokens as hard errors in admission fields.
2. Add `kind: open_question` (or `status: unknown` on any concept) with:
   - `blocking: true | false` — whether it blocks first-slice / promotion
   - `blocks: [opf:...]` — optional links to the concepts it blocks
3. Validator reports a count, e.g. `3 open questions (1 blocking first slice)`
   rather than failing the pack solely for honest unknowns.
4. Promotion gates (`validated`, `building`, `operating`) still require that
   no *blocking* open questions remain on the first-slice path.

## Example

```yaml
---
okf_version: "0.2"
opf_version: "0.2.2"
type: product-concept
opf_id: opf:eam:open:attention-ranking
kind: open_question
title: "How should attention ranking weight relationship risk?"
blocking: true
blocks: [opf:eam:slice:first-orientation]
verified:
  by: human:daniel
  method: "explicit unknown recorded in shaping"
---

Not yet decided. Must resolve before the first slice ships.
```

## Migration

- v0.2.1 denylist remains as a **warning** in draft mode.
- `--strict` in 0.2.2 fails only on *blocking* open questions for active statuses.
- Existing packs keep validating; new packs can express unknowns honestly.
