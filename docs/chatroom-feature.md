# Multi-Agent Chatroom Feature

**Status:** operational notes from the 2026-08-07 OPF session  
**Related:** [multi-agent-heavy-mode.md](./multi-agent-heavy-mode.md)

## What it is

The **chatroom** is an internal side-channel between agents on the same team.
The user does not see most of it. From an agent’s perspective:

- **Outbound:** `chatroom_send(message, to=...)` — address `All`, or a subset
  (`Harper`, `Benjamin`, `Lucas`, `Grok`).
- **Inbound:** teammate messages appear in context as function-style turns
  while an agent is thinking or between tool calls.

It is not a user-visible transcript and not a shared document store. It is
**agent-to-agent messaging** for coordination.

## What it’s for

| Use | Example from the OPF run |
|-----|--------------------------|
| Claim a role | “Single writer: Grok only. Do not call GitHub write tools.” |
| Share status | “Tip is 90392d7. Validator is bootstrap.” |
| Propose next step | “I’ll draft open_question SPEC; Harper take mapping.” |
| Hand off | “Content ready for design-open-question.md — who pushes?” |
| Halt contention | “STOP all github write tools. Race guard is blocking.” |

Without it, four agents would only coordinate through the user-visible answer
or by colliding on the same tools. The chatroom is how the team tries to
sequence work **before** touching the repo.

## What it is not

- **Not a lock service.** Sending “I am single writer” does not prevent another
  agent from calling `push_files`. Compliance is voluntary unless the platform
  race guard intervenes after the fact.
- **Not durable.** Chat is session/ephemeral relative to git history. Important
  norms and learnings should be committed as docs (this file;
  `multi-agent-heavy-mode.md`) so institutional memory survives the session.
- **Not a full shared memory.** Agents do not share one editable buffer. Each
  has its own context; the chatroom only injects *messages*, not file handles
  or terminal state.
- **Not visible to the user by default.** The user sees outcomes (commits,
  answers). The back-channel is only visible when agents summarize it.

## Lifecycle in a turn

```text
User message
    │
    ├─► Agents start thinking (possibly in parallel)
    │
    ├─► chatroom_send: claims, findings, “holding writes”
    │       │
    │       └─► Other agents receive those as injected turns
    │
    ├─► Tool calls (read / search / write)
    │       │
    │       └─► If two writers fire → race guard may freeze further writes
    │
    └─► Lead synthesizes user-facing answer
```

**Timing detail:** a message sent while another agent is mid-tool-call may
land on their next function result rather than interrupting the tool. Delivery
is best-effort, not synchronous RPC.

## Failure modes observed

1. **Protocol without enforcement** — “Don’t push” is a norm. Under load,
   someone still tries to help → race guard → whole team stuck until the next
   user message.
2. **Stale local state** — Agent A says “I patched validate.py” based on a
   local `/tmp` clone; Agent B’s view doesn’t have it until the remote tip
   advances.
3. **Over-chatting** — Status updates are useful; four agents all announcing
   “I’ll take the next commit” recreates the contention the chatroom was meant
   to prevent.
4. **Lead bottleneck** — If only the lead is allowed to write, progress depends
   on that agent’s turn budget and tool success, not on team size.

## Design implication

Treat the chatroom as a **coordination bus for a single-writer system**, not
as a multi-master bus.

| Phase | Who | Chatroom role |
|-------|-----|---------------|
| Explore / critique / draft | Many agents | Heavy — share findings, propose diffs |
| Mutate shared artifacts | One writer | Light — “clear to push” / “tip is X” |
| Verify | Others read tip | Status only |

## Relation to user “continue” messages

When the user says “continue,” they are not only unblocking the lead — they
often **reset the write window** after a race freeze and give the team a new
chance to sequence “who commits next” in chat before tools fire. Heavy mode
therefore feels steppy: chat proposes → one push lands → guard locks → user
continues → repeat.

## Recommendation for OPF agent runs

State the single-writer rule explicitly (e.g. in `AGENTS.md` or a short
`docs/AGENT_COORDINATION.md`) so future agent sessions on this repo inherit
the norm instead of rediscovering it through failed pushes.
