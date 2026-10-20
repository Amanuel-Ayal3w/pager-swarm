from collections import defaultdict

from sqlalchemy import select
from sqlalchemy.orm import Session

from pager.storage.models import Action, Approval, Finding, Hypothesis, Incident, Task, TraceStep
from pager.storage.schemas import (
    ActionOut,
    ApprovalOut,
    FindingOut,
    HypothesisOut,
    IncidentDetail,
    IncidentOut,
    TaskOut,
)


def with_cost(db: Session, rows: list[Incident]) -> list[IncidentOut]:
    totals: dict[str, list[float]] = defaultdict(lambda: [0, 0.0])
    steps = db.scalars(select(TraceStep)).all()
    for step in steps:
        bucket = totals[step.incident_id]
        bucket[0] += step.tokens_in + step.tokens_out
        bucket[1] += step.cost
    items: list[IncidentOut] = []
    for row in rows:
        item = IncidentOut.model_validate(row)
        tokens, cost = totals.get(row.id, [0, 0.0])
        item.token_total = int(tokens)
        item.cost_usd = round(float(cost), 4)
        items.append(item)
    return items


def incident_detail(db: Session, incident: Incident) -> IncidentDetail:
    base = with_cost(db, [incident])[0]
    findings = db.scalars(
        select(Finding).where(Finding.incident_id == incident.id).order_by(Finding.confidence.desc())
    ).all()
    hypotheses = db.scalars(
        select(Hypothesis).where(Hypothesis.incident_id == incident.id).order_by(Hypothesis.confidence.desc())
    ).all()
    actions = db.scalars(
        select(Action).where(Action.incident_id == incident.id).order_by(Action.created_at.desc())
    ).all()
    tasks = db.scalars(select(Task).where(Task.incident_id == incident.id).order_by(Task.created_at)).all()
    approvals = db.scalars(
        select(Approval).join(Action).where(Action.incident_id == incident.id).order_by(Approval.timestamp)
    ).all()
    return IncidentDetail(
        **base.model_dump(),
        findings=[FindingOut.model_validate(row) for row in findings],
        hypotheses=[HypothesisOut.model_validate(row) for row in hypotheses],
        actions=[ActionOut.model_validate(row) for row in actions],
        tasks=[TaskOut.model_validate(row) for row in tasks],
        approvals=[ApprovalOut.model_validate(row) for row in approvals],
    )
