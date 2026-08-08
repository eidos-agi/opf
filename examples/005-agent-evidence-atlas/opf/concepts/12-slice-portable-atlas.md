---
okf_version: "0.2"
opf_version: "0.2.2"
type: product-concept
opf_id: opf:agent-evidence-atlas:slice:portable-atlas
kind: slice
title: "One portable source-backed evidence atlas"
serves: [opf:agent-evidence-atlas:outcome:maxims-understood]
includes: [opf:agent-evidence-atlas:journey:read-proof-chain]
proof: [opf:agent-evidence-atlas:acceptance:source-backed-atlas]
non_goals: ["live refresh", "warehouse", "custom chart runtime", "new simulation rules"]
verified:
  by: agent:codex
  method: "the canonical analytics reader already supplies the needed dashboard mechanics"
---

The slice adds a reproducible snapshot generator and one packaged HTML artifact, reusing all prior strategy code.
