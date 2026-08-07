---
okf_version: "0.2"
opf_version: "0.2.1"
type: product-concept
opf_id: opf:tetris-ai:moment:choose-placement
kind: moment
title: "Choose one legal landing"
in_journey: opf:tetris-ai:journey:evaluate-and-place
on_surface: opf:tetris-ai:surface:placement-laboratory
verified:
  by: agent:codex
  method: "smallest repeated decision in autonomous play"
---

The agent ranks all legal rotation-and-column candidates and selects a deterministic winner.

