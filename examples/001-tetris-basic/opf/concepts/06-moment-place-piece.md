---
okf_version: "0.2"
opf_version: "0.2.2"
type: product-concept
opf_id: opf:tetris:moment:place-piece
kind: moment
title: "Place the current piece"
in_journey: opf:tetris:journey:play-session
on_surface: opf:tetris:surface:game-board
verified:
  by: agent:codex
  method: "smallest repeated decision in the core loop"
---

The player reads the board, moves or rotates the piece, and commits its position.
