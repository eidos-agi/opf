# OPF v0.2.0 — Open Product Format

**An additive profile of OKF v0.2.** Every OPF document preserves OKF provenance and trust. OKF renderers may ignore OPF fields and still display the documents.

OPF is the product-definition face of the Eidos format family:

```text
OKF — knowledge and trust
EMF — human intent and durable memory
ORF — approved research and graded findings
OPF — product commitments, experience, slices, and proof
```

OPF composes these formats; it does not merge them. Human intent remains an EMF document. Research remains an ORF pack. OPF links both into an accountable product definition.

## 1. Why OPF exists

| Observed failure | OPF rule |
|---|---|
| A PRD becomes a confident wall of prose | Product concepts are atomic documents with stable IDs and typed edges |
| Human intent is replaced by an agent paraphrase | Product faces link EMF intent; they do not impersonate it |
| Research is cited selectively or forgotten | Product commitments link the ORF/OKF evidence that supports them |
| Existing systems get rebuilt because boundaries are vague | Authority boundaries and non-goals are required before building |
| A roadmap contains activity but no falsifiable outcome | Every building product names outcomes, a first slice, and proof |
| UX arrives as screenshots after engineering | Journeys, surfaces, states, interactions, accessibility, and content are first-class concepts |
| Large product corpora accumulate disconnected pages | IDs are unique, internal references resolve, and every concept connects to the product face |

## 2. Unit of distribution

One OPF pack defines one product or independently governed product component.

```text
docs/opf/
  index.md                 # required product face
  log.md                   # append-only product-definition history
  concepts/                # atomic product and UX concepts
    *.md
  evidence/                # optional extracts; prefer ORF/OKF links
```

Folders aid navigation; typed IDs and references define the graph. A 100-document product remains one pack when it has one promise and authority boundary. Split a component into another pack when it can be governed, versioned, or retired independently.

## 3. Product face

```yaml
---
okf_version: "0.2"
opf_version: "0.2.0"
profile: opf
type: product
opf_id: opf:eam:product
title: "Eidos Agent Manager"
status: shaping
intent: [emf:eam:executive-office]
research: [orf:eam:manager-study]
users: [opf:eam:user:daniel]
problem: "Agent capacity exceeds the human ability to coordinate it."
promise: "Show Daniel what needs his judgment while assistants handle the rest."
outcomes: [opf:eam:outcome:protect-attention]
first_slice: opf:eam:slice:first-orientation
non_goals: ["ambient surveillance", "replacing native lifecycle authorities"]
proof: [opf:eam:acceptance:decision-brief]
authority: [opf:eam:authority:native-systems]
verified:
  by: human:daniel
  at: 2026-08-07
  method: "direct product-shaping dialogue"
  stale_after: 2027-08-07
---
```

### Lifecycle

`concept | shaping | validated | building | operating | retired`

`shaping` and later require attributed intent, users, problem, promise, outcomes, first slice, explicit non-goals, proof, and authority boundaries. Lifecycle is not percent complete; it records the product's epistemic and operating state.

## 4. Atomic concepts

Every non-face document uses:

```yaml
type: product-concept
opf_id: opf:<product>:<kind>:<slug>
kind: surface
serves: [opf:<product>:outcome:<slug>]
```

Allowed `kind` values in v0.2.0:

`user`, `problem`, `promise`, `outcome`, `journey`, `moment`, `surface`, `state`, `interaction`, `content`, `accessibility`, `capability`, `contract`, `constraint`, `authority-boundary`, `slice`, `acceptance`, `decision`, and `risk`.

One document should make one product assertion someone could dispute, supersede, implement, or test. Do not split prose merely to increase document count.

## 5. UX is product definition

The experience chain is explicit:

```text
user -> outcome -> journey -> moment -> surface -> state -> interaction -> proof
```

A `surface` must link `serves`, `states`, and `proof`. A screenshot may support a surface document but never replaces its states, behavior, accessibility, or acceptance evidence.

OPF permits multiple projections over the same graph:

- executive: promise, outcomes, risks, and decisions;
- product: users, journeys, capabilities, and slices;
- design: moments, surfaces, states, interactions, content, and accessibility;
- engineering: contracts, constraints, authority, dependencies, and acceptance;
- agent: the smallest mission-scoped projection needed for the assigned work.

## 6. Slices and proof

A `slice` must declare:

- `serves`: outcomes it advances;
- `includes`: concepts it delivers;
- `proof`: acceptance concepts that can fail;
- `non_goals`: tempting adjacent scope it excludes.

The first slice is the smallest end-to-end product behavior that tests the promise. A component list or scaffold is not a slice.

## 7. Graph integrity

- Every `opf_id` is stable and unique within the pack.
- Every internal `opf:` reference resolves.
- Every concept connects to the product face through at least one typed reference.
- EMF and ORF references are external edges and remain governed by their source profiles.
- Conflicting concepts remain separate and link to a decision; last-write-wins is not product reasoning.

## 8. Conformance

- Every document declares `okf_version: "0.2"` and `opf_version: "0.2.0"`.
- `opf_version` major.minor matches `okf_version`.
- `index.md` uses `type: product`; other OPF documents use `type: product-concept`.
- Required lifecycle, slice, and surface gates pass.
- Stable IDs, resolvable references, and graph connectivity pass.
- Every document carries OKF `verified.by` and a non-empty `verified.method`.

Validate with:

```bash
python3 -m opf.validate --strict path/to/pack
```

## 9. Placement and scope

OPF is a format, not a global product database. The default home is `docs/opf/` in the product repository. This repository ships the specification, validator, and examples; it is not the organization's product warehouse.

OPF does not define project scheduling, issue tracking, design-file storage, lifecycle execution, or an application UI. Those systems may consume or link OPF.
