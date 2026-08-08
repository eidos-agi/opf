---
okf_version: "0.2"
opf_version: "0.2.3"
type: product-concept
opf_id: opf:tetris-ai:interaction:restart-seed
kind: interaction
title: "Restart the deterministic run"
on: opf:tetris-ai:state:stack-ended
yields: [opf:tetris-ai:state:running, opf:tetris-ai:outcome:legal-session]
covered_by: opf:tetris-ai:acceptance:autonomous-session
verified:
  by: agent:codex
  method: "recovery preserves repeatability for inspection"
---

Restart restores the fixed seed, empty board, zero totals, and an empty trace.

