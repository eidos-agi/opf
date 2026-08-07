# Comparative eval harness (skeleton)

**Status:** proposed for 0.2.2+
**Priority:** 9 from multi-model review

## Goal

Answer the ceremony-vs-utility question empirically:

does an OPF pack improve agent outcomes versus a conventional PRD
for the same product task?

## Setup

1. **Fixture pair** for one product (start with Eidos Agent Manager):
   - `examples/eidos-agent-manager/` (OPF pack)
   - `examples/eidos-agent-manager-prd.md` (single prose PRD, same intent)
2. **Agent task set** (fixed prompts):
   - Name the authority boundaries
   - List non-goals
   - Propose the first slice and its acceptance criterion
   - Identify what must not be rebuilt
3. **Same model / tool config** for both conditions.

## Metrics

| Metric | How measured |
|--------|----------------|
| Authority violations | Agent proposes work outside declared authority-boundaries |
| Non-goal violations | Agent expands into listed non-goals |
| Acceptance clarity | First-slice proof is falsifiable without raw-tree inspection |
| Rework | Follow-up turns needed to correct scope drift |
| Time-to-first-slice | Turns until a complete experience path is stated |

## Harness layout (future)

```text
evals/
  fixtures/
    eam-opf/
    eam-prd/
  tasks/
    authority.md
    first-slice.md
  run.py          # runs agent against both fixtures
  score.py        # computes metrics from transcripts
```

## Success criterion for OPF

On the fixed task set, OPF condition shows fewer authority and non-goal
violations and equal or better time-to-first-slice than the PRD condition.

Until this harness exists, claims about utility remain design arguments,
not measured results.
