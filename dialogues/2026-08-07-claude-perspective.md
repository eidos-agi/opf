# What Claude would likely be concerned about with OPF (v0.2.1)

**Date:** 2026-08-07  
**Framing:** Characteristic concerns from a Claude / Anthropic-style perspective (human control, constitutional alignment, avoiding false confidence, calibrated uncertainty).

Claude’s concerns would come from a characteristic place: preserving meaningful human control, avoiding false confidence in structured systems, and noticing the gap between a clean static definition and actual agent behavior under pressure. It would not reject the project—in fact it would recognize the design as unusually thoughtful—but it would surface several careful, structural worries.

## 1. False confidence from mechanical validity

The directed composition graph, typed edges, complete experience-path check, lifecycle gates, and fail-closed parser are rigorous. Claude would worry that “the pack validates under `--strict`” becomes a substitute for ongoing human judgment. Agents (and people) can start treating a green validation as evidence that the product definition is *true*, *complete*, or *safe to act on*, rather than merely *well-formed according to the current rules*. Structure can create an illusion of settled knowledge.

## 2. Human intent can still be diluted in practice

OPF does the right things on paper: pinned EMF imports, explicit refusal to let agents restate human intent, non-goals, authority boundaries. Claude would still ask how robust this is once agents are the primary authors or expanders of the graph. Selective linking, subtle reframing of outcomes, or quiet pressure to reinterpret “non-goals” under delivery pressure remain possible. The format makes the right things *expressible*; it does not by itself make them *enforced*.

## 3. Premature completeness pressure

Requiring a mechanically complete first-slice experience path (`journey → moment → surface → state → interaction → proof`) for any status beyond `concept` is strong engineering. Claude would note the risk that early product thinking gets forced into fully specified interactions and states before the team actually understands the problem. This can produce either bureaucratic over-specification or gaming of the required shape.

## 4. Auditability of dense graphs

A 100-document pack with many directed edges is machine-checkable. It is not necessarily human-auditable at a glance. Claude tends to care about whether a careful human can still understand and challenge the product definition without specialized tooling. Dense, high-quality graphs can become opaque even when they are formally correct.

## 5. The static-vs-runtime gap

OPF is a definition and validation format. Claude would emphasize that nothing in the pack guarantees the running agents will actually respect the authority boundaries, non-goals, or acceptance criteria under distribution shift, tool failure, prompt injection, or competing incentives. Formats describe what *should* be true; containment and oversight live in the runtime and the human processes around it.

## 6. Agent-authored or agent-expanded packs

If agents write or significantly expand OPF documents, Claude would be attentive to self-reinforcing loops, subtle goal drift across supersession lineages, and the possibility of adversarially constructed but still validating graphs. The bidirectional supersession rules and single-live-head constraint help, but they do not eliminate the risk.

## 7. Falsifiability can become theater

The `proposed` / `observed` / `failed` acceptance statuses and required evidence for observed/failed are excellent. Claude would still watch for the common failure mode: many “proposed” criteria that never get real evidence, or evidence that is thin/performative. The format supports real accountability; it does not automatically produce it.

## What Claude would *not* be especially worried about

- The zero-dependency, fail-closed, stdlib-only design (it would see this as careful and restrained).
- The explicit philosophy of “add a rule only for an observed failure.”
- The separation of EMF / ORF / OPF rather than merging everything into one mega-format.
- The existence of authority boundaries and non-goals as first-class concepts.

## Overall Claude posture

Claude would treat OPF as a serious attempt at the right layer of the stack (product governance before agent action) and would view the rapid hardening in 0.2.1 as encouraging. Its characteristic note would be something like:

> This is unusually careful about human intent, authority, and falsifiability. Structure of this quality is valuable, but it is not a substitute for ongoing human oversight, runtime enforcement of boundaries, and calibrated refusal to act when the definition is incomplete or the evidence is thin. Formats help; they do not close the loop by themselves.

That combination of respect for the design + insistence on the remaining human and runtime gaps is the most distinctive Claude-shaped concern set.
