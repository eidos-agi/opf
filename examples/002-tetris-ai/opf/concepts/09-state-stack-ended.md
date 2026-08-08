---
okf_version: "0.2"
opf_version: "0.2.3"
type: product-concept
opf_id: opf:tetris-ai:state:stack-ended
kind: state
title: "No legal placement remains"
of_surface: opf:tetris-ai:surface:placement-laboratory
allows: [opf:tetris-ai:interaction:restart-seed]
verified:
  by: agent:codex
  method: "terminal state needs an explicit recovery"
---

The run stops, preserves its totals and trace, and offers a deterministic restart.

