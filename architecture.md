# Pager architecture

Pager is an incident-response agent swarm. Agents will watch a system, investigate a failure in parallel, and propose a fix. A human approves the fix before anything runs. The operator UI is already built. The agents are not.

The UI never talks to an agent. It reads Postgres and a Redis event stream. When the swarm exists, it will write the same tables and the same stream. The screens stay the same.

## What runs today

```
Browser (Next.js, :3000)
    |  REST + SSE
    v
FastAPI (:8000)
    |                |
    v                v
Postgres `pager`     Redis `pager:events`
```

`make dev` starts the API and the web app against Postgres and Redis already running on the host. Docker is not part of this loop.

| Piece | Where | Job |
|---|---|---|
| Operator UI | `web/` | Landing, login, board, approval, trace, audit, kill switch |
| API | `pager/api/` | Incidents, approvals, traces, audit, kill switch, SSE |
| Tables | `pager/storage/models.py` | The incident board the UI and the future swarm share |
| Events | `pager/storage/events.py` | Audit row, then a stream row, then a Redis publish |
| Demo data | `pager/dev/seed.py` | Ten incidents, one in every state |
| Live replay | `pager/dev/simulator.py` | One new incident played onto the feed |

Sign-in is local to the browser (`on-call` / `pager`). The API does not check it. The name is sent with an approval so the audit log can say who decided.

## How a screen gets its data

1. The page loads history with REST (`GET /api/incidents`, `GET /api/events`, and the rest).
2. `web/components/live.tsx` opens `GET /api/stream`.
3. The stream sends any events the browser missed (`Last-Event-ID`), then subscribes to Redis.
4. Each new event bumps a counter. The board and the open incident refetch.

An event is durable before it is live. `append_audit` writes an `audit_events` row and a `stream_events` row, then `publish` sends the same payload on `pager:events`. If Redis is down, a refresh still shows the row. The audit row stores `prev_hash` and `this_hash`, so the log can be checked later.

The seed writes history and does not publish. The simulator commits and publishes, which is why its lines appear on the board while it runs.

## The incident board

One incident owns the rows the operator reads:

```
Incident
  tasks          who is working, and on what
  findings       evidence, with a confidence
  hypotheses     open, supported, or refuted
  actions        the proposed fix, its tier, its rollback
  approvals      who said yes or no, and when
  traces         each step, tokens, cost, latency
```

`thread_id` on the incident is empty of meaning today. It is the id the LangGraph checkpointer will use so a restart can resume the same incident.

States, in order:

`DETECTED` → `INVESTIGATING` → `DIAGNOSED` → `AWAITING_APPROVAL` → `REMEDIATING` → `VERIFYING` → `RESOLVED`

Two exits sit beside that line. `ESCALATED` means a person has to take it. `CLOSED_NO_ACTION` means the incident ended without a fix.

## Approval

The gate lives in `pager/api/routes/approvals.py`. The UI posts Approve, Reject, or Investigate more. The same rules will resume the graph later.

- Approve and reject only apply while the incident is `AWAITING_APPROVAL`.
- Approve only applies to an action that is still `proposed`, and only if `action_version` matches. A changed proposal cannot reuse an old yes.
- T1 is one click. T2 needs the operator to type the confirmation phrase (`rollback api` on `INC-1048`). T3 is refused.
- Reject needs a reason. The incident goes back to `DIAGNOSED`.
- Investigate more sends it back to `INVESTIGATING` and leaves the action proposed.
- The kill switch (`kill_switch` id `1`) blocks approve. The header shows a banner while it is on.

Illegal transitions are written to the audit log, then rejected.

## The swarm

`make investigate` (or `POST /api/runs`) injects a fault into an in-process target and runs the LangGraph incident graph. The graph writes the same tables as the seed. Docker is still later.

```
pager/target/     world + scenarios (the cause stays out of the prompt)
pager/tools/      registry. Every call is validated, then authorized
pager/safety/     tiers, allowlist, kill switch, budgets, untrusted wrap
pager/graph/      StateGraph, parallel investigators, interrupt, resume
```

```
triage
  -> investigators (logs, metrics, git, infra)
  -> diagnostician
  -> planner
  -> interrupt()          # AWAITING_APPROVAL
  -> executor             # only if the approval row is still valid
  -> verify
```

The tier comes from the registry, not from the model. Read tools are T0. A restart is T1. A rollback or config change is T2. `drop_database` and anything off the allowlist is refused before a handler runs. Log text is wrapped and labeled as data. The executor loads the action from Postgres and runs it only when `approval_holds` is true: right version, right tier, kill switch off, and the T2 phrase matches.

Approving on the board is the same API as before. If the incident has a paused checkpoint, the API resumes the graph after it writes the approval.

The model is swappable. `ScriptedModel` reads tool output and proposes a fix with no API key. `OpenAIModel` calls the OpenAI Responses API when `OPENAI_API_KEY` is set and `PAGER_MODEL=openai`. The default model is `gpt-6.1-sol`.

Checkpoints live in Postgres (`PostgresSaver`). A restart can resume the same `thread_id`.

Still to build: a containerized target, the eval runner, and the single-agent baseline.

## Layout

```
pager/
  api/            HTTP and SSE
  storage/        models, audit, Redis publish
  dev/            Faker seed, catalog, simulator
  safety/         gates the tool nodes call
  tools/          registry and handlers
  target/         in-process system and faults
  graph/          LangGraph incident lifecycle
web/              Next.js operator UI
```
