---
okf_version: "0.2"
opf_version: "0.2.2"
type: product-concept
opf_id: opf:tetris-smart-arena:interaction:restart-duel
kind: interaction
title: "Restart the identical duel"
on: opf:tetris-smart-arena:state:duel-complete
yields: [opf:tetris-smart-arena:state:duel-running, opf:tetris-smart-arena:outcome:explain-superiority]
covered_by: opf:tetris-smart-arena:acceptance:lookahead-wins
verified:
  by: agent:codex
  method: "fixed seeds make both decisions and outcomes reproducible"
---

Restart resets both boards, totals, divergence count, and the shared piece stream.
