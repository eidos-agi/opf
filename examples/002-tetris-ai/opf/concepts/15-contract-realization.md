---
okf_version: "0.2"
opf_version: "0.2.3"
type: product-concept
opf_id: opf:tetris-ai:contract:realization
kind: contract
contract_type: realization
title: "Behavioral realization of the placement agent"
applies_to: opf:tetris-ai:surface:placement-laboratory
fidelity: behaviorally-equivalent
dimensions: [interaction, explanation-semantics, deterministic-output]
proof: opf:tetris-ai:acceptance:autonomous-session
verified:
  by: agent:codex
  method: "the example fixes agent behavior and visible rationale without a visual reference artifact"
---

Implementations must preserve legal physical play and the meaning of the visible decision explanation; visual composition may vary.
