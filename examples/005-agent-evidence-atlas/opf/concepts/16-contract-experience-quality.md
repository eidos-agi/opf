---
okf_version: "0.2"
opf_version: "0.2.4"
type: product-concept
opf_id: opf:agent-evidence-atlas:contract:experience-quality
kind: contract
contract_type: experience-quality
title: "Agent Evidence Atlas product-wide experience quality"
scope: product
qualities: [operability, usability, clarity, readability, visual-cleanliness, consistency, experiential-character]
requirements:
  - operability=every maxim, comparison, and source path can be inspected without broken navigation or hidden data
  - usability=a reader can move from claim to example to evidence without learning the implementation
  - clarity=maxims, findings, caveats, and source evidence remain visibly distinct
  - readability=prose, charts, labels, and tables remain legible at desktop and narrow viewport sizes
  - visual-cleanliness=the evidence hierarchy is dominant and ornament never obscures meaning
  - consistency=terminology, chart encodings, citations, spacing, and interactions retain one system
  - experiential-character=the product feels like a beautiful evidence atlas rather than a generic analytics dashboard
assurance: hybrid
proof: opf:agent-evidence-atlas:acceptance:source-backed-atlas
verified:
  by: agent:codex
  method: "project-wide quality contract derived from the validated source-backed atlas"
---

# Agent Evidence Atlas experience quality

This contract governs the whole product experience rather than any single screen or implementation.
