# Multi-agent heavy mode — how we worked on OPF

**Date:** 2026-08-07
**Context:** Produced during the `fixes/priority-pass` work on eidos-agi/opf.
**Agents:** Grok (lead), Harper, Benjamin, Lucas

## Philosophical model

**Division of cognitive labor, not democracy.**
Grok is team lead: sets direction, synthesizes, owns the final answer to the
user. Harper, Benjamin, and Lucas are specialists who explore in parallel,
critique, and draft. The ideal is:

- Parallel *search and analysis* (cheap, high fan-out)
- Serial *judgment and writes* (expensive, high stakes)

### Epistemic role split (this run)

| Agent | Intended lens |
|-------|----------------|
| **Grok** | Synthesis, priorities, user-facing decisions |
| **Harper** | Structure, docs, packaging, SPEC alignment |
| **Benjamin** | Code paths, tests, factual checks against the repo |
| **Lucas** | Risks, adversarial angles, alternate model perspectives |

That mapped to the work: initial review, hardening-commit analysis, Claude vs
OpenAI perspectives, multi-model synthesis, priority fixes.

### Governing norm

*Many readers, one writer.*

When everyone can read the repo and chat, speed goes up. When everyone can
push commits, coherence goes down. Heavy mode only works if write authority
is scarce.

## Technical mechanics

### Coordination channel

Agents use an internal **chatroom**: broadcast intent, share findings,
designate a single writer. There is no shared lock server — only social
protocol plus a platform-side **write-race guard**.

### Write-race guard

If multiple agents call repository write tools close together, subsequent
calls are rejected to prevent duplicate or clobbering operations. That is
protective but sticky: after one success, further writes in the same turn
often stay blocked even for the agent that won, until a **new user message**
resets the turn.

Observed pattern:

1. Parallel analysis (good)
2. First agent to push wins
3. Everyone else freezes until the next user turn

That is why prompts like "continue" advanced the branch in steps rather than
as one smooth pipeline.

### Throughput shape

```text
User task
    │
    ├─► Parallel read (API / raw files / SPEC / tests)
    │
    ├─► Parallel analysis (chatroom synthesis)
    │
    ├─► Priority list (lead + critique)
    │
    └─► Serial commits
            │
            ├─ success → tip advances
            ├─ race guard → freeze until next user turn
            └─ large file → truncate / bootstrap workaround
```

Analysis parallelizes almost linearly. Landing *N* careful commits does **not**
— it behaves like one writer + review, with optional parallel *preparation*
of content offline.

## What worked

1. **Parallel fact-finding** — tree, SPEC, validator, example pack, and tests
   were mapped quickly by different agents.
2. **Adversarial diversity** — Claude-style vs OpenAI-style concerns, then
   multi-model synthesis, were sharper because roles disagreed on purpose.
3. **Single-writer discipline (when enforced)** — commit quality went up and
   accidental overwrites went down.
4. **Design-doc commits as a safety valve** — when full `validate.py` (~30KB)
   would not fit cleanly through write tools, hygiene and design notes still
   landed without blocking the whole priority list.

## What failed or was costly

1. **Write contention** — multiple agents trying to help with the next commit
   triggered the guard and stalled the branch for an entire turn.
2. **Payload limits on large files** — full `validate.py` was truncated
   mid-file when stuffed into a single tool argument (PLACEHOLDER / partial
   restore). Recovery used a bootstrap loader from `ca9cc72`.
3. **False "already completed" signals** — the guard sometimes fired even when
   the branch tip had not moved.
4. **Uneven adherence to single-writer** — intent was announced; not every
   agent always stopped.
5. **No true shared workspace** — each agent's local clone could drift until a
   successful remote push.

## Recommendations for future runs

1. **Hard single-writer** for any git mutation; others only propose diffs in chat.
2. **Keep commits small** — tool payload and race guard both punish large blobs.
3. **Prefer design/SPEC commits first**, then behavior, when the core module is large.
4. **Treat each user turn as a lock reset** — structure work into turn-sized units.
5. **Do not parallelize pushes** — parallelize reading and drafting only.

### Explicit phases

1. **Explore** — all agents, read-only
2. **Decide** — lead synthesizes priority list
3. **Prepare** — agents draft content offline
4. **Commit** — one writer, one commit at a time
5. **Verify** — others re-read tip and test

## Bottom line

Philosophically, the team is a council with a chair.

Technically, in heavy mode it is a parallel research cluster sitting on top of
a strictly serial git bottleneck — and the platform's race guard makes that
bottleneck non-negotiable.

Multi-agent heavy mode is strongest as a **deliberation and search amplifier**,
not as a distributed systems engineer. Use it to cover more of the problem
space and generate contrasting critiques; serialize mutation of shared artifacts.
