---
okf_version: "0.2"
opf_version: "0.2.3"
type: product-concept
opf_id: opf:tetris-smart-arena:slice:depth-duel
kind: slice
title: "One depth-one versus depth-two duel"
serves: [opf:tetris-smart-arena:outcome:explain-superiority]
includes: [opf:tetris-smart-arena:journey:inspect-foresight]
proof: [opf:tetris-smart-arena:acceptance:lookahead-wins]
non_goals: ["deeper search", "weight tuning", "learning", "model calls", "tournament infrastructure"]
verified:
  by: agent:codex
  method: "one extra ply is the smallest intelligible increase in planning"
---

The slice reuses examples 001 through 003 and adds only next-piece lookahead, explanation, and comparative proof.
