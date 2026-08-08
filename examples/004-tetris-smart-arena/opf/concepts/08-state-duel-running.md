---
okf_version: "0.2"
opf_version: "0.2.3"
type: product-concept
opf_id: opf:tetris-smart-arena:state:duel-running
kind: state
title: "Both experts are playing"
of_surface: opf:tetris-smart-arena:surface:thought-duel
allows: [opf:tetris-smart-arena:interaction:advance-experts]
verified:
  by: agent:codex
  method: "active play is required to connect reasoning with board consequences"
---

Each agent receives one ordinary input per 100 ms while the reason ledger updates at placement boundaries.
