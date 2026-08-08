---
okf_version: "0.2"
opf_version: "0.2.3"
type: product-concept
opf_id: opf:tetris-ai:acceptance:autonomous-session
kind: acceptance
title: "The autonomous session is legal and inspectable"
condition: "Fail if the same board and piece produce different choices, an illegal placement is returned, a piece teleports instead of using at most one nudge or rotation every 100 ms, the board does not visibly advance without human placement input, decision metrics are hidden, pause or restart fails, or 001's game core is duplicated instead of reused."
status: observed
evidence: [file:evidence/autonomous-session.json@sha256-b4a1a51f8043a0d246f9973f4d15367a690dfa3efc48eeb92773383298375954]
verified:
  by: agent:codex
  method: "falsifiable first-slice acceptance defined before browser verification"
---

The logic suite and timed browser observation passed, including the 100 ms input constraint.
