# Design: headless product topology

**Status:** proposed for 0.2.2
**Priority:** 6 from multi-model review

## Problem

The first-slice experience path assumes a UX chain:

  user -> outcome -> journey -> moment -> surface -> state -> interaction -> proof

Headless products (agents, daemons, APIs, research systems) have no honest
surface or moment. Forcing dummy nodes produces the performative filler
the format exists to prevent. surface_kind already includes api and service,
but the experience-path gate still requires the full UX chain.

## Proposal

Support a second topology alongside the UX chain:

  system -> capability -> trigger -> action -> outcome/proof

### New optional kinds (or reuse)

| Kind | Role |
|---|---|
| capability | what the system can do |
| trigger | what initiates work (event, schedule, message) |
| action | the unit of behavior under a capability |

Existing kinds still apply: outcome, acceptance, authority-boundary, slice.

### First-slice gate (either topology)

A first_slice is complete if it includes a directed path that reaches
proof via either:

- UX: journey -> moment -> surface -> state -> interaction -> acceptance
- Headless: capability -> trigger -> action -> acceptance

The face (or slice) may declare `topology: ux | headless | hybrid`.
Default remains `ux` for backward compatibility.

## Migration

- Existing packs unchanged (default topology: ux).
- Headless packs set topology: headless and use the alternate path.
- Validator error experience_chain gains a clearer message naming which
  topology was expected.
