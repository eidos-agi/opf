---
okf_version: "0.2"
opf_version: "0.2.2"
type: product-concept
opf_id: opf:tetris-smart-arena:acceptance:lookahead-wins
kind: acceptance
title: "Lookahead is explainable and materially stronger"
condition: "Fail unless both agents receive identical seven-bag streams, the live ledger shows current and next pieces plus immediate and future scoring, choices visibly diverge, both agents use at most one normal input each per 100 ms tick, 50 fixed 300-piece matches contain zero illegal placements, lookahead wins at least 30 matches, clears at least 150 more aggregate lines, survives more pieces, pause and restart work, or examples 001 through 003 are not reused."
status: observed
evidence: [file:evidence/lookahead-wins.json@sha256-5f1e44cb0a3d19acdbf21fda97db4770319132cc7c714f50b2866560a8383df6]
verified:
  by: agent:codex
  method: "falsifiable comparison and explanation gate fixed before browser evidence closure"
---

The fixed cohort passed the performance gate while the browser proved the explanation and physical input behavior.
