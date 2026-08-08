---
okf_version: "0.2"
opf_version: "0.2.3"
type: product-concept
opf_id: opf:tetris-smart-arena:contract:realization
kind: contract
contract_type: realization
title: "Reference-faithful realization of the smart arena"
applies_to: opf:tetris-smart-arena:surface:thought-duel
fidelity: reference-faithful
dimensions: [visual-composition, content, interaction-timing, explanation-semantics, deterministic-output]
references: [file:references/desktop-1440x1400.png@sha256-2494f0d5f29f4ea4522f4831e08b5cacda597ea94f2dcfaae0d86b3866ac8802, file:references/realization-oracle.json@sha256-b91589f41eb36ed2e17882951e911c9309405f4dac82a627147c1469acac6ae5]
tolerances: ["font rasterization and device pixel ratio may vary; layout, palette, labels, explanation semantics, timing, and deterministic oracle values may not"]
proof: opf:tetris-smart-arena:acceptance:lookahead-wins
verified:
  by: agent:codex
  method: "blind reconstruction exposed that behavioral acceptance alone did not preserve the shipped product"
---

A conforming realization must match the pinned screen composition and the structured semantic oracle, not merely exceed performance thresholds.
