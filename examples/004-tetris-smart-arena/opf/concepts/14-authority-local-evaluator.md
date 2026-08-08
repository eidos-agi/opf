---
okf_version: "0.2"
opf_version: "0.2.2"
type: product-concept
opf_id: opf:tetris-smart-arena:authority:local-evaluator
kind: authority-boundary
title: "Local deterministic code owns the duel"
serves: [opf:tetris-smart-arena:outcome:explain-superiority]
verified:
  by: agent:codex
  method: "keeps planning rules and evidence inspectable without credentials"
---

The comparison makes no model or network calls after static assets load and uses only fixed local seeds.
