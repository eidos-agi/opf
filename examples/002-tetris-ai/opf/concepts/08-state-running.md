---
okf_version: "0.2"
opf_version: "0.2.2"
type: product-concept
opf_id: opf:tetris-ai:state:running
kind: state
title: "Agent evaluating and placing"
of_surface: opf:tetris-ai:surface:placement-laboratory
allows: [opf:tetris-ai:interaction:evaluate-and-place]
verified:
  by: agent:codex
  method: "active state required by the autonomous loop"
---

The board advances while the current candidate metrics and placement trace remain visible.

