---
okf_version: "0.2"
opf_version: "0.2.1"
type: product-concept
opf_id: opf:tetris:surface:game-board
kind: surface
title: "Falling-block game board"
surface_kind: screen
serves: [opf:tetris:outcome:complete-lines]
states: [opf:tetris:state:playing, opf:tetris:state:game-over]
proof: [opf:tetris:acceptance:playable-session]
verified:
  by: agent:codex
  method: "single surface required by the first-slice journey"
---

The surface contains the board, current and next pieces, score, status, controls, and restart action.
