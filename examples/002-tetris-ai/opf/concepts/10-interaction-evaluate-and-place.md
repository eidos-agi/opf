---
okf_version: "0.2"
opf_version: "0.2.1"
type: product-concept
opf_id: opf:tetris-ai:interaction:evaluate-and-place
kind: interaction
title: "Evaluate legal landings and place the winner"
on: opf:tetris-ai:state:running
yields: opf:tetris-ai:outcome:legal-session
covered_by: opf:tetris-ai:acceptance:autonomous-session
verified:
  by: agent:codex
  method: "observable board transition backed by deterministic scoring"
---

Only an enumerated legal placement may be committed to the shared game board.

