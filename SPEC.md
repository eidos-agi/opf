# OPF v0.2.4 — Open Product Format

**An additive profile of OKF v0.2.** Every OPF document preserves OKF provenance and trust. OKF renderers may ignore OPF fields and still display the documents.

```text
OKF — knowledge and trust
EMF — human intent and durable memory
ORF — approved research and graded findings
OPF — product commitments, experience, slices, and proof
```

OPF composes these formats; it does not merge them. Human intent remains an EMF document. Research remains an ORF pack. OPF links pinned revisions of both into an accountable product definition.

## 1. Why OPF exists

| Observed failure | OPF rule |
|---|---|
| A PRD becomes a confident wall of prose | Product concepts are atomic documents with stable IDs and typed edges |
| Human intent is replaced by an agent paraphrase | Product faces link pinned EMF intent; they do not impersonate it |
| Research is cited selectively or forgotten | Product commitments link pinned ORF/OKF evidence |
| Existing systems get rebuilt because boundaries are vague | Authority boundaries and non-goals are required before shaping |
| A roadmap contains activity but no falsifiable outcome | Every active product names outcomes, one first slice, and acceptance proof |
| UX arrives as screenshots after engineering | The first slice contains a mechanically complete experience path |
| A rebuild passes behavioral tests but materially degrades the product | Every active product declares realization fidelity and a project-wide experience-quality contract with proof |
| Large product corpora accumulate connected sludge | Only directed composition edges make documents members of the product definition |

## 2. Unit of distribution

One OPF pack defines one product or independently governed product component.

```text
docs/opf/
  index.md                 # required product face
  log.md                   # append-only product-definition history
  concepts/                # atomic product and UX concepts
    *.md
  evidence/                # optional extracts; prefer pinned ORF/OKF links
  references/              # optional content-addressed realization oracles
```

Folders aid navigation; IDs and typed references define the graph. A 100-document product remains one pack when it has one promise and authority boundary. Split a component when it can be governed, versioned, or retired independently. Cross-pack targets must be declared in the face's `imports` closure.

## 3. Product face

```yaml
---
okf_version: "0.2"
opf_version: "0.2.4"
profile: opf
type: product
opf_id: opf:eam:product
title: "Eidos Agent Manager"
status: shaping
imports: [emf:eam@2026-08-07]
intent: [emf:eam:executive-office@2026-08-07]
users: [opf:eam:user:daniel]
problem: opf:eam:problem:coordination
promise: opf:eam:promise:executive-office
outcomes: [opf:eam:outcome:protect-attention]
first_slice: opf:eam:slice:first-orientation
non_goals: ["ambient surveillance", "replacing native lifecycle authorities"]
proof: [opf:eam:acceptance:decision-brief]
authority: [opf:eam:authority:native-systems]
realization: [opf:eam:contract:realization]
experience_quality: [opf:eam:contract:experience-quality]
verified:
  by: human:daniel
  at: 2026-08-07
  method: "direct product-shaping dialogue"
  stale_after: 2027-08-07
---
```

`problem` and `promise` are references, not duplicate inline authorities. Their documents may evolve and retain provenance independently.

### Lifecycle gates

| status | mechanical meaning |
|---|---|
| `concept` | named product face; incomplete structure allowed |
| `shaping` | intent, users, problem, promise, outcomes, first slice, non-goals, proof, authority, realization, and experience quality resolve; first experience path is complete |
| `validated` | shaping plus `validation` pointing to at least one `acceptance` with `status: observed` and pinned evidence |
| `building` | shaping contract admitted for implementation; the first slice remains complete and falsifiable |
| `operating` | building contract plus `operational_proof` pointing to observed acceptance |
| `retired` | `retirement_reason` required; historical product declarations remain readable |

Lifecycle is not percent complete. Placeholder values such as `TBD`, `TODO`, or `later` do not satisfy admission.

## 4. Atomic concepts and IDs

Every non-face document uses:

```yaml
type: product-concept
opf_id: opf:<product>:<kind>:<slug>
kind: surface
```

Allowed `kind` values:

`user`, `problem`, `promise`, `outcome`, `journey`, `moment`, `surface`, `state`, `interaction`, `content`, `accessibility`, `capability`, `contract`, `constraint`, `authority-boundary`, `slice`, `acceptance`, `decision`, and `risk`.

IDs match `opf:<product>:<kind>:<slug>` (additional stable segments are allowed), are unique in the validation closure, and never change after publication. A new interpretation gets a new ID and explicit `supersedes`; the old document names the new ID in `superseded_by`. Both edges are required, kinds must match, and one lineage may have only one live head.

One document makes one product assertion someone could dispute, supersede, implement, or test. Do not split prose merely to increase document count.

## 5. Directed typed edges

Field names are edge types. The validator checks both direction and target kind. Examples:

| source field | required target kind |
|---|---|
| `users` / `actor` | `user` |
| `problem` | `problem` |
| `promise` | `promise` |
| `outcomes` / `outcome` | `outcome` |
| `first_slice` | `slice` |
| `proof`, `covered_by`, `validation`, `operational_proof` | `acceptance` |
| `authority` | `authority-boundary` |
| `realization`, `experience_quality` | `contract` |
| `moments` | `moment` |
| `on_surface`, `surfaces`, `of_surface` | `surface` |
| `states` | `state` |
| `allows`, `interactions` | `interaction` |

Composition edges flow out from the face and from admitted product structures. Grounding and back-reference fields such as `serves`, `actor`, and `of_surface` do not make an otherwise disconnected document part of the product. This prevents a risk or note from passing merely because it points at a valid outcome.

## 6. UX is product definition

The minimum experience path is:

```text
user -> outcome -> journey -> moment -> surface -> state -> interaction -> outcome/proof
```

| kind | required semantics |
|---|---|
| `journey` | `actor`, `outcome`, and ordered `moments` |
| `moment` | `in_journey` and `on_surface` |
| `surface` | `surface_kind`, `serves`, `states`, and `proof` |
| `state` | `of_surface` plus `allows`, or `terminal: true` |
| `interaction` | `on`, `yields`, and `proof` or `covered_by` |
| `content` | `appears_on` |
| `accessibility` | `applies_to` and a nonempty `requirement` |

`surface_kind` is one of `screen`, `api`, `physical-control`, `device-output`, `voice`, `notification`, `document`, or `service`. This permits mobile, software, services, and physical products without storing design-system components in OPF.

Screenshots, Figma frames, CAD files, copy decks, analytics events, sensor logs, and WCAG audit bodies remain in their native systems. OPF records the product commitment and typed pointer, not the full artifact.

### Realization fidelity

Every active product face points through `realization` to at least one `contract`
with `contract_type: realization`. The contract covers the first-slice screen
surface through `applies_to` and states what a future implementation must preserve:

```yaml
kind: contract
contract_type: realization
applies_to: opf:arena:surface:duel
fidelity: reference-faithful
dimensions: [visual-composition, content, interaction-timing, explanation-semantics, deterministic-output]
references: [file:references/desktop.png@sha256-<64-lowercase-hex-digest>]
tolerances: ["font rasterization and device pixel ratio only"]
proof: opf:arena:acceptance:duel
```

`fidelity` is one of:

| value | claim |
|---|---|
| `intent-equivalent` | preserves the product purpose; realization remains open |
| `behaviorally-equivalent` | preserves the listed observable behavior; visual identity is not implied |
| `experience-equivalent` | preserves listed behavior and the project-wide experience-quality contract; byte and pixel identity are not implied |
| `reference-faithful` | preserves every listed dimension against pinned references within declared tolerances |

Allowed dimensions are `visual-composition`, `content`, `interaction`,
`interaction-timing`, `explanation-semantics`, `deterministic-output`,
`accessibility`, `performance`, and `physical-form`.

A `reference-faithful` contract requires content-addressed `references` and
nonempty `tolerances`. A screenshot alone does not define explanation semantics,
and a passing behavioral threshold does not define visual fidelity. Pin the
smallest set of visual, content, state, timing, and deterministic oracles needed
to make the listed dimensions independently testable. Repository-local references
use `file:references/<path>@sha256-<digest>` and may contain images, JSON, text, or
other stable artifacts. The validator checks containment and digest; the contract's
acceptance proof checks the realization against them.

### Project-wide experience quality

Every active product face also points through `experience_quality` to a contract
with `contract_type: experience-quality` and `scope: product`. This is the
whole-product quality bar, not a per-screen checklist:

```yaml
kind: contract
contract_type: experience-quality
scope: product
qualities: [operability, usability, clarity, readability, visual-cleanliness, consistency, experiential-character]
requirements:
  - operability=all primary paths work without invalid state
  - usability=a first-time user can complete the primary journey without instructions
  - clarity=purpose, state, choices, and consequences are immediately distinguishable
  - readability=content and controls remain legible across supported viewports
  - visual-cleanliness=the primary hierarchy dominates decorative material
  - consistency=vocabulary, visual roles, spacing, and interactions retain one system
  - experiential-character=the product feels calm, exact, and intentional rather than generic
assurance: hybrid
proof: opf:product:acceptance:first-slice
```

The validator requires all seven qualities and exactly one nonempty requirement
for each. `assurance` is `mechanical`, `human`, or `hybrid`; because experiential
character cannot be established honestly by syntax alone, a complete contract
must use human or hybrid assurance. For `validated` and `operating` products,
each experience-quality contract must point to observed acceptance proof. The
validator guarantees declared coverage, linkage, and proof status; the linked
human review supplies the judgment for experiential character.

## 7. Slices and acceptance

A `slice` declares:

- `serves`: outcomes it advances;
- `includes`: product concepts it delivers;
- `proof`: acceptance concepts that can fail;
- `non_goals`: tempting adjacent scope it excludes.

The face names exactly one `first_slice`. That slice must include a journey whose directed path resolves through moment, surface, state, and interaction to the declared journey outcome, with acceptance proof on the surface or interaction path. A component list or deployed scaffold does not satisfy this gate.

Acceptance documents require:

```yaml
kind: acceptance
condition: "A falsifiable sentence"
status: proposed       # proposed | observed | failed
evidence: [orf:pack:finding@revision]  # required for observed or failed
```

Evidence records an observation; it does not convert product direction into fact.
Repository-local executable proof may instead use a content-addressed receipt:

```yaml
evidence: [file:evidence/browser-proof.json@sha256-<64-lowercase-hex-digest>]
```

The path must remain beneath the pack's `evidence/` directory. The JSON receipt
must name `subject`, `observed_at`, `method`, `source_revision`, `result`, and a
nonempty `checks` list. Its subject must equal the acceptance ID, its result must
agree with `observed` or `failed`, and its SHA-256 digest must match the reference.
Local receipts are for same-repository mechanical proof; research claims still
belong in ORF or OKF.

## 8. External references

External references are pinned strings:

```text
emf:<pack>:<object>@<revision>
orf:<pack>:<object>@<revision>
okf:<pack>:<object>@<revision>
```

The product face declares the closure:

```yaml
imports: [emf:eam@2026-08-07, orf:manager-study@a1b2c3d]
```

`intent` accepts EMF only. `research` accepts ORF only. External `evidence` accepts ORF or OKF. Draft validation warns on unpinned or undeclared externals; `--strict` fails. v0.2.4 validates local evidence and reference content plus declared external pins, but does not fetch remote packs.

## 9. Validation modes and parser

Default mode is draft: all local structure, target kinds, directed reachability, lifecycle, experience, and supersession rules apply; external pin/import defects warn.

`--strict` additionally turns every warning into an error and requires all external references to be pinned and imported. Strict validation is the publication gate.

The validator accepts only the documented YAML subset: scalar values, inline scalar lists, indented scalar lists, and nested maps such as `verified`. Duplicate keys, tabs, multiline scalars, inline maps, lists of maps, and malformed lines fail closed. This restriction keeps the validator dependency-free and deterministic.

## 10. Conformance

- Every document declares `okf_version: "0.2"` and an OPF version on the `0.2.x` line.
- `index.md` uses `type: product`; other OPF documents use `type: product-concept`.
- Lifecycle, target-kind, first-slice, UX, acceptance, supersession, and parser gates pass.
- IDs are unique, internal references resolve, and every concept is reachable through directed composition edges.
- Every document carries OKF `verified.by` and a nonempty `verified.method`.
- Every active face declares realization fidelity, and each first-slice screen is covered by it.
- Every active face declares all seven project-wide experience qualities with human or hybrid assurance; validated and operating products link observed proof.
- Reference-faithful contracts pin local reference artifacts and state tolerances.
- Local evidence receipts are content-addressed, complete, and agree with their acceptance result.
- Strict validation has no warnings.

```bash
python3 -m opf.validate --strict path/to/pack
```

## 11. Placement and boundaries

OPF is a format, not a global product database, issue tracker, roadmap application, design tool, analytics store, runtime system, or execution log. The default home is `docs/opf/` in the product repository. This repository ships the specification, validator, fixtures, and examples; it is not the organization's product warehouse.

Issue trackers execute work. Design tools hold design artifacts. Runtime systems own live state. EMF owns human intent. ORF owns research. OPF owns the product commitments and typed links connecting those authorities.
