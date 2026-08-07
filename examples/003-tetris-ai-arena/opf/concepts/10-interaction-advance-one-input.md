---
okf_version: "0.2"
opf_version: "0.2.2"
type: product-concept
opf_id: opf:tetris-ai-arena:interaction:advance-one-input
kind: interaction
title: "Advance each agent by one legal input"
on: opf:tetris-ai-arena:state:match-running
yields: opf:tetris-ai-arena:outcome:strategy-evidence
covered_by: opf:tetris-ai-arena:acceptance:heuristic-beats-random
verified:
  by: agent:codex
  method: "the shared action-plan mechanism prevents direct placement"
---

An agent may rotate once, nudge once, or descend once per clock tick; it cannot assign a target position.
