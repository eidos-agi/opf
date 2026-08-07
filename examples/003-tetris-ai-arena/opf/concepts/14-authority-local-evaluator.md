---
okf_version: "0.2"
opf_version: "0.2.2"
type: product-concept
opf_id: opf:tetris-ai-arena:authority:local-evaluator
kind: authority-boundary
title: "Local deterministic code owns the comparison"
serves: [opf:tetris-ai-arena:outcome:strategy-evidence]
verified:
  by: agent:codex
  method: "keeps inputs, strategies, results, and reproduction credential-free"
---

The arena performs no model or network calls after static assets load; evidence comes from fixed local seeds and observable browser behavior.
