---
okf_version: "0.2"
opf_version: "0.2.2"
type: product-concept
opf_id: opf:tetris:slice:playable-browser-game
kind: slice
title: "One complete local browser session"
serves: [opf:tetris:outcome:complete-lines]
includes: [opf:tetris:journey:play-session]
proof: [opf:tetris:acceptance:playable-session]
non_goals: ["accounts", "leaderboards", "multiplayer", "network persistence"]
verified:
  by: agent:codex
  method: "minimum implementation that fulfills the requested product"
---

The slice is complete when the core loop can be played repeatedly on desktop and touch-sized screens.
