---
okf_version: "0.2"
opf_version: "0.2.2"
type: product-concept
opf_id: opf:tetris-ai-arena:state:match-complete
kind: state
title: "The fixed match has a result"
of_surface: opf:tetris-ai-arena:surface:same-bag-arena
allows: [opf:tetris-ai-arena:interaction:restart-match]
verified:
  by: agent:codex
  method: "the terminal state preserves the comparison and a repeatable recovery"
---

The arena names the winner from cleared lines and retains both final boards and totals.
