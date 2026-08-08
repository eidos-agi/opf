---
okf_version: "0.2"
opf_version: "0.2.5"
type: product-concept
opf_id: opf:tetris-smart-arena:acceptance:lookahead-wins
kind: acceptance
title: "Lookahead is explainable and materially stronger"
condition: "Fail unless both agents receive identical seven-bag streams; the realization satisfies every project-wide experience-quality requirement through hybrid review and matches the structured oracle; the live ledger distinguishes selected-branch replies, immediate score, future score, and future gain; both agents use at most one normal input each per 100 ms tick; the fixed 50 by 300 cohort exactly produces 36 lookahead wins, 4 greedy wins, 10 draws, 5903 versus 5670 lines, 15000 versus 14837 surviving pieces, and zero illegal placements; pause and restart work; and examples 001 through 003 are reused."
status: observed
quality_coverage: [operability, usability, clarity, readability, visual-cleanliness, consistency, experiential-character]
reviewed_by: [human:daniel]
reviewed_surfaces: [opf:tetris-smart-arena:surface:thought-duel]
reviewed_revision: sha256:1fbee5eb708398b8b1c03222450d29a0851b89802b6b1c81c1e1c6942dc4bf82
evidence: [file:evidence/lookahead-wins.json@sha256-92a43d7ad2b43b906c6da4e6ab34de8f5d78ffd2811a7540686562c571b34ff5]
verified:
  by: agent:codex
  method: "falsifiable comparison and explanation gate fixed before browser evidence closure"
---

The fixed cohort passed the performance gate while the browser proved the explanation and physical input behavior.
