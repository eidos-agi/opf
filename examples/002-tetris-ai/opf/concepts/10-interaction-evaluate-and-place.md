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

The agent reaches an enumerated legal placement through normal game inputs, limited to one nudge or rotation every 100 ms. It cannot teleport to the chosen landing.
