---
okf_version: "0.2"
opf_version: "0.2.2"
type: product-concept
opf_id: opf:tetris:interaction:restart
kind: interaction
title: "Restart after game over"
on: opf:tetris:state:game-over
yields: [opf:tetris:state:playing, opf:tetris:outcome:complete-lines]
covered_by: opf:tetris:acceptance:playable-session
verified:
  by: agent:codex
  method: "recovery interaction required for repeated sessions"
---

Restart clears the board, score, lines, and level, then spawns a new piece.
