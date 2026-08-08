---
okf_version: "0.2"
opf_version: "0.2.3"
type: product-concept
opf_id: opf:tetris-ai-arena:slice:seeded-arena
kind: slice
title: "One seeded control-versus-candidate arena"
serves: [opf:tetris-ai-arena:outcome:strategy-evidence]
includes: [opf:tetris-ai-arena:journey:watch-and-evaluate]
proof: [opf:tetris-ai-arena:acceptance:heuristic-beats-random]
non_goals: ["training", "model APIs", "strategy tuning", "tournament management"]
verified:
  by: agent:codex
  method: "smallest slice that tests whether the existing heuristic adds value"
---

The slice reuses the 001 engine and 002 heuristic, adding only a random control, fair sequence generator, arena, and evaluator.
