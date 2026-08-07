# Open Product Format

OPF is an additive profile of OKF v0.2 for defining products as linked, testable concepts rather than monolithic PRDs.

```text
OKF — knowledge and trust
EMF — human intent and durable memory
ORF — research and findings
OPF — product commitments, UX, slices, and proof
```

OPF keeps human intent in EMF and research in ORF. It links to those sources, then records the product promise, outcomes, constraints, experience, first slice, and falsifiable proof.

```bash
python3 -m opf.validate --selftest
python3 -m opf.validate --strict examples/eidos-agent-manager
```

See [SPEC.md](SPEC.md) and the [Eidos Agent Manager example](examples/eidos-agent-manager/index.md).
