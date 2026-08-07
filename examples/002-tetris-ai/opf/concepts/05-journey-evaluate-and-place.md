---
okf_version: "0.2"
opf_version: "0.2.2"
type: product-concept
opf_id: opf:tetris-ai:journey:evaluate-and-place
kind: journey
title: "Evaluate and place pieces until the stack ends"
actor: opf:tetris-ai:user:placement-agent
outcome: opf:tetris-ai:outcome:legal-session
moments: [opf:tetris-ai:moment:choose-placement]
surfaces: [opf:tetris-ai:surface:placement-laboratory]
verified:
  by: agent:codex
  method: "the repeated autonomous loop is the complete first-slice journey"
---

For each piece, the agent enumerates legal landings, scores their resulting boards, chooses one, and commits it.

