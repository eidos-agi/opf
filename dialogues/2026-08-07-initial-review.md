# Multi-agent review of OPF first version (v0.2.0)

**Date:** 2026-08-07  
**Subject:** [eidos-agi/opf](https://github.com/eidos-agi/opf) at commit `b3174f1` ("Establish Open Product Format v0.2.0 baseline")

This is a brand-new repository (created 2026-08-07, single commit at the time of review). It is a thoughtful, zero-dependency Python package that defines and validates **OPF** — an additive profile of OKF v0.2 for product definition.

## What OPF is

OPF treats a product as a **graph of atomic, linked, testable concepts** rather than a monolithic PRD. It deliberately keeps concerns separated:

```
OKF  — knowledge and trust
EMF  — human intent and durable memory
ORF  — research and graded findings
OPF  — product commitments, UX, slices, and proof
```

A pack lives in `docs/opf/` (or similar) with:
- `index.md` — the product face (promise, outcomes, first slice, authority, etc.)
- `concepts/*.md` — atomic concepts (user, outcome, journey, surface, state, slice, acceptance, authority-boundary, …)
- `log.md` — append-only history

The design is driven by observed failures (wall-of-prose PRDs, lost human intent, selective research citation, vague authority boundaries, non-falsifiable roadmaps, UX arriving late, disconnected corpora). The SPEC maps each failure to a concrete rule.

## Strengths

**Conceptual design is the standout.**  
The experience chain (`user → outcome → journey → moment → surface → state → interaction → proof`), required lifecycle admission gates, explicit first-slice + non-goals + proof, and authority boundaries are unusually clear and agent-friendly. Treating UX concepts as first-class product concepts (not post-hoc screenshots) is especially good.

**Validator is purposeful and clean.**  
- Pure stdlib, custom minimal YAML frontmatter parser (intentional).
- Checks: version alignment, types/kinds, verified provenance, product admission for `shaping+`, surface/slice traceability, unique `opf_id`s, resolvable internal references, graph connectivity from the product face (no orphans), missing `log.md` warning.
- CLI: `python -m opf.validate --selftest` and `--strict <pack>`.
- The shipped example pack validates cleanly under `--strict`.

**Example is coherent.**  
The “Eidos Agent Manager” pack (index + 8 concepts) demonstrates a real connected graph with a meaningful first slice and falsifiable acceptance criterion. It is small enough to read and understand quickly.

**Agent-oriented thinking.**  
`AGENTS.md` is concise and useful. Stable IDs + typed edges + proof make the format naturally consumable by agents.

**Philosophy of restraint.**  
“Add a field or rule only for an observed failure; keep the validator stdlib-only.” This is visible in the code and SPEC.

## Gaps and weaknesses (expected for a first version)

1. **Packaging polish**
   - No `LICENSE` file (MIT is declared in `pyproject.toml`).
   - `pyproject.toml` is minimal — missing authors, project.urls, classifiers, package discovery config.
   - README is functional but thin.

2. **Custom YAML parser**
   - Intentionally limited. Real-world tools or multi-line values will break it.
   - The supported subset needs to be documented precisely.

3. **Tests & CI**
   - Only three unittest cases + a selftest. The shipped example itself is not exercised by the test suite.
   - No GitHub Actions.

4. **Validator depth**
   - Graph connectivity is undirected (sufficient for “no orphans,” but does not enforce edge directionality).
   - Few kind-specific required fields beyond surface and slice.
   - Body/content is not validated.
   - External `emf:` / `orf:` references are not checked beyond presence of the field.

5. **Minor nits**
   - Example `index.md` omits the `research` field shown in the SPEC illustration.
   - No install instructions or note that the package is not (yet) on PyPI.

## Prioritized suggestions

**Immediate**
- Add a proper `LICENSE` file.
- Expand `pyproject.toml` (metadata, urls, package discovery).
- Add a GitHub Actions workflow that runs selftest + unittest + validates the example pack under `--strict`.
- Document the exact YAML subset the parser accepts.
- Make the example pack a formal test case.

**Short-term**
- Slightly richer README.
- A few more kind-specific required fields where they prevent common failure modes.
- Optional research requirement (or strong recommendation) for later lifecycle statuses.

## Verdict

This is a **strong, purposeful first version**. The conceptual model is the most interesting part — it is unusually clear about what product definition should actually contain and how it should stay linked to human intent and evidence. The validator is small, focused, and already useful. The example proves the format works.

The gaps are almost all packaging, test/CI, and documentation hygiene — exactly what one expects on day one of a new format. Fix those and this becomes a solid foundation for the Eidos family and for any team that wants agent-readable, falsifiable product definitions instead of prose walls.

Well done for a v0.2.0 drop. The philosophy of “address observed failures, stay stdlib-only, keep concepts atomic” is already visible and coherent.
