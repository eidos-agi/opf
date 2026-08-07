# Open Product Format

OPF is an additive profile of OKF v0.2 for defining products as linked, testable concepts rather than monolithic PRDs.

```text
OKF — knowledge and trust
EMF — human intent and durable memory
ORF — research and findings
OPF — product commitments, UX, slices, and proof
```

OPF keeps human intent in EMF and research in ORF. It links pinned revisions of those sources, then records the product promise, outcomes, constraints, directed experience, first slice, and falsifiable proof.

```bash
python3 -m opf.validate --selftest
python3 -m unittest -q tests.test_validate
python3 -m opf.validate --strict examples/eidos-agent-manager
```

Strict validation enforces typed target kinds, directed product reachability, distinct lifecycle gates, a complete first-slice UX path, pinned evidence and external imports, and explicit supersession.

See [SPEC.md](SPEC.md) and the [Eidos Agent Manager example](examples/eidos-agent-manager/index.md).
