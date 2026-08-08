---
okf_version: "0.2"
opf_version: "0.2.2"
type: product-concept
opf_id: opf:tetris-smart-arena:state:duel-complete
kind: state
title: "The fixed duel has ended"
of_surface: opf:tetris-smart-arena:surface:thought-duel
allows: [opf:tetris-smart-arena:interaction:restart-duel]
verified:
  by: agent:codex
  method: "a terminal comparison needs a stable result and repeatable recovery"
---

The final boards and line totals remain visible until the evaluator restarts the seed.
