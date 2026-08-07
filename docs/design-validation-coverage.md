# Design: validation coverage and failed semantics

**Status:** proposed for 0.2.2
**Priority:** 2 from multi-model review

## Problem

In v0.2.1 a single acceptance with status: observed anywhere satisfies
the validated gate; the same pattern applies to operational_proof for
operating. That is the weakest gate relative to the rest of the strictness.
There is also no rule about unresolved failed acceptances while sitting
in operating.

## Proposal

### Coverage for validated

Minimum rule for 0.2.2:
- validation must be non-empty
- every target must resolve to kind: acceptance with status: observed
- at least one acceptance must sit on the first-slice experience path

### Coverage for operating

Same shape for operational_proof: non-empty, all observed, at least one
on the first-slice path.

### Failed acceptances

- status: failed requires evidence (already true in 0.2.1).
- A pack in validated or operating must not have unresolved failed
  acceptances on the first-slice path unless each is superseded.
- Error code: OPF-E046 (failed_acceptance_blocking).

## Migration

- Draft mode: warn when coverage is thin.
- --strict: enforce coverage and failed rules for validated+.
- Example pack remains valid under the minimum rule.
