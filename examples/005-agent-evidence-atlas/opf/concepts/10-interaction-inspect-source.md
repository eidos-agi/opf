---
okf_version: "0.2"
opf_version: "0.2.3"
type: product-concept
opf_id: opf:agent-evidence-atlas:interaction:inspect-source
kind: interaction
title: "Inspect the cohort source"
on: opf:agent-evidence-atlas:state:snapshot-ready
yields: opf:agent-evidence-atlas:outcome:maxims-understood
covered_by: opf:agent-evidence-atlas:acceptance:source-backed-atlas
verified:
  by: agent:codex
  method: "every quantitative component resolves to the cohort pipeline"
---

The reader can open the executable normalized snapshot query and its seed, ceiling, and metric definitions.
