---
okf_version: "0.2"
opf_version: "0.2.1"
type: product-concept
opf_id: opf:tetris-ai:authority:local-browser
kind: authority-boundary
title: "The local browser owns the autonomous run"
serves: [opf:tetris-ai:outcome:legal-session]
verified:
  by: agent:codex
  method: "keeps the first agent slice dependency-free and inspectable"
---

The run is local, credential-free, deterministic, and sends no network requests after its static assets load.

