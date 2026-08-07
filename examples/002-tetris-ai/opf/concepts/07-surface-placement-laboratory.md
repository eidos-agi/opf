---
okf_version: "0.2"
opf_version: "0.2.1"
type: product-concept
opf_id: opf:tetris-ai:surface:placement-laboratory
kind: surface
title: "Placement laboratory"
surface_kind: screen
serves: [opf:tetris-ai:outcome:legal-session]
states: [opf:tetris-ai:state:running, opf:tetris-ai:state:stack-ended]
proof: [opf:tetris-ai:acceptance:autonomous-session]
verified:
  by: agent:codex
  method: "one surface can show the board, decision, controls, and trace"
---

The surface presents the live board as an instrument beside the agent's current metrics and recent placements.

