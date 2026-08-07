---
okf_version: "0.2"
opf_version: "0.2.2"
type: product-concept
opf_id: opf:tetris:state:game-over
kind: state
title: "Stack reached the top"
of_surface: opf:tetris:surface:game-board
allows: [opf:tetris:interaction:restart]
verified:
  by: agent:codex
  method: "terminal gameplay condition with an explicit recovery action"
---

The board stops advancing, preserves the result, and offers a clear restart.
