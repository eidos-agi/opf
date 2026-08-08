---
okf_version: "0.2"
opf_version: "0.2.3"
type: product-concept
opf_id: opf:tetris-ai-arena:journey:watch-and-evaluate
kind: journey
title: "Watch a fair match and verify the result across seeds"
actor: opf:tetris-ai-arena:user:evaluator
outcome: opf:tetris-ai-arena:outcome:strategy-evidence
moments: [opf:tetris-ai-arena:moment:compare-same-piece]
surfaces: [opf:tetris-ai-arena:surface:same-bag-arena]
verified:
  by: agent:codex
  method: "the visible match explains the behavior and the evaluator measures it"
---

The evaluator sees both agents act, then can reproduce the aggregate result outside the browser animation.
