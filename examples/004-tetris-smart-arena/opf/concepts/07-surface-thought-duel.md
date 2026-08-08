---
okf_version: "0.2"
opf_version: "0.2.2"
type: product-concept
opf_id: opf:tetris-smart-arena:surface:thought-duel
kind: surface
title: "One move further duel"
surface_kind: screen
serves: [opf:tetris-smart-arena:outcome:explain-superiority]
states: [opf:tetris-smart-arena:state:duel-running, opf:tetris-smart-arena:state:duel-complete]
proof: [opf:tetris-smart-arena:acceptance:lookahead-wins]
verified:
  by: agent:codex
  method: "side-by-side boards plus a shared reason ledger expose method and play"
---

The surface distinguishes depth one from depth two without calling either strategy random or incompetent.
