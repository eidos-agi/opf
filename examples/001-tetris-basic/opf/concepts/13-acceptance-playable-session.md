---
okf_version: "0.2"
opf_version: "0.2.1"
type: product-concept
opf_id: opf:tetris:acceptance:playable-session
kind: acceptance
title: "The basic session is playable"
condition: "Fail if pieces do not fall, legal controls do not move or rotate them, complete rows do not clear and score, game over does not stop play, or restart does not begin a clean session."
status: proposed
verified:
  by: agent:codex
  method: "falsifiable first-slice acceptance derived before implementation"
---

The acceptance remains proposed until the implementation is exercised in a browser.
