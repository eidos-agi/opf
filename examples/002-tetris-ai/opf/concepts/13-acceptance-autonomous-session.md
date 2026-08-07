---
okf_version: "0.2"
opf_version: "0.2.1"
type: product-concept
opf_id: opf:tetris-ai:acceptance:autonomous-session
kind: acceptance
title: "The autonomous session is legal and inspectable"
condition: "Fail if the same board and piece produce different choices, an illegal placement is returned, the board does not visibly advance without placement input, decision metrics are hidden, pause or restart fails, or 001's game core is duplicated instead of reused."
status: proposed
verified:
  by: agent:codex
  method: "falsifiable first-slice acceptance defined before browser verification"
---

The acceptance remains proposed until logic tests and browser exercise both pass.

