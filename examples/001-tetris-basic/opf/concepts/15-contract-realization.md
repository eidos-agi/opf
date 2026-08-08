---
okf_version: "0.2"
opf_version: "0.2.3"
type: product-concept
opf_id: opf:tetris:contract:realization
kind: contract
contract_type: realization
title: "Behavioral realization of basic Tetris"
applies_to: opf:tetris:surface:game-board
fidelity: behaviorally-equivalent
dimensions: [interaction, deterministic-output]
proof: opf:tetris:acceptance:playable-session
verified:
  by: agent:codex
  method: "the example fixes play behavior but does not claim reference-faithful visual identity"
---

Implementations must preserve the playable session and deterministic rules; visual composition may vary.
