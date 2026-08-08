---
okf_version: "0.2"
opf_version: "0.2.2"
type: product-concept
opf_id: opf:tetris-smart-arena:interaction:advance-experts
kind: interaction
title: "Advance both experts through normal inputs"
on: opf:tetris-smart-arena:state:duel-running
yields: opf:tetris-smart-arena:outcome:explain-superiority
covered_by: opf:tetris-smart-arena:acceptance:lookahead-wins
verified:
  by: agent:codex
  method: "the shared action planner preserves the no-teleport constraint"
---

Each clock tick permits one rotation, horizontal nudge, or downward nudge per unfinished agent.
