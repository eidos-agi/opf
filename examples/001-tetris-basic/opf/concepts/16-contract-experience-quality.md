---
okf_version: "0.2"
opf_version: "0.2.4"
type: product-concept
opf_id: opf:tetris:contract:experience-quality
kind: contract
contract_type: experience-quality
title: "Basic Tetris product-wide experience quality"
scope: product
qualities: [operability, usability, clarity, readability, visual-cleanliness, consistency, experiential-character]
requirements:
  - operability=play, pause, restart, keyboard input, scoring, and game over work without invalid state
  - usability=a first-time player can begin and recover without instructions
  - clarity=board, next piece, score, level, and controls have an obvious hierarchy
  - readability=status and controls remain legible at desktop and narrow viewport sizes
  - visual-cleanliness=the playfield dominates and decorative elements do not compete with play
  - consistency=labels, colors, spacing, and control behavior retain one system across states
  - experiential-character=the product feels focused, immediate, and recognizably like a polished arcade game
assurance: hybrid
proof: opf:tetris:acceptance:playable-session
verified:
  by: agent:codex
  method: "project-wide quality contract derived from the validated playable session"
---

# Basic Tetris experience quality

This contract governs the whole product experience rather than any single screen or implementation.
