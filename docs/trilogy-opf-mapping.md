# Trilogy ↔ OPF Mapping

**Status:** living documentation  
**Date:** 2026-08-07

Eidos public materials describe two related but distinct families. This table
makes the relationship explicit so adopters know which artifact to use.

## The two families

| Layer | Public site / Trilogy | Format family (this repo) |
|-------|----------------------|---------------------------|
| North star | **Telos** (unchanging vision) | *Outside OPF* — human intent lives in **EMF** |
| Decisions / evidence | **research.md** | **ORF** (approved research and graded findings) |
| Governance / contracts | **Governor** (vision, goals, guardrails, ADRs) | **OPF** authority-boundaries, non-goals, product face |
| Execution / work tracking | **Docket** (tasks, milestones, Definition of Done) | **OPF** slices, acceptance, and the experience path |
| Improvement loop | **Praxis** | *Outside OPF* — runtime and process, not the format |
| Knowledge / trust base | — | **OKF** (knowledge and trust substrate) |

## Overlap and ownership

| Concern | Prefer | Why |
|---------|--------|-----|
| Human intent / north-star prose | EMF (linked from OPF face) | OPF must not restate agent paraphrases as human intent |
| Evidence-graded research | ORF or research.md | ORF is the format profile; research.md is the Trilogy tool |
| Guardrails that block work | Governor **and** OPF `authority-boundary` / `non_goals` | Governor is the runtime contract; OPF records the product-level boundary |
| What the first shippable slice is | OPF `slice` + `acceptance` | Docket tracks tasks; OPF defines the falsifiable product slice |
| Day-to-day task list | Docket | OPF is not an issue tracker |
| Product promise, users, journeys, surfaces | OPF | Trilogy tools do not define UX or product face |

## Rule of thumb

- **Trilogy tools** govern *how an agent works* (decide → constrain → execute).
- **OPF** defines *what the product is* (promise, experience, slice, proof) as a
  linked, testable graph.
- Link, do not merge. An OPF pack may reference EMF/ORF (and by extension the
  Trilogy artifacts that produce them); it does not replace Governor or Docket.

## Open questions

- Should Governor ADRs be linkable as OPF `decision` concepts?
- Should a Docket Definition of Done be required to point at an OPF `acceptance`?
- Is there a single install meta-package that pulls Trilogy + OPF validator?

This mapping will be updated as the families stabilize.
