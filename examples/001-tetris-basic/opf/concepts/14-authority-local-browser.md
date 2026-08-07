---
okf_version: "0.2"
opf_version: "0.2.1"
type: product-concept
opf_id: opf:tetris:authority:local-browser
kind: authority-boundary
title: "The local browser owns the session"
serves: [opf:tetris:outcome:complete-lines]
verified:
  by: agent:codex
  method: "boundary chosen to keep the first slice dependency-free"
---

The game stores no account data, sends no network requests, and has no server-owned gameplay state.
