"""Faker demo data. Replaces whatever is in the pager database.

One incident is created for every state. Two of them wait on approval:
INC-1048 is a T2 rollback (type `rollback api`), INC-1042 is a T1 restart.
"""

from datetime import datetime, timedelta, timezone
from uuid import uuid4

from faker import Faker

from pager.dev.catalog import CAUSES, EXCERPTS, FINDINGS, HYPOTHESES, SUMMARIES, TITLES, TRACE_LINES
from pager.storage.db import SessionLocal, engine, init_db
from pager.storage.events import append_audit
from pager.storage.models import (
    Action,
    Approval,
    Base,
    Finding,
    Hypothesis,
    Incident,
    KillSwitch,
    Task,
    TraceStep,
)

# Stable across machines so the board does not reshuffle on every seed.
Faker.seed(1048)


def _ago(now: datetime, minutes: int) -> datetime:
    return now - timedelta(minutes=minutes)


def _evidence(fake: Faker, source: str) -> dict:
    return {
        "id": fake.bothify("??-####").lower(),
        "source": source,
        "excerpt": fake.random_element(EXCERPTS[source]),
    }


def _trace(fake: Faker, incident_id: str, number: int, when: datetime) -> TraceStep:
    role, agent, response, tool = TRACE_LINES[(number - 1) % len(TRACE_LINES)]
    tokens_in = fake.random_int(400, 1600)
    tokens_out = fake.random_int(80, 280)
    return TraceStep(
        incident_id=incident_id,
        agent_id=agent,
        agent_role=role,
        step_no=number,
        prompt_ref=f"prompt:{role}:{number}",
        response=response,
        tool_calls=[{"tool": tool, "tier": "T0"}],
        tokens_in=tokens_in,
        tokens_out=tokens_out,
        cost=round((tokens_in * 3 + tokens_out * 15) / 1_000_000, 4),
        latency_ms=fake.random_int(120, 900),
        created_at=when,
    )


def main() -> None:
    fake = Faker()
    Base.metadata.drop_all(bind=engine)
    init_db()
    db = SessionLocal()
    now = datetime.now(timezone.utc)
    pinned = {"INC-1048": TITLES[0], "INC-1042": TITLES[1]}
    pool = [item for item in TITLES if item not in pinned.values()]
    fake.random.shuffle(pool)

    # Approval cases keep the ids and titles the UI copy uses.
    plan = [
        ("DETECTED", "INC-0970", 4),
        ("INVESTIGATING", "INC-1033", 12),
        ("DIAGNOSED", "INC-1008", 40),
        ("AWAITING_APPROVAL", "INC-1048", 18),
        ("AWAITING_APPROVAL", "INC-1042", 26),
        ("REMEDIATING", "INC-0988", 34),
        ("VERIFYING", "INC-0994", 55),
        ("RESOLVED", "INC-1021", 180),
        ("ESCALATED", "INC-1014", 70),
        ("CLOSED_NO_ACTION", "INC-0962", 300),
    ]

    def take_title(ident: str) -> tuple[str, str, list[str]]:
        if ident in pinned:
            return pinned[ident]
        return pool.pop()

    try:
        notes: list[tuple[datetime, str, str, str, str]] = []
        for state, ident, minutes in plan:
            title, severity, services = take_title(ident)
            opened = _ago(now, minutes)
            closed = _ago(now, max(minutes - 25, 1)) if state in {"RESOLVED", "CLOSED_NO_ACTION"} else None
            service = services[0]
            progressed = state != "DETECTED"
            diagnosed = state not in {"DETECTED", "INVESTIGATING"}
            acted = state in {"AWAITING_APPROVAL", "REMEDIATING", "VERIFYING", "RESOLVED"}
            db.add(
                Incident(
                    id=ident,
                    title=title,
                    summary=SUMMARIES[title],
                    severity=severity,
                    state=state,
                    opened_at=opened,
                    closed_at=closed,
                    root_cause=CAUSES[title] if diagnosed else None,
                    resolution=fake.sentence(nb_words=8) if state in {"RESOLVED", "CLOSED_NO_ACTION", "VERIFYING"} else None,
                    thread_id=str(uuid4()),
                    affected_services=services,
                )
            )
            notes.append((opened, ident, "triager", "incident_opened", f"Opened {severity}. {title}."))

            if state == "DETECTED":
                db.add(
                    Task(
                        incident_id=ident,
                        agent_id="triager",
                        agent_role="triager",
                        description="Score the new page.",
                        status="running",
                        step="Opening the incident",
                        tokens=fake.random_int(80, 400),
                        created_at=opened,
                    )
                )
            if state == "INVESTIGATING":
                for agent, source in (("inv-logs", "logs"), ("inv-metrics", "metrics"), ("inv-deploys", "git"), ("inv-infra", "infra")):
                    db.add(
                        Task(
                            incident_id=ident,
                            agent_id=agent,
                            agent_role="investigator",
                            description=f"Read {source}.",
                            status="running",
                            step=f"Reading {source}",
                            tokens=fake.random_int(200, 1800),
                            created_at=_ago(now, minutes - 2),
                        )
                    )
            if state == "REMEDIATING":
                db.add(
                    Task(
                        incident_id=ident,
                        agent_id="executor",
                        agent_role="executor",
                        description="Run the approved action.",
                        status="running",
                        step="Waiting on health",
                        tokens=fake.random_int(100, 500),
                        created_at=_ago(now, 6),
                    )
                )

            finding_count = 0 if not progressed else 1 if state == "INVESTIGATING" else 2
            for index in range(finding_count):
                agent, source, line = FINDINGS[index % len(FINDINGS)]
                when = _ago(now, max(minutes - 4 - index, 1))
                db.add(
                    Finding(
                        incident_id=ident,
                        agent_id=agent,
                        summary=line,
                        evidence_refs=[_evidence(fake, source)],
                        confidence=round(fake.pyfloat(min_value=0.55, max_value=0.97), 2),
                        created_at=when,
                    )
                )
                notes.append((when, ident, agent, "finding", line))

            if progressed:
                lead = HYPOTHESES[0 if acted or diagnosed else 3]
                status = "supported" if diagnosed and state != "ESCALATED" else "open"
                if state == "CLOSED_NO_ACTION":
                    status = "refuted"
                when = _ago(now, max(minutes - 6, 1))
                db.add(
                    Hypothesis(
                        incident_id=ident,
                        description=lead,
                        confidence=0.42 if state == "ESCALATED" else round(fake.pyfloat(min_value=0.6, max_value=0.95), 2),
                        status=status,
                        created_at=when,
                    )
                )
                if finding_count > 1:
                    db.add(
                        Hypothesis(
                            incident_id=ident,
                            description=HYPOTHESES[1],
                            confidence=round(fake.pyfloat(min_value=0.1, max_value=0.4), 2),
                            status="refuted" if diagnosed else "open",
                            created_at=when,
                        )
                    )
                notes.append((when, ident, "diagnostician", "hypothesis", lead))

            if acted:
                tier = "T2" if ident == "INC-1048" else "T1"
                tool = "rollback_deploy" if tier == "T2" else "restart_service" if ident == "INC-1042" else "scale_service"
                status = "proposed" if state == "AWAITING_APPROVAL" else "approved"
                action_id = f"ACT-{ident.removeprefix('INC-')}"
                when = _ago(now, max(minutes - 7, 1))
                db.add(
                    Action(
                        id=action_id,
                        incident_id=ident,
                        tool=tool,
                        args={"service": service} if tool != "scale_service" else {"service": service, "replicas": 3},
                        tier=tier,
                        risk=fake.sentence(nb_words=8),
                        blast_radius=f"The {service} service.",
                        rollback_plan=fake.sentence(nb_words=7),
                        expected_outcome=fake.sentence(nb_words=7),
                        confirmation_phrase="rollback api" if tier == "T2" else None,
                        status=status,
                        version=1,
                        created_at=when,
                    )
                )
                notes.append((when, ident, "planner", "action_proposed", f"Proposed {tool}. Tier {tier}."))
                if status == "approved":
                    approved_at = _ago(now, max(minutes - 12, 1))
                    db.add(
                        Approval(
                            action_id=action_id,
                            operator="on-call",
                            decision="approve",
                            reason=None,
                            typed_confirmation="rollback api" if tier == "T2" else None,
                            action_version=1,
                            timestamp=approved_at,
                        )
                    )
                    notes.append((approved_at, ident, "on-call", "approval", f"Approved {tool}."))

            steps = 1 if state == "DETECTED" else 3 if state == "INVESTIGATING" else 4
            for number in range(1, steps + 1):
                db.add(_trace(fake, ident, number, _ago(now, max(minutes - number, 1))))

        for when, incident_id, actor, kind, summary in sorted(notes, key=lambda item: item[0]):
            append_audit(db, actor=actor, event_type=kind, summary=summary, incident_id=incident_id, when=when)

        db.add(KillSwitch(id=1, active=False, actor=None, updated_at=now))
        db.commit()
    finally:
        db.close()
    print("seeded 10 incidents")


if __name__ == "__main__":
    main()
