---
okf_version: "0.2"
opf_version: "0.2.1"
type: product-concept
opf_id: opf:tetris:interaction:control-piece
kind: interaction
title: "Move, rotate, or drop the piece"
on: opf:tetris:state:playing
yields: opf:tetris:outcome:complete-lines
covered_by: opf:tetris:acceptance:playable-session
verified:
  by: agent:codex
  method: "observable input-to-board transition in the first slice"
---

Keyboard and touch controls change the current piece only when the resulting position is legal.
