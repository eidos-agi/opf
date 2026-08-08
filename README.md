# Open Product Format

OPF is an additive profile of OKF v0.2 for defining products as linked, testable concepts rather than monolithic PRDs.

```text
OKF — knowledge and trust
EMF — human intent and durable memory
ORF — research and findings
OPF — product commitments, UX, slices, and proof
```

OPF keeps human intent in EMF and research in ORF. It links pinned revisions of those sources, then records the product promise, outcomes, constraints, directed experience, first slice, and falsifiable proof.

OPF v0.2.3 also makes realization fidelity explicit. A pack must say whether a build is intent-equivalent, behaviorally equivalent, or reference-faithful; only the last may claim faithful reconstruction, and it requires pinned visual or semantic oracles plus tolerances.

```bash
python3 -m opf.validate --selftest
PYTHONPATH=. python3 -m unittest discover -s tests -q
python3 -m opf.validate --strict examples/eidos-agent-manager
# all example packs:
# for p in examples/*/opf examples/eidos-agent-manager; do
#   [ -f "$p/index.md" ] && python3 -m opf.validate --strict "$p"
# done
```

Strict validation enforces typed target kinds, directed product reachability, distinct lifecycle gates, a complete first-slice UX path, pinned evidence and external imports, and explicit supersession.

See [SPEC.md](SPEC.md) and the [Eidos Agent Manager example](examples/eidos-agent-manager/index.md).
