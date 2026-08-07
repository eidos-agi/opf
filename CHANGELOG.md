# Changelog

## Unreleased — 0.2.2 (fixes/priority-pass)

- Add MIT LICENSE file.
- Document Trilogy ↔ OPF mapping (docs/trilogy-opf-mapping.md).
- Add stable error codes OPF-E001..E047 (opf/codes.py, docs/error-codes.md);
  Problem.code exposed on validator problems.
- Design notes for 0.2.2: open_question, validation coverage, headless topology.
- Bootstrap validate.py from ca9cc72 with error-code wiring after truncated
  multi-agent pushes (temporary; replace with in-tree source).

## 0.2.1 — 2026-08-07

- Replace undirected connectivity with directed composition reachability and target-kind checks.
- Give lifecycle states distinct evidence gates and require a complete first-slice experience path.
- Add pinned external imports, explicit supersession, fail-closed parsing, and adversarial fixtures.

## 0.2.0 — 2026-08-07

- Define Open Product Format as an additive OKF v0.2 profile.
- Add a dependency-free validator with lifecycle, graph, slice, and UX gates.
- Add a connected Eidos Agent Manager example pack.
