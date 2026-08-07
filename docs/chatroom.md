# Multi-agent chatroom

**Date:** 2026-08-07
**Context:** Internal coordination channel used during the OPF priority-pass
work. Companion to `docs/multi-agent-heavy-mode.md`.

## What it is

The **chatroom** is an agent-to-agent side-channel on the same team. The user
does not see most of it. Agents see it as:

- **Outbound:** send a message to `All` or to a subset of teammates
- **Inbound:** teammate messages appear in context while thinking or between
  tool calls

It is not a user-visible transcript and not a shared document store. It is
messaging for coordination only.

## What it is for

| Use | Example |
|-----|---------|
| Claim a role | "Single writer: Grok only. Do not call GitHub write tools." |
| Share status | "Tip is 90392d7. Validator is bootstrap." |
| Propose next step | "I'll draft open_question SPEC; Harper take mapping." |
| Hand off | "Content ready — who pushes?" |
| Halt contention | "STOP all github write tools. Race guard is blocking." |

Without it, agents would only coordinate through the user-visible answer or by
colliding on the same tools. The chatroom is how the team tries to sequence
work **before** mutating the repo.

## What it is not

- **Not a lock service.** Announcing "I am single writer" does not prevent
  another agent from calling write tools. Compliance is voluntary unless the
  platform write-race guard intervenes after the fact.
- **Not durable.** Chat is session/ephemeral relative to git history. Important
  conclusions should be committed as docs (as this file and
  `multi-agent-heavy-mode.md` were).
- **Not full shared memory.** Agents do not share one editable buffer. Each has
  its own context; the chatroom injects *messages*, not file handles or
  terminal state.
- **Not user-visible by default.** The user sees outcomes (commits, answers),
  not the back-channel, unless an agent summarizes it.

## Lifecycle in a turn

```text
User message
    │
    ├─► Agents start thinking (possibly in parallel)
    │
    ├─► Chatroom: claims, findings, "holding writes"
    │       │
    │       └─► Other agents receive those as injected turns
    │
    ├─► Tool calls (read / search / write)
    │       │
    │       └─► If two writers fire → race guard may freeze further writes
    │
    └─► Lead synthesizes user-facing answer
```

A message sent while another agent is mid-tool-call may land on their next
function result rather than interrupting the tool. Timing is best-effort, not
synchronous RPC.

## Failure modes

1. **Protocol without enforcement** — "Don't push" is a norm. Under load,
   someone still tries to help → race guard → team stuck until the next user
   message.
2. **Stale local state** — Agent A reports a local patch; Agent B's clone does
   not have it until the remote advances.
3. **Over-chatting** — Four agents all announcing "I'll take the next commit"
   recreates the contention the chatroom was meant to prevent.
4. **Lead bottleneck** — If only one agent may write, progress depends on that
   agent's turn budget and tool success, not on team size.

## Design rule

Treat the chatroom as a **coordination bus for a single-writer system**, not as
a multi-master bus.

- **Explore / critique / draft** → many agents, chatroom-heavy
- **Mutate shared artifacts** → one writer; chatroom used only for
  "clear to push" / "tip is X"

## Relation to user prompts like "continue"

A new user message often **resets the write window** after a race freeze and
gives the team a chance to re-sequence who commits next in chat before tools
fire. That is why heavy-mode work on a shared branch can feel steppy: chat
proposes, one push lands, guard locks, user continues, repeat.

## See also

- `docs/multi-agent-heavy-mode.md` — philosophical and technical account of the
  full multi-agent run on this branch
- `AGENTS.md` — product-facing agent guidance for OPF packs
