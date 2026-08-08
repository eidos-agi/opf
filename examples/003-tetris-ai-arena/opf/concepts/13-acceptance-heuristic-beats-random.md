---
okf_version: "0.2"
opf_version: "0.2.3"
type: product-concept
opf_id: opf:tetris-ai-arena:acceptance:heuristic-beats-random
kind: acceptance
title: "The heuristic materially beats the legal random control"
condition: "Fail unless both agents receive identical seven-bag streams, the visible agents use at most one normal game input each per 100 ms tick, 50 fixed 300-piece matches contain zero illegal placements, the heuristic wins at least 45 matches and clears at least three times the random agent's aggregate lines, pause and restart work, or the 001 engine and 002 heuristic are not reused."
status: observed
evidence: [file:evidence/heuristic-beats-random.json@sha256-23819d50e2adde26df593a03662806e5d18036ba1ca5c18507938beddfa337ad]
verified:
  by: agent:codex
  method: "threshold declared before browser verification and OPF validation"
---

The automated evaluator passed the declared comparison threshold; browser observation separately proved that the animated arena follows the input constraint.
