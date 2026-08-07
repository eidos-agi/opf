---
okf_version: "0.2"
opf_version: "0.2.1"
profile: opf
type: product
opf_id: opf:tetris:product
title: "Basic Tetris"
status: shaping
imports: [emf:tetris@2026-08-07]
intent: [emf:tetris:basic-browser-game@2026-08-07]
users: [opf:tetris:user:solo-player]
problem: opf:tetris:problem:idle-play
promise: opf:tetris:promise:immediate-play
outcomes: [opf:tetris:outcome:complete-lines]
first_slice: opf:tetris:slice:playable-browser-game
non_goals: ["accounts", "leaderboards", "multiplayer", "network services", "advanced scoring variants"]
proof: [opf:tetris:acceptance:playable-session]
authority: [opf:tetris:authority:local-browser]
verified:
  by: human:daniel
  at: 2026-08-07
  method: "explicit request to use OPF to build a basic Tetris"
---

# Basic Tetris

A dependency-free browser game that proves an OPF first slice can drive a small implementation.
