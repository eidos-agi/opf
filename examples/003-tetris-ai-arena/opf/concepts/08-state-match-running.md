---
okf_version: "0.2"
opf_version: "0.2.3"
type: product-concept
opf_id: opf:tetris-ai-arena:state:match-running
kind: state
title: "Both strategies are playing"
of_surface: opf:tetris-ai-arena:surface:same-bag-arena
allows: [opf:tetris-ai-arena:interaction:advance-one-input]
verified:
  by: agent:codex
  method: "active state is required for visible non-teleporting play"
---

Every 100 ms tick grants each unfinished agent no more than one normal game input.
