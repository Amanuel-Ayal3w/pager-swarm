"""Play one new incident onto the live feed.

Each beat is stored and published, then the process waits. The board
picks the lines up over SSE. Ctrl-C stops the replay.
"""

import argparse
import time
from datetime import datetime, timezone
from uuid import uuid4

from faker import Faker

from pager.dev.catalog import EXCERPTS, SERVICES
from pager.storage.db import SessionLocal, init_db
from pager.storage.events import append_audit, publish
from pager.storage.models import Action, Finding, Hypothesis, Incident, KillSwitch, Task, TraceStep

Faker.seed(int(datetime.now(timezone.utc).timestamp()))


def _beat(db, *, actor: str, event_type: str, summary: str, incident_id: str) -> None:
    event = append_audit(db, actor=actor, event_type=event_type, summary=summary, incident_id=incident_id)
    db.commit()
    publish(event)
    print(f"{actor}: {summary}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Replay one incident onto the live feed.")
    parser.add_argument("--interval", type=float, default=2.0, help="Seconds between beats.")
    args = parser.parse_args()
    fake = Faker()
    init_db()
    db = SessionLocal()
    service = fake.random_element(SERVICES)
    incident_id = f"INC-{fake.random_int(2000, 8999)}"
    title = f"{service} error rate jumped"
    try:
        incident = Incident(
            id=incident_id,
            title=title,
            summary=fake.sentence(nb_words=10),
            severity="sev2",
            state="DETECTED",
            opened_at=datetime.now(timezone.utc),
            thread_id=str(uuid4()),
            affected_services=[service],
        )
        db.add(incident)
        db.add(
            Task(
                incident_id=incident_id,
                agent_id="triager",
                agent_role="triager",
                description="Score the new page.",
                status="running",
                step="Opening the incident",
                tokens=fake.random_int(80, 300),
            )
        )
        db.commit()
        _beat(db, actor="triager", event_type="incident_opened", summary=f"Opened sev 2. {title}.", incident_id=incident_id)
        time.sleep(args.interval)

        incident.state = "INVESTIGATING"
        for agent, source in (("inv-logs", "logs"), ("inv-metrics", "metrics")):
            db.add(
                Task(
                    incident_id=incident_id,
                    agent_id=agent,
                    agent_role="investigator",
                    description=f"Read {source}.",
                    status="running",
                    step=f"Reading {source}",
                    tokens=fake.random_int(200, 900),
                )
            )
        db.commit()
        _beat(db, actor="triager", event_type="state", summary=f"{incident_id} is under investigation.", incident_id=incident_id)
        time.sleep(args.interval)

        line = f"{service} logs match the failing window."
        db.add(
            Finding(
                incident_id=incident_id,
                agent_id="inv-logs",
                summary=line,
                evidence_refs=[{"id": fake.bothify("??-####").lower(), "source": "logs", "excerpt": fake.random_element(EXCERPTS["logs"])}],
                confidence=0.74,
            )
        )
        db.add(
            TraceStep(
                incident_id=incident_id,
                agent_id="inv-logs",
                agent_role="investigator",
                step_no=1,
                prompt_ref="prompt:investigator:1",
                response=line,
                tool_calls=[{"tool": "search_logs", "tier": "T0"}],
                tokens_in=fake.random_int(400, 1200),
                tokens_out=fake.random_int(80, 200),
                cost=0.004,
                latency_ms=fake.random_int(150, 700),
            )
        )
        _beat(db, actor="inv-logs", event_type="finding", summary=line, incident_id=incident_id)
        time.sleep(args.interval)

        cause = f"A change on {service} is the leading cause."
        db.add(Hypothesis(incident_id=incident_id, description=cause, confidence=0.81, status="supported"))
        incident.state = "DIAGNOSED"
        incident.root_cause = cause
        _beat(db, actor="diagnostician", event_type="hypothesis", summary=cause, incident_id=incident_id)
        time.sleep(args.interval)

        switch = db.get(KillSwitch, 1)
        if switch is not None and switch.active:
            _beat(db, actor="planner", event_type="action_proposed", summary="Kill switch is on. No action was proposed.", incident_id=incident_id)
            return

        db.add(
            Action(
                id=f"ACT-{incident_id.removeprefix('INC-')}",
                incident_id=incident_id,
                tool="restart_service",
                args={"service": service},
                tier="T1",
                risk="In-flight work retries once.",
                blast_radius=f"The {service} service.",
                rollback_plan="The process comes back on its own.",
                expected_outcome="The error rate falls within a minute.",
                status="proposed",
                version=1,
            )
        )
        incident.state = "AWAITING_APPROVAL"
        _beat(
            db,
            actor="planner",
            event_type="action_proposed",
            summary=f"Proposed a restart of {service}. Tier T1.",
            incident_id=incident_id,
        )
        print(f"paused on {incident_id}. Approve it on the board.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
