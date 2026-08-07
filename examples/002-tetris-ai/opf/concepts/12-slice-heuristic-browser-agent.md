---
okf_version: "0.2"
opf_version: "0.2.2"
type: product-concept
opf_id: opf:tetris-ai:slice:heuristic-browser-agent
kind: slice
title: "One inspectable heuristic browser agent"
serves: [opf:tetris-ai:outcome:legal-session]
includes: [opf:tetris-ai:journey:evaluate-and-place]
proof: [opf:tetris-ai:acceptance:autonomous-session]
non_goals: ["model training", "network calls", "perfect play", "engine duplication"]
verified:
  by: agent:codex
  method: "smallest implementation that satisfies example 002"
---

The slice is complete when the agent can repeatedly choose legal placements while exposing its scoring evidence.

