---
okf_version: "0.2"
opf_version: "0.2.2"
type: product-concept
opf_id: opf:tetris-ai-arena:interaction:restart-match
kind: interaction
title: "Restart the identical match"
on: opf:tetris-ai-arena:state:match-complete
yields: [opf:tetris-ai-arena:state:match-running, opf:tetris-ai-arena:outcome:strategy-evidence]
covered_by: opf:tetris-ai-arena:acceptance:heuristic-beats-random
verified:
  by: agent:codex
  method: "fixed seeds make the visible comparison reproducible"
---

Restart resets both boards, counters, strategy RNG, and the common piece sequence.
