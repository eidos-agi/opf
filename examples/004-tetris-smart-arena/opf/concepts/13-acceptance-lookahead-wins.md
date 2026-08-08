---
okf_version: "0.2"
opf_version: "0.2.3"
type: product-concept
opf_id: opf:tetris-smart-arena:acceptance:lookahead-wins
kind: acceptance
title: "Lookahead is explainable and materially stronger"
condition: "Fail unless both agents receive identical seven-bag streams; the realization matches the pinned 1440 by 1400 composition and structured oracle within the realization contract's tolerance; the live ledger distinguishes selected-branch replies, immediate score, future score, and future gain; both agents use at most one normal input each per 100 ms tick; the fixed 50 by 300 cohort exactly produces 36 lookahead wins, 4 greedy wins, 10 draws, 5903 versus 5670 lines, 15000 versus 14837 surviving pieces, and zero illegal placements; pause and restart work; and examples 001 through 003 are reused."
status: observed
evidence: [file:evidence/lookahead-wins.json@sha256-f87012b3bb5c7eb114d36d99d2376fe6d3b637006a22147ff38820f5e92a5e9c]
verified:
  by: agent:codex
  method: "falsifiable comparison and explanation gate fixed before browser evidence closure"
---

The fixed cohort passed the performance gate while the browser proved the explanation and physical input behavior.
