---
okf_version: "0.2"
opf_version: "0.2.4"
type: product-concept
opf_id: opf:tetris-ai:contract:experience-quality
kind: contract
contract_type: experience-quality
title: "Tetris Placement Agent product-wide experience quality"
scope: product
qualities: [operability, usability, clarity, readability, visual-cleanliness, consistency, experiential-character]
requirements:
  - operability=the agent plays only through legal timed inputs and pause and restart remain reliable
  - usability=an evaluator can start, pause, restart, and understand the agent without instructions
  - clarity=the current move, reason, board state, and outcome are visibly distinct
  - readability=decision text and game status remain legible at desktop and narrow viewport sizes
  - visual-cleanliness=gameplay and decision evidence dominate without decorative clutter
  - consistency=agent vocabulary, colors, spacing, and controls retain one system across states
  - experiential-character=the product feels like a transparent autonomous player rather than an opaque animation
assurance: hybrid
proof: opf:tetris-ai:acceptance:autonomous-session
verified:
  by: agent:codex
  method: "project-wide quality contract derived from the validated autonomous session"
---

# Tetris Placement Agent experience quality

This contract governs the whole product experience rather than any single screen or implementation.
