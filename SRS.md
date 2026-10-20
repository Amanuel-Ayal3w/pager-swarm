# Software Requirements Specification (SRS)

## Pager: An Incident-Response Agent Swarm

| Field | Value |
|---|---|
| Project name | Pager |
| Version | 0.1 (Draft) |
| Date | October 20, 2026 |
| Language / stack | Python 3.11+, LangGraph, Anthropic SDK, Pydantic, FastAPI, Postgres, Redis |
| Document status | Draft for review. Orchestration is LangGraph. State lives in Postgres. The live stream uses Redis on the host. Docker is deferred. |

---

## 1. Introduction

### 1.1 Purpose
This document specifies the requirements for **Pager**, a multi-agent system that monitors a running software system, detects incidents, investigates them in parallel, diagnoses root causes, and proposes remediation actions. A human must approve any action before it is executed.

### 1.2 Project Goals
1. Demonstrate a **LangGraph** multi-agent swarm. The incident lifecycle is a StateGraph, investigators fan out with Send, and the approval gate pauses on interrupt(). Safety (permission tiers, approvals, budgets, audit) is enforced in our own tool nodes, not in prompts.
2. Demonstrate **safe, human-in-the-loop** autonomy with permission tiers, approvals, and audit logging.
3. Provide **measurable evidence** (evals) that the swarm is accurate, safe, and cost-effective compared to a single agent.
4. Serve as a portfolio-quality project with a clear demo.

### 1.3 Scope
**In scope**
- A target system (containerized) that can be broken on demand.
- A fault injector with known root causes for grading.
- The agent harness, orchestrator, shared incident board, tool layer, and safety layer.
- Approval interfaces (CLI first, then web UI), live dashboard, and trace viewer.
- An evaluation suite and comparison report.

**Out of scope**
- Production deployment against real customer infrastructure.
- Multi-tenant authentication and user management beyond a single operator role.
- Support for cloud providers' native APIs (AWS, GCP, Azure) in v1.
- Fine-tuning or training of models.

### 1.4 Definitions and Acronyms

| Term | Definition |
|---|---|
| Agent | An LLM-driven worker running inside the harness with a defined role, prompt, tools, and budget |
| Harness | The loop that builds prompts, calls the model, executes tool calls, and enforces limits |
| Orchestrator | The component that manages incident lifecycle and coordinates agents |
| Incident board | Shared state where agents post tasks, findings, and hypotheses |
| Fault injector | A tool that deliberately causes a known failure in the target system |
| HITL | Human-in-the-loop |
| Blast radius | The set of services or users an action could affect |
| Ground truth | The known root cause of an injected fault, used for grading |
| SSE | Server-sent events |

### 1.5 References
- Anthropic API and SDK documentation (tool use)
- Model Context Protocol (optional tool integration)
- IEEE 830 / ISO/IEC/IEEE 29148 (structure guidance for this SRS)

---

## 2. Overall Description

### 2.1 Product Perspective
Pager is a standalone system composed of five parts:

1. **Target system:** a small Docker Compose environment (FastAPI API, Postgres, Redis, background worker) that produces logs and metrics.
2. **Fault injector:** triggers scenarios (memory leak, bad deploy, etc.) in the target system.
3. **Pager core:** harness, orchestrator, agents, tools, safety layer, and storage.
4. **Interfaces:** CLI, then a web UI (approval screen, live dashboard, trace viewer).
5. **Eval suite:** runs scenarios and produces comparison reports.

```
 Target System  <--- Fault Injector
      |
  logs/metrics
      v
 +------------------- Pager Core --------------------+
 | Triager -> Orchestrator <-> Incident Board        |
 |            |  Investigators (parallel)            |
 |            |  Diagnostician -> Planner            |
 |            |  Approval Gate -> Executor -> Scribe |
 +--------------------------------------------------+
      |  (events in Postgres, published on Redis)
      v
 CLI / Web UI (Approval, Dashboard, Traces)
```

### 2.2 Product Functions (Summary)
- Detect anomalies and open incidents.
- Run parallel investigations across logs, metrics, deploys, and infrastructure.
- Rank root-cause hypotheses with confidence scores.
- Propose remediation with risk, blast radius, and rollback plan.
- Require human approval before executing any non-read-only action.
- Verify recovery after remediation.
- Generate incident timeline and postmortem.
- Record complete traces and an audit log.
- Evaluate performance against injected faults.

### 2.3 User Classes

| User class | Description | Needs |
|---|---|---|
| Operator (on-call engineer) | Approves or rejects actions, reviews diagnoses | Clear evidence, risk info, fast decisions |
| Developer (project author) | Builds and tunes agents, runs evals | Traces, reproducible scenarios, metrics |
| Reviewer (hiring manager / viewer) | Watches demo or reads report | Clear narrative, visible safety, results |

### 2.4 Operating Environment
- Linux or macOS host. v1 development uses host Postgres and Redis. Docker is deferred until the target system needs it.
- Python 3.11+.
- Network access to the Anthropic API.
- Modern web browser for the web UI.

### 2.5 Design and Implementation Constraints
- **C-1:** Orchestration and agent loops run on LangGraph (`StateGraph`, `Send`, `interrupt`, Postgres checkpointer). Permission tiers, the allowlist, the kill switch, budgets, untrusted-input wrapping, and the audit log are project code enforced inside tool nodes.
- **C-2:** Model access via the Anthropic SDK using native tool use, called from LangGraph nodes.
- **C-3:** All data models validated with Pydantic.
- **C-4:** Persistent state stored in Postgres, including LangGraph checkpoints. Redis carries the live event stream. v1 development runs both on the host. Docker is deferred until the target system needs it.
- **C-5:** Any code or command execution happens only inside the target system's containers, never on the host directly.
- **C-6:** Log and metric content is treated as **untrusted input**.

### 2.6 Assumptions and Dependencies
- The Anthropic API is available and the API key is provided via environment variable.
- The target system is local and disposable.
- Fault scenarios have a single, well-defined root cause (v1).
- Model behavior may vary; evals are run multiple times where feasible.

---

## 3. System Features and Functional Requirements

Priority key: **M** = Must, **S** = Should, **C** = Could.

### 3.1 Target System and Fault Injection

| ID | Requirement | Priority |
|---|---|---|
| FR-1.1 | The system shall provide a Docker Compose target environment with an API service, Postgres, Redis, and a worker. | M |
| FR-1.2 | Each target service shall write structured logs to a location readable by Pager tools. | M |
| FR-1.3 | The target system shall expose metrics (CPU, memory, latency, error rate, queue depth). | M |
| FR-1.4 | The fault injector shall support scenarios with `inject()` and `revert()` operations. | M |
| FR-1.5 | Each scenario shall record a ground-truth `root_cause`, `affected_services`, and an `acceptable_fixes` list. | M |
| FR-1.6 | The system shall ship with at least 5 scenarios in v1 and 15 to 20 by final release. | M |
| FR-1.7 | Scenarios shall include: memory leak, bad deploy, slow query, full disk, dependency timeout, expired certificate. | S |
| FR-1.8 | The injector shall support adversarial scenarios: misleading logs, red-herring errors, and prompt injection embedded in log lines. | M |

### 3.2 Agent Harness

| ID | Requirement | Priority |
|---|---|---|
| FR-2.1 | The harness shall run an agent loop: build prompt, call model, parse tool calls, execute tools, append results, repeat. | M |
| FR-2.2 | The harness shall terminate when the model signals completion or any budget is exceeded. | M |
| FR-2.3 | The harness shall enforce per-agent budgets for maximum steps, tokens, and wall-clock time. | M |
| FR-2.4 | The harness shall validate every tool call's arguments against a Pydantic schema before execution. | M |
| FR-2.5 | The harness shall enforce per-agent tool permissions; calling a non-permitted tool shall fail safely and be logged. | M |
| FR-2.6 | The harness shall return structured, typed results (findings, confidence, evidence references). | M |
| FR-2.7 | The harness shall handle model API errors with bounded retries and backoff. | M |
| FR-2.8 | The harness shall manage context size (truncate or summarize long tool outputs). | S |
| FR-2.9 | The harness shall detect repeated identical tool calls (loop detection) and stop or redirect the agent. | S |

### 3.3 Tool Layer

| ID | Requirement | Priority |
|---|---|---|
| FR-3.1 | A tool registry shall define each tool's name, description, input schema, and **permission tier**. | M |
| FR-3.2 | Read-only tools shall include: `read_logs`, `search_logs`, `query_metrics`, `list_recent_deploys`, `get_git_diff`, `docker_ps`, `service_health`. | M |
| FR-3.3 | Action tools shall include: `restart_service`, `rollback_deploy`, `scale_service`, `update_config`, `clear_cache`. | M |
| FR-3.4 | Every tool shall have a **dry-run** mode that reports what would happen without making changes. | M |
| FR-3.5 | Tool outputs derived from logs or external text shall be wrapped and labeled as untrusted data. | M |
| FR-3.6 | Tools shall enforce an allowlist of permitted targets (services, commands). | M |

### 3.4 Permission Tiers

| Tier | Description | Approval required |
|---|---|---|
| T0: Read-only | Reading logs, metrics, status | None |
| T1: Low-risk action | Reversible, narrow blast radius (e.g., restart one stateless service) | One-click approval |
| T2: High-risk action | Wider impact or hard to reverse (e.g., rollback, config change, DB-related) | Approval plus typed confirmation |
| T3: Forbidden | Destructive actions outside the allowlist (e.g., deleting data) | Never executable |

| ID | Requirement | Priority |
|---|---|---|
| FR-4.1 | The system shall assign every tool and proposed action to exactly one tier. | M |
| FR-4.2 | The system shall block execution of any T1 or T2 action without a recorded human approval. | M |
| FR-4.3 | T2 actions shall require the operator to type a confirmation string. | M |
| FR-4.4 | T3 actions shall be rejected automatically and logged. | M |

### 3.5 Orchestrator and Incident Lifecycle

| ID | Requirement | Priority |
|---|---|---|
| FR-5.1 | The orchestrator shall implement an incident state machine: `DETECTED`, `INVESTIGATING`, `DIAGNOSED`, `AWAITING_APPROVAL`, `REMEDIATING`, `VERIFYING`, `RESOLVED`, `ESCALATED`, `CLOSED_NO_ACTION`. | M |
| FR-5.2 | The orchestrator shall spawn multiple investigators concurrently with LangGraph `Send`. | M |
| FR-5.3 | The orchestrator shall assign investigators distinct focus areas (logs, metrics, deploys, infrastructure). | M |
| FR-5.4 | The orchestrator shall decide when investigation is sufficient or request additional investigation. | M |
| FR-5.5 | The orchestrator shall deduplicate and correlate alerts into a single incident. | S |
| FR-5.6 | The orchestrator shall escalate to the human if confidence stays below a threshold or budgets are exhausted. | M |
| FR-5.7 | The orchestrator shall support multiple simultaneous incidents. | C |
| FR-5.8 | State transitions shall be validated; illegal transitions shall raise errors and be logged. | M |

### 3.6 Incident Board and Messaging

| ID | Requirement | Priority |
|---|---|---|
| FR-6.1 | The incident board shall store tasks, findings, hypotheses, and evidence, each linked to an incident and agent. | M |
| FR-6.2 | Agents shall communicate through structured messages (types: `task`, `finding`, `question`, `result`, `error`). | M |
| FR-6.3 | Investigators shall be able to read the board to avoid duplicate work. | M |
| FR-6.4 | Each finding shall reference supporting evidence (log line IDs, metric windows). | M |
| FR-6.5 | Hypotheses shall carry a confidence score and a status (`open`, `supported`, `refuted`). | M |

### 3.7 Agent Roles

| ID | Agent | Responsibilities | Priority |
|---|---|---|---|
| FR-7.1 | Triager | Monitor logs and metrics, detect anomalies, assign severity, open incidents | M |
| FR-7.2 | Investigator | Examine one focus area, form hypotheses, gather and cite evidence | M |
| FR-7.3 | Diagnostician | Merge findings, rank hypotheses, request more investigation if needed | M |
| FR-7.4 | Remediation planner | Propose actions with risk tier, blast radius, expected outcome, and rollback plan | M |
| FR-7.5 | Executor | Execute **only approved** actions and verify recovery with health and metric checks | M |
| FR-7.6 | Scribe | Produce incident timeline and postmortem (summary, root cause, impact, actions, follow-ups) | S |

### 3.8 Approval Workflow

| ID | Requirement | Priority |
|---|---|---|
| FR-8.1 | For each proposed action, the operator shall see: incident summary, severity, diagnosis with confidence, supporting evidence, action details, risk tier, blast radius, and rollback plan. | M |
| FR-8.2 | The operator shall be able to **Approve**, **Reject**, or **Investigate more**. | M |
| FR-8.3 | Approval decisions shall be stored with timestamp, operator identity, and action version. | M |
| FR-8.4 | An approval shall be bound to the exact action proposed; any change to the action shall invalidate it. | M |
| FR-8.5 | Approvals shall expire after a configurable time window. | S |
| FR-8.6 | A rejection with a reason shall be fed back to the planner to propose an alternative. | S |

### 3.9 Verification and Rollback

| ID | Requirement | Priority |
|---|---|---|
| FR-9.1 | After execution, the executor shall verify recovery using defined health and metric checks. | M |
| FR-9.2 | If verification fails, the system shall mark the incident `ESCALATED` and propose rollback of the applied action. | M |
| FR-9.3 | Every action shall have a documented rollback procedure stored with the proposal. | M |

### 3.10 Safety Controls

| ID | Requirement | Priority |
|---|---|---|
| FR-10.1 | A global **kill switch** shall immediately halt all agents and block all actions. | M |
| FR-10.2 | A **dry-run mode** shall run the full pipeline without executing actions. | M |
| FR-10.3 | Action rate limits shall cap the number of actions per time window. | M |
| FR-10.4 | Content from logs, metrics, and tool outputs shall never be treated as instructions; instructions embedded in such content shall be flagged. | M |
| FR-10.5 | Agents shall not have access to secrets beyond those required by their tools. | S |

### 3.11 Observability, Tracing, and Audit

| ID | Requirement | Priority |
|---|---|---|
| FR-11.1 | The system shall record a trace of every agent step: prompt summary, model response, tool calls, results, tokens, latency, and cost. | M |
| FR-11.2 | The system shall maintain an append-only audit log of approvals, executed actions, state transitions, and safety events. | M |
| FR-11.3 | Traces and audit entries shall be queryable by incident, agent, and time. | M |
| FR-11.4 | The system shall compute token usage and estimated cost per agent, per incident. | M |

### 3.12 User Interfaces

**CLI (early milestones)**

| ID | Requirement | Priority |
|---|---|---|
| FR-12.1 | The CLI shall print incident state changes and agent activity. | M |
| FR-12.2 | The CLI shall prompt `approve? y/n` using the same approval logic as the web UI. | M |

**Web UI (milestone 5)**

| ID | Requirement | Priority |
|---|---|---|
| FR-12.3 | The approval screen shall present all information in FR-8.1 and the three decision buttons. | M |
| FR-12.4 | The live dashboard shall show incident states, active agents, and a streaming activity feed using SSE or WebSockets. | M |
| FR-12.5 | The trace viewer shall show a per-incident timeline of agent steps, tool calls, tokens, cost, and approvals. | S |
| FR-12.6 | The web UI shall read from storage and event streams only; it shall not call agents directly. | M |
| FR-12.7 | The UI shall include a prominent kill-switch control. | M |

### 3.13 Evaluation Suite

| ID | Requirement | Priority |
|---|---|---|
| FR-13.1 | The eval runner shall execute scenarios end to end: inject, run Pager, grade, revert. | M |
| FR-13.2 | The eval runner shall auto-approve or simulate operator decisions according to a configured policy. | M |
| FR-13.3 | Metrics shall include: diagnosis accuracy, time to diagnosis, time to resolution, fix quality, safety violations, token use, and cost per incident. | M |
| FR-13.4 | The runner shall support a **single-agent baseline** using the same tools and model for comparison. | M |
| FR-13.5 | The runner shall execute each scenario multiple times (configurable) and report variance. | S |
| FR-13.6 | The report generator shall output a Markdown summary with tables and charts comparing swarm and baseline. | M |
| FR-13.7 | Adversarial scenarios shall be reported separately with outcomes on safety and resilience. | M |

---

## 4. Non-Functional Requirements

### 4.1 Safety and Security

| ID | Requirement |
|---|---|
| NFR-S1 | **Zero unapproved actions:** no T1/T2 action shall execute without a valid approval (target: 0 violations across all evals). |
| NFR-S2 | Prompt injection embedded in logs shall not cause an agent to call a non-permitted tool or bypass approval (target: 0 successful injections in the adversarial suite). |
| NFR-S3 | Action execution shall be sandboxed to the target containers. |
| NFR-S4 | API keys and secrets shall be loaded from environment variables and never written to logs or traces. |
| NFR-S5 | The audit log shall be append-only and tamper-evident (hash chaining is a stretch goal). |

### 4.2 Performance

| ID | Requirement |
|---|---|
| NFR-P1 | Time from fault injection to incident detection: under 60 seconds. |
| NFR-P2 | Time from incident open to diagnosis for standard scenarios: under 3 minutes median. |
| NFR-P3 | Parallel investigators shall run concurrently with no blocking on each other. |
| NFR-P4 | Web UI updates shall appear within 2 seconds of the underlying event. |

### 4.3 Reliability

| ID | Requirement |
|---|---|
| NFR-R1 | A failure of one agent shall not crash the orchestrator or other agents. |
| NFR-R2 | Orchestrator state shall be persisted so an incident can resume after a process restart. |
| NFR-R3 | Model API failures shall be retried with exponential backoff, then degrade to escalation. |

### 4.4 Cost Control

| ID | Requirement |
|---|---|
| NFR-C1 | Per-incident token and cost budgets shall be configurable and enforced. |
| NFR-C2 | The system shall abort and escalate when the incident budget is exceeded. |
| NFR-C3 | Target median cost per incident shall be reported in the eval; a soft target is under USD 1.00 for standard scenarios. |

### 4.5 Maintainability and Extensibility

| ID | Requirement |
|---|---|
| NFR-M1 | Adding a new tool shall require only registering a schema, a handler, and a tier. |
| NFR-M2 | Adding a new scenario shall require only a new scenario file and an entry in `scenarios.yaml`. |
| NFR-M3 | Adding a new agent role shall require only a prompt, a tool set, and a budget. |
| NFR-M4 | Code shall be typed, linted, and covered by unit tests for harness, state machine, and safety logic (target: 80% coverage on these modules). |

### 4.6 Usability

| ID | Requirement |
|---|---|
| NFR-U1 | The approval screen shall let an operator make a decision without reading raw logs (evidence is summarized with drill-down). |
| NFR-U2 | The whole system shall start with one command (`make dev`), which starts the API and the web UI against host Postgres and Redis. |
| NFR-U3 | The README shall include a quick start, architecture diagram, and demo instructions. |

### 4.7 Portability
- Runs on Linux and macOS with Docker. Windows via WSL2 is optional.

---

## 5. Data Requirements

### 5.1 Core Entities

| Entity | Key fields |
|---|---|
| Incident | id, title, severity, state, opened_at, closed_at, root_cause, resolution, thread_id |
| Task | id, incident_id, agent_role, description, status, created_at |
| Finding | id, incident_id, agent_id, summary, evidence_refs, confidence |
| Hypothesis | id, incident_id, description, confidence, status |
| Action | id, incident_id, tool, args, tier, risk, blast_radius, rollback_plan, status |
| Approval | id, action_id, operator, decision, reason, typed_confirmation, timestamp |
| TraceStep | id, incident_id, agent_id, step_no, prompt_ref, response, tool_calls, tokens_in, tokens_out, cost, latency |
| AuditEvent | id, timestamp, actor, event_type, payload, prev_hash |
| Scenario | id, name, root_cause, affected_services, acceptable_fixes, difficulty, adversarial |
| EvalRun | id, scenario_id, mode (swarm/baseline), results, metrics |

### 5.2 Storage
- Postgres for all entities, including LangGraph checkpoints.
- Redis pub/sub for the live event stream. Each event is written to Postgres first, then published. SSE clients backfill from Postgres on reconnect.
- Raw logs and large tool outputs stored as files with references from the database.
- Retention: local and indefinite for v1.
- v1 development runs Postgres and Redis on the host. Docker returns only if the target system needs it.

---

## 6. External Interface Requirements

### 6.1 Software Interfaces
- **Anthropic API:** messages endpoint with tool use.
- **Docker Engine API / CLI:** container status, logs, restart, scaling.
- **Git:** deploy history and diffs for the target API service.
- **Postgres and Redis:** health and metric queries.

### 6.2 User Interfaces
- CLI and web UI as described in section 3.12.

### 6.3 Internal Interfaces
- **Message schema:** Pydantic models for all agent messages.
- **Tool interface:** `Tool(name, schema, tier, handler, dry_run_handler)`.
- **Event stream:** Postgres event table, Redis pub/sub, and an SSE endpoint consumed by the web UI.

---

## 7. Architecture Overview

```
pager/
  target/                 # system that breaks
  faults/                 # injector and scenarios
  pager/
    graph/                # LangGraph StateGraph, Send fan-out, interrupt gate
    harness/              # budgets, tool nodes, permission checks
    orchestrator/         # incident state, board, bus
    agents/               # triager, investigator, diagnostician, planner, executor, scribe
    safety/               # approvals.py, allowlist.py, killswitch.py
    storage/              # db.py, audit.py, traces.py
    ui/                   # approval_app.py
  evals/                  # scenarios.yaml, runner.py, report.py
  tests/
```

### 7.1 Key Design Decisions
1. **LangGraph orchestration.** The incident lifecycle is a StateGraph, investigators run in parallel via Send, and human approval resumes a paused thread with Command. Checkpoints live in Postgres so a restart can resume the same incident. Safety stays in project code inside tool nodes so a prompt cannot raise its own permissions.
2. **Decoupled UI:** agents write events to Postgres and Redis; the UI reads them and never calls agents directly.
3. **Typed everything:** Pydantic models at every boundary.
4. **Safety by construction:** permission tier is a property of the tool, enforced in the harness, not in the prompt.
5. **Untrusted-input handling:** tool outputs derived from logs are wrapped and labeled, and agents have no ability to escalate their own permissions.

---

## 8. Acceptance Criteria and Success Metrics

| Metric | Target |
|---|---|
| Diagnosis accuracy (standard scenarios) | at least 80% correct root cause |
| Diagnosis accuracy (adversarial scenarios) | at least 60% correct root cause |
| Unapproved action executions | 0 |
| Successful prompt injections | 0 |
| Proposed fix would resolve incident | at least 75% of cases |
| Swarm vs. single agent | Swarm equal or better on accuracy or time, with cost reported honestly |
| Median time to diagnosis | under 3 minutes |
| Median cost per incident | under USD 1.00 (soft) |
| Scenarios implemented | at least 15 |

The project is complete when all **Must** requirements are implemented, the eval report is generated, and a demo video (about 2 minutes) shows an injected incident, the swarm's diagnosis, and an operator approval.

---

## 9. Milestones

| # | Milestone | Deliverables |
|---|---|---|
| 1 | Target system and faults | Docker Compose environment, injector, 5 scenarios with ground truth |
| 2 | Harness and tools | Agent loop, budgets, tool registry with tiers, read-only tools, single investigating agent |
| 3 | Orchestration | Orchestrator state machine, parallel investigators, incident board, structured messaging |
| 4 | Remediation and safety | Planner, approval gate (CLI), executor, verification, kill switch, dry-run, audit log |
| 5 | Interfaces and tracing | Web UI (approval, dashboard, trace viewer), postmortem generation |
| 6 | Evals and polish | Eval runner, adversarial cases, single-agent baseline, comparison report, README, demo video |

---

## 10. Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Agents loop or waste tokens | Cost, delay | Step/token/time budgets, loop detection |
| Hallucinated diagnosis with high confidence | Wrong fix proposed | Require evidence references, human approval, confidence calibration in evals |
| Prompt injection via logs | Safety breach | Untrusted-data wrapping, tier enforcement in harness, adversarial evals |
| Non-deterministic results make evals noisy | Weak conclusions | Multiple runs per scenario, report variance |
| Scope creep | Project never finishes | Strict milestone order, CLI before web UI |
| Docker/environment flakiness | Unreliable demos | Host Postgres and Redis for v1 dev; reset scripts, deterministic seeds, health checks before each eval |
| LangGraph resumes a changed action | Approval applies to the wrong change | interrupt payload includes the action version; resume rejects a mismatch |
| A framework helper bypasses the safety layer | Unapproved or forbidden action | Tiers, the allowlist, and the kill switch run inside tool nodes before any side effect |

---

## 11. Future Enhancements (Out of Scope for v1)
- Slack or PagerDuty integration for approvals.
- Support for real cloud infrastructure and Kubernetes.
- Learning from past incidents (retrieval over postmortems).
- Multi-root-cause incidents and cascading failures.
- Automatic runbook generation from resolved incidents.
- Hash-chained, tamper-evident audit log.

---

## Appendix A: Requirement Traceability (Summary)

| Goal | Related requirements |
|---|---|
| LangGraph swarm with safety in project code | C-1, FR-2.x, FR-5.x |
| Safe human-in-the-loop autonomy | FR-4.x, FR-8.x, FR-10.x, NFR-S1, NFR-S2 |
| Measurable evaluation | FR-13.x, Section 8 |
| Portfolio-quality demo | FR-12.x, NFR-U2, NFR-U3, Milestone 6 |