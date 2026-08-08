# Open Product Format

OPF is an additive profile of OKF v0.2 for defining products as linked, testable concepts rather than monolithic PRDs.

```text
OKF — knowledge and trust
EMF — human intent and durable memory
ORF — research and findings
OPF — product commitments, UX, slices, and proof
```

OPF keeps human intent in EMF and research in ORF. It links pinned revisions of those sources, then records the product promise, outcomes, constraints, directed experience, first slice, and falsifiable proof.

OPF v0.2.5 makes realization fidelity and project-wide experience quality explicit. A pack must say whether a build is intent-equivalent, behaviorally equivalent, experience-equivalent, or reference-faithful. It must also define and prove operability, usability, clarity, readability, visual cleanliness, consistency, and experiential character across the product—not merely reproduce bytes or pixels. Human or hybrid quality proof names the reviewer, reviewed surfaces, and pinned build revision.

```bash
python3 -m opf.validate --selftest
PYTHONPATH=. python3 -m unittest discover -s tests -q
python3 -m opf.validate --strict examples/eidos-agent-manager
# all example packs:
# for p in examples/*/opf examples/eidos-agent-manager; do
#   [ -f "$p/index.md" ] && python3 -m opf.validate --strict "$p"
# done
```

Strict validation enforces typed target kinds, directed product reachability, distinct lifecycle gates, a complete first-slice UX path, project-wide experience-quality coverage and proof, pinned evidence and external imports, and explicit supersession.

See [SPEC.md](SPEC.md) and the [Eidos Agent Manager example](examples/eidos-agent-manager/index.md).
