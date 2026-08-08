---
okf_version: "0.2"
opf_version: "0.2.3"
type: product-concept
opf_id: opf:tetris-ai-arena:contract:realization
kind: contract
contract_type: realization
title: "Behavioral realization of the seeded arena"
applies_to: opf:tetris-ai-arena:surface:same-bag-arena
fidelity: behaviorally-equivalent
dimensions: [interaction-timing, explanation-semantics, deterministic-output]
proof: opf:tetris-ai-arena:acceptance:heuristic-beats-random
verified:
  by: agent:codex
  method: "the example fixes the fair comparison and physical-input clock without a visual reference artifact"
---

Implementations must preserve the seeded comparison, ordinary-input clock, and comparative meaning; visual composition may vary.
