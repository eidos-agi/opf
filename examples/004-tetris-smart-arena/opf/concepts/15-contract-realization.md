---
okf_version: "0.2"
opf_version: "0.2.4"
type: product-concept
opf_id: opf:tetris-smart-arena:contract:realization
kind: contract
contract_type: realization
title: "Experience-equivalent realization of the smart arena"
applies_to: opf:tetris-smart-arena:surface:thought-duel
fidelity: experience-equivalent
dimensions: [visual-composition, content, interaction-timing, explanation-semantics, deterministic-output]
references: [file:references/desktop-1440x1400.png@sha256-2494f0d5f29f4ea4522f4831e08b5cacda597ea94f2dcfaae0d86b3866ac8802, file:references/realization-oracle.json@sha256-b91589f41eb36ed2e17882951e911c9309405f4dac82a627147c1469acac6ae5]
proof: opf:tetris-smart-arena:acceptance:lookahead-wins
verified:
  by: agent:codex
  method: "blind reconstruction proved that product experience can remain faithful without byte or pixel identity"
---

A conforming realization must preserve the project-wide experience-quality contract and the structured semantic oracle. The pinned screen is a design oracle, not a pixel-identity requirement.
