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
    latest: dict[str, str] = {}
    steps = db.scalars(select(TraceStep).order_by(TraceStep.created_at, TraceStep.step_no)).all()
    for step in steps:
        bucket = totals[step.incident_id]
        bucket[0] += step.tokens_in + step.tokens_out
        bucket[1] += step.cost
        if step.response:
            latest[step.incident_id] = step.response
    items: list[IncidentOut] = []
    for row in rows:
        item = IncidentOut.model_validate(row)
        tokens, cost = totals.get(row.id, [0, 0.0])
        item.token_total = int(tokens)
        item.cost_usd = round(float(cost), 4)
        item.latest_work = latest.get(row.id, "")
        items.append(item)
    return items


def task_views(db: Session, tasks: list[Task]) -> list[TaskOut]:
    if not tasks:
        return []
    ids = {task.incident_id for task in tasks}
    latest: dict[tuple[str, str], str] = {}
    steps = db.scalars(
        select(TraceStep).where(TraceStep.incident_id.in_(ids)).order_by(TraceStep.created_at, TraceStep.step_no)
    ).all()
    for step in steps:
        if step.response:
            latest[(step.incident_id, step.agent_id)] = step.response
    items: list[TaskOut] = []
    for task in tasks:
        item = TaskOut.model_validate(task)
        item.response = latest.get((task.incident_id, task.agent_id), "")
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
        tasks=task_views(db, list(tasks)),
        approvals=[ApprovalOut.model_validate(row) for row in approvals],
    )
