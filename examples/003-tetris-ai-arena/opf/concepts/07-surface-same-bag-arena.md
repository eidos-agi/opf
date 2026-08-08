---
okf_version: "0.2"
opf_version: "0.2.3"
type: product-concept
opf_id: opf:tetris-ai-arena:surface:same-bag-arena
kind: surface
title: "Same bag arena"
surface_kind: screen
serves: [opf:tetris-ai-arena:outcome:strategy-evidence]
states: [opf:tetris-ai-arena:state:match-running, opf:tetris-ai-arena:state:match-complete]
proof: [opf:tetris-ai-arena:acceptance:heuristic-beats-random]
verified:
  by: agent:codex
  method: "side-by-side boards make the controlled variable legible"
---

The screen labels the control and candidate, shows both boards and totals, and provides pause and deterministic restart.
