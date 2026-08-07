---
okf_version: "0.2"
opf_version: "0.2.1"
type: product-concept
opf_id: opf:tetris:journey:play-session
kind: journey
title: "Play one falling-block session"
actor: opf:tetris:user:solo-player
outcome: opf:tetris:outcome:complete-lines
moments: [opf:tetris:moment:place-piece]
surfaces: [opf:tetris:surface:game-board]
verified:
  by: agent:codex
  method: "minimum end-to-end journey for the first slice"
---

The player starts, manipulates pieces, clears lines, loses, and can restart.
