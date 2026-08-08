---
okf_version: "0.2"
opf_version: "0.2.4"
type: product-concept
opf_id: opf:tetris-ai-arena:contract:experience-quality
kind: contract
contract_type: experience-quality
title: "Tetris AI Arena product-wide experience quality"
scope: product
qualities: [operability, usability, clarity, readability, visual-cleanliness, consistency, experiential-character]
requirements:
  - operability=both agents play legal seeded matches through timed inputs and controls remain reliable
  - usability=an evaluator can run and compare the agents without setup knowledge
  - clarity=agent identity, fairness, score, and result are immediately distinguishable
  - readability=boards, metrics, and explanations remain legible at desktop and narrow viewport sizes
  - visual-cleanliness=the comparison has one dominant hierarchy without dashboard clutter
  - consistency=both competitors use the same vocabulary, metric treatment, spacing, and control rules
  - experiential-character=the product feels like a fair visible experiment rather than a staged demonstration
assurance: hybrid
proof: opf:tetris-ai-arena:acceptance:heuristic-beats-random
verified:
  by: agent:codex
  method: "project-wide quality contract derived from the validated seeded arena"
---

# Tetris AI Arena experience quality

This contract governs the whole product experience rather than any single screen or implementation.
