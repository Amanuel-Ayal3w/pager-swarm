"""Writes the incident board the UI already reads."""

import random
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select

from pager.safety.gates import approval_holds
from pager.storage.db import SessionLocal
from pager.storage.events import append_audit, publish
from pager.storage.models import Action, Approval, Finding, Hypothesis, Incident, KillSwitch, Scenario, Task, TraceStep


def estimate_cost(tokens_in: int, tokens_out: int) -> float:
    # gpt-6.1-sol list price: $2 / million input, $10 / million output.
    return round((tokens_in * 2 + tokens_out * 10) / 1_000_000, 6)


def _publish(event) -> None:
    try:
        publish(event)
    except Exception:
        return


class MemoryBoard:
    """In-memory board for tests. It follows the same approval rule as Postgres."""

    def __init__(self) -> None:
        self.incident_id = ""
        self.kill = False
        self.recent = 0
        self.states: list[str] = []
        self.findings: list[dict] = []
        self.hypotheses: list[dict] = []
        self.actions: list[dict] = []
        self.traces: list[dict] = []
        self.notes: list[str] = []
        self.tasks: list[dict] = []
        self.scenarios: list[str] = []
        self._seq = 2001

    def kill_active(self) -> bool:
        return self.kill

    def recent_action_count(self, incident_id: str | None = None, exclude_action_id: str | None = None) -> int:
        del incident_id, exclude_action_id
        return self.recent

    def open_incident(self, *, thread_id: str, title: str, summary: str, severity: str, services: list[str]) -> str:
        self.incident_id = f"INC-{self._seq}"
        self._seq += 1
        self.states.append("DETECTED")
        self.notes.append(f"Opened {self.incident_id}. {title}")
        del thread_id, summary, severity, services
        return self.incident_id

    def set_state(self, incident_id: str, state: str, **_: object) -> None:
        self.incident_id = incident_id
        self.states.append(state)

    def start_task(self, incident_id: str, agent_id: str, role: str, description: str) -> None:
        self.tasks.append({"incident_id": incident_id, "agent_id": agent_id, "role": role, "description": description, "status": "running"})

    def finish_task(self, incident_id: str, agent_id: str, step: str, tokens: int) -> None:
        for task in reversed(self.tasks):
            if task["incident_id"] == incident_id and task["agent_id"] == agent_id and task["status"] == "running":
                task["status"] = "done"
                task["step"] = step
                task["tokens"] = tokens
                return

    def add_finding(self, incident_id: str, agent_id: str, summary: str, evidence_refs: list, confidence: float) -> None:
        self.findings.append(
            {"incident_id": incident_id, "agent_id": agent_id, "summary": summary, "evidence_refs": evidence_refs, "confidence": confidence}
        )

    def add_hypothesis(self, incident_id: str, description: str, confidence: float, status: str) -> None:
        self.hypotheses.append({"incident_id": incident_id, "description": description, "confidence": confidence, "status": status})

    def propose_action(self, incident_id: str, **fields) -> dict:
        number = len(self.actions) + 1
        suffix = incident_id.removeprefix("INC-")
        action_id = f"ACT-{suffix}" if number == 1 else f"ACT-{suffix}-{number}"
        action = {
            "id": action_id,
            "incident_id": incident_id,
            "status": "proposed",
            "version": 1,
            "decision": "",
            "typed_confirmation": None,
            "approved_version": None,
            **fields,
        }
        self.actions.append(action)
        return action

    def get_action(self, action_id: str) -> dict | None:
        for action in self.actions:
            if action["id"] == action_id:
                return action
        return None

    def action_is_approved(self, action_id: str, version: int) -> bool:
        action = self.get_action(action_id)
        if action is None:
            return False
        return approval_holds(
            status=action["status"],
            version=action["version"],
            approved_version=action.get("approved_version") if action.get("approved_version") is not None else -1,
            tier=action["tier"],
            kill=self.kill,
            decision=action.get("decision") or "",
            typed=action.get("typed_confirmation"),
            phrase=action.get("confirmation_phrase"),
        )

    def add_trace(self, incident_id, agent_id, role, prompt_ref, response, tool_calls, tokens_in, tokens_out) -> None:
        self.traces.append(
            {
                "incident_id": incident_id,
                "agent_id": agent_id,
                "role": role,
                "prompt_ref": prompt_ref,
                "response": response,
                "tool_calls": tool_calls,
                "tokens_in": tokens_in,
                "tokens_out": tokens_out,
            }
        )

    def note(self, incident_id: str, actor: str, event_type: str, summary: str, payload: dict | None = None) -> None:
        del incident_id, actor, event_type, payload
        self.notes.append(summary)

    def upsert_scenario(self, scenario) -> None:
        self.scenarios.append(scenario.id)


class PostgresBoard:
    def __init__(self) -> None:
        self.incident_id = ""

    def kill_active(self) -> bool:
        with SessionLocal() as db:
            row = db.get(KillSwitch, 1)
            return bool(row and row.active)

    def recent_action_count(self, incident_id: str | None = None, exclude_action_id: str | None = None) -> int:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=1)
        with SessionLocal() as db:
            query = (
                select(func.count())
                .select_from(Approval)
                .join(Action)
                .where(Approval.decision == "approve", Approval.timestamp >= cutoff)
            )
            if incident_id:
                query = query.where(Action.incident_id == incident_id)
            if exclude_action_id:
                query = query.where(Approval.action_id != exclude_action_id)
            return int(db.scalar(query) or 0)

    def open_incident(self, *, thread_id: str, title: str, summary: str, severity: str, services: list[str]) -> str:
        with SessionLocal() as db:
            incident_id = _fresh_id(db)
            db.add(
                Incident(
                    id=incident_id,
                    title=title,
                    summary=summary,
                    severity=severity,
                    state="DETECTED",
                    thread_id=thread_id,
                    affected_services=services,
                )
            )
            event = append_audit(
                db,
                actor="triager",
                event_type="incident_opened",
                summary=f"Opened {incident_id}. {title}",
                incident_id=incident_id,
                payload={"severity": severity, "services": services},
            )
            db.commit()
            _publish(event)
        self.incident_id = incident_id
        return incident_id

    def set_state(self, incident_id: str, state: str, *, summary: str | None = None, root_cause: str | None = None, resolution: str | None = None) -> None:
        with SessionLocal() as db:
            incident = db.get(Incident, incident_id)
            if incident is None:
                return
            changed = incident.state != state
            incident.state = state
            if summary is not None:
                incident.summary = summary
            if root_cause is not None:
                incident.root_cause = root_cause
            if resolution is not None:
                incident.resolution = resolution
            if state in {"RESOLVED", "ESCALATED", "CLOSED_NO_ACTION"}:
                incident.closed_at = incident.closed_at or datetime.now(timezone.utc)
            else:
                incident.closed_at = None
            event = None
            if changed:
                event = append_audit(
                    db,
                    actor="orchestrator",
                    event_type="state",
                    summary=f"{incident_id} is {state}.",
                    incident_id=incident_id,
                    payload={"state": state},
                )
            db.commit()
            if event is not None:
                _publish(event)
        self.incident_id = incident_id

    def start_task(self, incident_id: str, agent_id: str, role: str, description: str) -> None:
        with SessionLocal() as db:
            db.add(Task(incident_id=incident_id, agent_id=agent_id, agent_role=role, description=description, status="running", step=description))
            db.commit()

    def finish_task(self, incident_id: str, agent_id: str, step: str, tokens: int) -> None:
        with SessionLocal() as db:
            task = db.scalar(
                select(Task)
                .where(Task.incident_id == incident_id, Task.agent_id == agent_id, Task.status == "running")
                .order_by(Task.created_at.desc())
            )
            if task is None:
                return
            task.status = "done"
            task.step = step
            task.tokens = tokens
            db.commit()

    def add_finding(self, incident_id: str, agent_id: str, summary: str, evidence_refs: list, confidence: float) -> None:
        with SessionLocal() as db:
            db.add(Finding(incident_id=incident_id, agent_id=agent_id, summary=summary, evidence_refs=evidence_refs, confidence=confidence))
            event = append_audit(
                db,
                actor=agent_id,
                event_type="finding",
                summary=summary,
                incident_id=incident_id,
                payload={"confidence": confidence, "evidence_refs": evidence_refs},
            )
            db.commit()
            _publish(event)

    def add_hypothesis(self, incident_id: str, description: str, confidence: float, status: str) -> None:
        with SessionLocal() as db:
            db.add(Hypothesis(incident_id=incident_id, description=description, confidence=confidence, status=status))
            event = append_audit(
                db,
                actor="diagnostician",
                event_type="hypothesis",
                summary=description,
                incident_id=incident_id,
                payload={"confidence": confidence, "status": status},
            )
            db.commit()
            _publish(event)

    def propose_action(
        self,
        incident_id: str,
        *,
        tool: str,
        args: dict,
        tier: str,
        risk: str,
        blast_radius: str,
        rollback_plan: str,
        expected_outcome: str,
        confirmation_phrase: str | None,
    ) -> dict:
        with SessionLocal() as db:
            action_id = _action_id(db, incident_id)
            action = Action(
                id=action_id,
                incident_id=incident_id,
                tool=tool,
                args=args,
                tier=tier,
                risk=risk,
                blast_radius=blast_radius,
                rollback_plan=rollback_plan,
                expected_outcome=expected_outcome,
                confirmation_phrase=confirmation_phrase,
                status="proposed",
                version=1,
            )
            db.add(action)
            event = append_audit(
                db,
                actor="planner",
                event_type="action_proposed",
                summary=f"Proposed {tool}.",
                incident_id=incident_id,
                payload={"action_id": action_id, "tier": tier, "tool": tool},
            )
            db.commit()
            _publish(event)
            return _action_dict(action)

    def get_action(self, action_id: str) -> dict | None:
        with SessionLocal() as db:
            action = db.get(Action, action_id)
            if action is None:
                return None
            return _action_dict(action)

    def action_is_approved(self, action_id: str, version: int) -> bool:
        with SessionLocal() as db:
            action = db.get(Action, action_id)
            if action is None:
                return False
            approval = db.scalar(select(Approval).where(Approval.action_id == action_id).order_by(Approval.timestamp.desc()))
            kill = db.get(KillSwitch, 1)
            return approval_holds(
                status=action.status,
                version=action.version,
                approved_version=approval.action_version if approval else -1,
                tier=action.tier,
                kill=bool(kill and kill.active),
                decision=approval.decision if approval else "",
                typed=approval.typed_confirmation if approval else None,
                phrase=action.confirmation_phrase,
            )

    def add_trace(self, incident_id, agent_id, role, prompt_ref, response, tool_calls, tokens_in, tokens_out) -> None:
        with SessionLocal() as db:
            step_no = int(
                db.scalar(select(func.count()).select_from(TraceStep).where(TraceStep.incident_id == incident_id)) or 0
            )
            db.add(
                TraceStep(
                    incident_id=incident_id,
                    agent_id=agent_id,
                    agent_role=role,
                    step_no=step_no + 1,
                    prompt_ref=prompt_ref,
                    response=response or "",
                    tool_calls=tool_calls,
                    tokens_in=tokens_in,
                    tokens_out=tokens_out,
                    cost=estimate_cost(tokens_in, tokens_out),
                    latency_ms=0,
                )
            )
            db.commit()

    def note(self, incident_id: str, actor: str, event_type: str, summary: str, payload: dict | None = None) -> None:
        with SessionLocal() as db:
            event = append_audit(
                db,
                actor=actor,
                event_type=event_type,
                summary=summary,
                incident_id=incident_id,
                payload=payload,
            )
            db.commit()
            _publish(event)

    def upsert_scenario(self, scenario) -> None:
        with SessionLocal() as db:
            row = db.get(Scenario, scenario.id)
            if row is None:
                db.add(
                    Scenario(
                        id=scenario.id,
                        name=scenario.title,
                        root_cause=scenario.root_cause,
                        affected_services=list(scenario.services),
                        acceptable_fixes=list(scenario.acceptable_fixes),
                        difficulty="adversarial" if scenario.adversarial else "standard",
                        adversarial=scenario.adversarial,
                    )
                )
            else:
                row.name = scenario.title
                row.root_cause = scenario.root_cause
                row.affected_services = list(scenario.services)
                row.acceptable_fixes = list(scenario.acceptable_fixes)
                row.adversarial = scenario.adversarial
            db.commit()


def _fresh_id(db) -> str:
    for _ in range(20):
        candidate = f"INC-{random.randint(2000, 8999)}"
        if db.get(Incident, candidate) is None:
            return candidate
    return f"INC-{random.randint(100000, 999999)}"


def _action_id(db, incident_id: str) -> str:
    suffix = incident_id.removeprefix("INC-")
    base = f"ACT-{suffix}"
    if db.get(Action, base) is None:
        return base
    count = int(db.scalar(select(func.count()).select_from(Action).where(Action.incident_id == incident_id)) or 0)
    return f"{base}-{count + 1}"


def _action_dict(action: Action) -> dict:
    return {
        "id": action.id,
        "incident_id": action.incident_id,
        "tool": action.tool,
        "args": action.args,
        "tier": action.tier,
        "version": action.version,
        "status": action.status,
        "confirmation_phrase": action.confirmation_phrase,
        "risk": action.risk,
        "blast_radius": action.blast_radius,
        "rollback_plan": action.rollback_plan,
        "expected_outcome": action.expected_outcome,
    }
