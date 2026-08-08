---
okf_version: "0.2"
opf_version: "0.2.5"
profile: opf
type: product
opf_id: opf:tetris-smart-arena:product
title: "Tetris Smart Arena"
status: validated
imports: [emf:tetris-smart-arena@2026-08-07]
intent: [emf:tetris-smart-arena:show-smarter-agent@2026-08-07]
users: [opf:tetris-smart-arena:user:evaluator]
problem: opf:tetris-smart-arena:problem:hidden-intelligence-gap
promise: opf:tetris-smart-arena:promise:visible-foresight
outcomes: [opf:tetris-smart-arena:outcome:explain-superiority]
first_slice: opf:tetris-smart-arena:slice:depth-duel
non_goals: ["model inference", "learning", "unknown-piece prediction", "perfect play", "teleporting pieces"]
proof: [opf:tetris-smart-arena:acceptance:lookahead-wins]
validation: [opf:tetris-smart-arena:acceptance:lookahead-wins]
authority: [opf:tetris-smart-arena:authority:local-evaluator]
realization: [opf:tetris-smart-arena:contract:realization]
experience_quality: [opf:tetris-smart-arena:contract:experience-quality]
verified:
  by: human:daniel
  at: 2026-08-07
  method: "explicit request for example 004 with two smart agents, one smarter, and an explanation of how"
---

# Tetris Smart Arena

A controlled duel that makes one extra level of planning visible and tests whether it improves results.
