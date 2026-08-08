---
okf_version: "0.2"
opf_version: "0.2.3"
profile: opf
type: product
opf_id: opf:tetris-ai:product
title: "Tetris Placement Agent"
status: validated
imports: [emf:tetris-ai@2026-08-07]
intent: [emf:tetris-ai:autonomous-player@2026-08-07]
users: [opf:tetris-ai:user:placement-agent]
problem: opf:tetris-ai:problem:opaque-placement
promise: opf:tetris-ai:promise:visible-autoplay
outcomes: [opf:tetris-ai:outcome:legal-session]
first_slice: opf:tetris-ai:slice:heuristic-browser-agent
non_goals: ["model training", "network inference", "perfect play", "multiplayer", "changing the 001 game engine"]
proof: [opf:tetris-ai:acceptance:autonomous-session]
validation: [opf:tetris-ai:acceptance:autonomous-session]
authority: [opf:tetris-ai:authority:local-browser]
realization: [opf:tetris-ai:contract:realization]
verified:
  by: human:daniel
  at: 2026-08-07
  method: "explicit request for example 002, an AI that plays the game"
---

# Tetris Placement Agent

A deterministic agent that exposes its decision and plays the shared Tetris engine without human placement input.
