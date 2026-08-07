---
okf_version: "0.2"
opf_version: "0.2.2"
type: product-concept
opf_id: opf:tetris:state:playing
kind: state
title: "Piece falling"
of_surface: opf:tetris:surface:game-board
allows: [opf:tetris:interaction:control-piece]
verified:
  by: agent:codex
  method: "interactive state required by the core loop"
---

A live piece falls while the player can move, rotate, drop, or pause it.
