"""Demo incidents for the operator UI. Replaces whatever is in the pager database."""

from datetime import datetime, timedelta, timezone
from uuid import uuid4

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


def _ago(now: datetime, minutes: int) -> datetime:
    return now - timedelta(minutes=minutes)


def main() -> None:
    Base.metadata.drop_all(bind=engine)
    init_db()
    db = SessionLocal()
    now = datetime.now(timezone.utc)
    try:
        specs = [
            ("INC-1048", "Error rate jumped after deploy", "sev1", "AWAITING_APPROVAL", 18, ["api"], "API 5xx went from 0.2% to 18% two minutes after deploy 4f2c1a. Pooling is off in that diff.", None, None),
            ("INC-1042", "Worker memory keeps climbing", "sev2", "AWAITING_APPROVAL", 26, ["worker"], "The worker grew from 180 MB to 1.4 GB over 40 minutes. A restart clears it.", None, None),
            ("INC-1033", "Checkout queries are slow", "sev2", "INVESTIGATING", 12, ["api", "postgres"], "Checkout p95 crossed 800 ms. Investigators are still reading logs and metrics.", None, None),
            ("INC-1021", "Disk filled on the database host", "sev1", "RESOLVED", 180, ["postgres"], "The database volume hit 98%. Rotated logs were the bulk of it.", "Log volume filled /var.", "Truncated rotated logs and capped the shipper."),
            ("INC-1014", "Payments dependency timing out", "sev1", "ESCALATED", 70, ["api", "payments"], "Confidence stayed under the bar after the budget ran out.", None, None),
            ("INC-1008", "Certificate expires tonight", "sev3", "DIAGNOSED", 40, ["api"], "The public certificate expires at 02:00. No action has been proposed yet.", "The leaf certificate on api expires tonight.", None),
            ("INC-0994", "Cache hit rate collapsed", "sev3", "VERIFYING", 55, ["redis"], "Cache was flushed. Health checks are still watching the hit rate.", "A deploy flushed the hot key set.", "Hit rate is climbing back."),
            ("INC-0988", "Queue depth stuck above 10k", "sev2", "REMEDIATING", 34, ["worker"], "A scale-up was approved and is in progress.", "One worker replica could not drain the queue.", "Scaling the worker to 3."),
            ("INC-0970", "Latency above the page budget", "sev4", "DETECTED", 4, ["api"], "The triager opened this from a latency page. No findings yet.", None, None),
            ("INC-0962", "Spike was a health-check loop", "sev4", "CLOSED_NO_ACTION", 300, ["api"], "A probe loop looked like customer errors. It was not.", "Synthetic checks retrying a closed endpoint.", "No customer impact. Closed with no action."),
        ]
        for item in specs:
            ident, title, severity, state, minutes, services, summary, cause, resolution = item
            closed = _ago(now, minutes - 20) if state in {"RESOLVED", "CLOSED_NO_ACTION"} else None
            db.add(
                Incident(
                    id=ident,
                    title=title,
                    summary=summary,
                    severity=severity,
                    state=state,
                    opened_at=_ago(now, minutes),
                    closed_at=closed,
                    root_cause=cause,
                    resolution=resolution,
                    thread_id=str(uuid4()),
                    affected_services=services,
                )
            )
        db.flush()

        db.add_all(
            [
                Task(incident_id="INC-1033", agent_id="inv-logs", agent_role="investigator", description="Read checkout logs.", status="running", step="Searching error spikes", tokens=1840, created_at=_ago(now, 10)),
                Task(incident_id="INC-1033", agent_id="inv-metrics", agent_role="investigator", description="Read latency and saturation.", status="running", step="Comparing deploy windows", tokens=960, created_at=_ago(now, 10)),
                Task(incident_id="INC-1033", agent_id="inv-deploys", agent_role="investigator", description="Read the latest diff.", status="running", step="Opening git diff", tokens=420, created_at=_ago(now, 9)),
                Task(incident_id="INC-1033", agent_id="inv-infra", agent_role="investigator", description="Check database health.", status="running", step="Reading service health", tokens=610, created_at=_ago(now, 9)),
                Task(incident_id="INC-0970", agent_id="triager", agent_role="triager", description="Score the latency page.", status="running", step="Opening the incident", tokens=220, created_at=_ago(now, 3)),
                Task(incident_id="INC-0988", agent_id="executor", agent_role="executor", description="Scale the worker.", status="running", step="Waiting on health", tokens=300, created_at=_ago(now, 6)),
            ]
        )

        db.add_all(
            [
                Finding(incident_id="INC-1048", agent_id="inv-deploys", summary="Deploy 4f2c1a turned connection pooling off.", evidence_refs=[{"id": "diff-4f2c1a", "source": "git", "excerpt": "pool: false  # was true"}], confidence=0.86, created_at=_ago(now, 14)),
                Finding(incident_id="INC-1048", agent_id="inv-metrics", summary="5xx rose from 0.2% to 18% within two minutes of that deploy.", evidence_refs=[{"id": "m-5xx", "source": "metrics", "excerpt": "api_error_rate 0.18 at 14:12"}], confidence=0.91, created_at=_ago(now, 13)),
                Finding(incident_id="INC-1042", agent_id="inv-metrics", summary="Worker RSS climbed for 40 minutes, then dropped after the last restart.", evidence_refs=[{"id": "m-rss", "source": "metrics", "excerpt": "worker rss 1.4GB"}], confidence=0.84, created_at=_ago(now, 20)),
                Finding(incident_id="INC-1042", agent_id="inv-logs", summary="The resize loop logs a new buffer every request and never frees it.", evidence_refs=[{"id": "log-1842", "source": "worker", "excerpt": "alloc resize buf 12MB"}], confidence=0.78, created_at=_ago(now, 18)),
                Finding(incident_id="INC-1033", agent_id="inv-logs", summary="Checkout queries wait on a lock in orders.", evidence_refs=[{"id": "log-220", "source": "api", "excerpt": "slow query orders 840ms"}], confidence=0.62, created_at=_ago(now, 8)),
                Finding(incident_id="INC-1008", agent_id="inv-infra", summary="The leaf certificate on api expires at 02:00.", evidence_refs=[{"id": "cert-api", "source": "infra", "excerpt": "notAfter 02:00Z"}], confidence=0.97, created_at=_ago(now, 30)),
            ]
        )
        db.add_all(
            [
                Hypothesis(incident_id="INC-1048", description="Deploy 4f2c1a disabled pooling and exhausted connections.", confidence=0.9, status="supported", created_at=_ago(now, 12)),
                Hypothesis(incident_id="INC-1048", description="The payments provider is timing out.", confidence=0.15, status="refuted", created_at=_ago(now, 12)),
                Hypothesis(incident_id="INC-1042", description="The image resize loop leaks one buffer per job.", confidence=0.81, status="supported", created_at=_ago(now, 16)),
                Hypothesis(incident_id="INC-1042", description="The Redis client is left open.", confidence=0.34, status="open", created_at=_ago(now, 16)),
                Hypothesis(incident_id="INC-1033", description="A new index is missing on orders.user_id.", confidence=0.58, status="open", created_at=_ago(now, 7)),
                Hypothesis(incident_id="INC-1008", description="The api certificate expires tonight.", confidence=0.97, status="supported", created_at=_ago(now, 28)),
            ]
        )

        restart = Action(
            id="ACT-1042",
            incident_id="INC-1042",
            tool="restart_service",
            args={"service": "worker"},
            tier="T1",
            risk="In-flight jobs retry. One stateless replica restarts.",
            blast_radius="The worker only. API traffic stays up.",
            rollback_plan="No rollback. The process comes back on its own.",
            expected_outcome="RSS returns under 200 MB within a minute.",
            status="proposed",
            version=1,
            created_at=_ago(now, 15),
        )
        rollback = Action(
            id="ACT-1048",
            incident_id="INC-1048",
            tool="rollback_deploy",
            args={"service": "api", "to": "b91e0c"},
            tier="T2",
            risk="Every API user is restarted onto the previous build for about two minutes.",
            blast_radius="All API users.",
            rollback_plan="Redeploy 4f2c1a if the previous build is worse.",
            expected_outcome="Error rate returns under 1%.",
            confirmation_phrase="rollback api",
            status="proposed",
            version=1,
            created_at=_ago(now, 11),
        )
        scale = Action(
            id="ACT-0988",
            incident_id="INC-0988",
            tool="scale_service",
            args={"service": "worker", "replicas": 3},
            tier="T1",
            risk="More workers share the same queue.",
            blast_radius="The worker pool.",
            rollback_plan="Scale back to 1 replica.",
            expected_outcome="Queue depth falls under 1k.",
            status="approved",
            version=1,
            created_at=_ago(now, 20),
        )
        db.add_all([restart, rollback, scale])
        db.add(
            Approval(
                action_id="ACT-0988",
                operator="on-call",
                decision="approve",
                reason=None,
                typed_confirmation=None,
                action_version=1,
                timestamp=_ago(now, 8),
            )
        )

        def step(incident_id: str, n: int, role: str, agent: str, response: str, tool: str, minutes: int, tokens_in: int, tokens_out: int) -> TraceStep:
            return TraceStep(
                incident_id=incident_id,
                agent_id=agent,
                agent_role=role,
                step_no=n,
                prompt_ref=f"prompt:{role}:{n}",
                response=response,
                tool_calls=[{"tool": tool, "tier": "T0"}],
                tokens_in=tokens_in,
                tokens_out=tokens_out,
                cost=round((tokens_in * 3 + tokens_out * 15) / 1_000_000, 4),
                latency_ms=180 + n * 40,
                created_at=_ago(now, minutes),
            )

        db.add_all(
            [
                step("INC-1048", 1, "triager", "triager", "Opened a sev 1 after the error page.", "query_metrics", 17, 800, 120),
                step("INC-1048", 2, "investigator", "inv-deploys", "The diff turns pooling off.", "get_git_diff", 14, 1400, 260),
                step("INC-1048", 3, "diagnostician", "diagnostician", "Pooling is the supported cause.", "search_logs", 12, 900, 180),
                step("INC-1048", 4, "planner", "planner", "Propose a rollback. This is T2.", "list_recent_deploys", 11, 700, 160),
                step("INC-1042", 1, "triager", "triager", "Memory slope is not a blip.", "query_metrics", 24, 600, 100),
                step("INC-1042", 2, "investigator", "inv-logs", "The resize loop keeps the buffer.", "search_logs", 18, 1100, 200),
                step("INC-1042", 3, "planner", "planner", "Restart the worker. This is T1.", "service_health", 15, 500, 90),
                step("INC-1033", 1, "investigator", "inv-logs", "Checkout waits on orders.", "search_logs", 8, 700, 140),
                step("INC-1021", 1, "executor", "executor", "Disk is back under 70%.", "service_health", 160, 400, 80),
            ]
        )

        notes = [
            (20, "INC-1048", "triager", "incident_opened", "Opened sev 1. Error rate jumped after deploy."),
            (16, "INC-1042", "triager", "incident_opened", "Opened sev 2. Worker memory keeps climbing."),
            (14, "INC-1048", "inv-deploys", "finding", "Deploy 4f2c1a turned pooling off."),
            (13, "INC-1048", "inv-metrics", "finding", "5xx hit 18% within two minutes."),
            (12, "INC-1048", "diagnostician", "hypothesis", "Pooling is the leading cause at 0.90."),
            (11, "INC-1048", "planner", "action_proposed", "Proposed rollback of api. Tier T2."),
            (18, "INC-1042", "inv-logs", "finding", "Resize loop retains a buffer per job."),
            (15, "INC-1042", "planner", "action_proposed", "Proposed a worker restart. Tier T1."),
            (9, "INC-1033", "inv-logs", "finding", "Checkout queries wait on orders."),
            (8, "INC-0988", "on-call", "approval", "Approved scaling the worker."),
        ]
        for minutes, incident_id, actor, kind, summary in sorted(notes, key=lambda item: -item[0]):
            append_audit(db, actor=actor, event_type=kind, summary=summary, incident_id=incident_id, when=_ago(now, minutes))

        db.add(KillSwitch(id=1, active=False, actor=None, updated_at=now))
        db.commit()
    finally:
        db.close()
    print("seeded 10 incidents")


if __name__ == "__main__":
    main()
