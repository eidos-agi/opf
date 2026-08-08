---
name: use-opf
description: Define, review, and validate Open Product Format packs. Use when turning intent and research into linked product commitments, UX journeys, first slices, realization contracts, or evidence-backed release gates, and when checking OPF Markdown with opf-validate.
---

# Use OPF

## Workflow

1. Read `SPEC.md` and the pack's `index.md` before editing concepts.
2. Keep human intent in pinned EMF references and research in pinned ORF references. Do not restate either as agent-authored truth.
3. Add the smallest atomic concept that closes the observed product gap. Keep IDs stable and composition edges directed from the product face.
4. Preserve UX as journeys, moments, surfaces, states, and interactions tied to outcomes and proof.
5. Match realization claims to their evidence. Never claim experience equivalence or reference fidelity without the required attributed or content-addressed proof.
6. Run the strict gate:

```bash
opf-validate --strict path/to/pack
```

Treat every reported error as a publication blocker. Fix the concept at the authority surface; do not weaken the validator to admit an invalid pack.
