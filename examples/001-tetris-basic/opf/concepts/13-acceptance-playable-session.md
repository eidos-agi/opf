---
okf_version: "0.2"
opf_version: "0.2.3"
type: product-concept
opf_id: opf:tetris:acceptance:playable-session
kind: acceptance
title: "The basic session is playable"
condition: "Fail if pieces do not fall, legal controls do not move or rotate them, complete rows do not clear and score, game over does not stop play, or restart does not begin a clean session."
status: observed
evidence: [file:evidence/playable-session.json@sha256-2a67fcf3a7f41ce24f0892c0a19c9af232a94afdbe9ee9fc14f0fc7e77755ed3]
verified:
  by: agent:codex
  method: "falsifiable first-slice acceptance derived before implementation"
---

The implementation passed its game-core checks and desktop/mobile browser exercise.
