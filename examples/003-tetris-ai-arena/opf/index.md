---
okf_version: "0.2"
opf_version: "0.2.4"
profile: opf
type: product
opf_id: opf:tetris-ai-arena:product
title: "Tetris AI Arena"
status: validated
imports: [emf:tetris-ai-arena@2026-08-07]
intent: [emf:tetris-ai-arena:compare-agents@2026-08-07]
users: [opf:tetris-ai-arena:user:evaluator]
problem: opf:tetris-ai-arena:problem:unproven-superiority
promise: opf:tetris-ai-arena:promise:fair-visible-comparison
outcomes: [opf:tetris-ai-arena:outcome:strategy-evidence]
first_slice: opf:tetris-ai-arena:slice:seeded-arena
non_goals: ["model inference", "learning", "perfect play", "changing examples 001 or 002", "teleporting pieces"]
proof: [opf:tetris-ai-arena:acceptance:heuristic-beats-random]
validation: [opf:tetris-ai-arena:acceptance:heuristic-beats-random]
authority: [opf:tetris-ai-arena:authority:local-evaluator]
realization: [opf:tetris-ai-arena:contract:realization]
experience_quality: [opf:tetris-ai-arena:contract:experience-quality]
verified:
  by: human:daniel
  at: 2026-08-07
  method: "explicit approval to build example 003 after selecting a Tetris AI arena"
---

# Tetris AI Arena

A controlled arena that determines whether the example 002 heuristic actually outperforms a legal random baseline.
