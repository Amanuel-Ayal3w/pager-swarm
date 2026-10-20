from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from pager.api.serialize import incident_detail
from pager.storage.db import get_db
from pager.storage.events import append_audit, publish
from pager.storage.models import Action, Approval, KillSwitch
from pager.storage.schemas import DecisionIn, IncidentDetail

router = APIRouter(tags=["approvals"])


def _fail(db: Session, status: int, code: str, message: str, **payload: object) -> None:
    event = append_audit(
        db,
        actor=str(payload.get("operator") or "operator"),
        event_type="decision_rejected",
        summary=message,
        incident_id=payload.get("incident_id") if isinstance(payload.get("incident_id"), str) else None,
        payload={"code": code, **payload},
    )
    db.commit()
    publish(event)
    raise HTTPException(status_code=status, detail={"code": code, "message": message})


@router.post("/actions/{action_id}/decision", response_model=IncidentDetail)
def decide(action_id: str, body: DecisionIn, db: Session = Depends(get_db)) -> IncidentDetail:
    action = db.get(Action, action_id)
    if action is None:
        raise HTTPException(status_code=404, detail="Nothing here yet.")
    incident = action.incident
    kill = db.get(KillSwitch, 1)

    if body.decision == "approve" and kill is not None and kill.active:
        _fail(db, 409, "kill_switch", "Kill switch is on. Actions are blocked.", operator=body.operator, incident_id=incident.id, action_id=action.id)

    if body.decision in {"approve", "reject"} and incident.state != "AWAITING_APPROVAL":
        _fail(db, 409, "bad_state", "That action is not waiting for approval.", operator=body.operator, incident_id=incident.id, action_id=action.id)

    if body.decision == "approve" and action.status != "proposed":
        _fail(db, 409, "bad_state", "That action is not waiting for approval.", operator=body.operator, incident_id=incident.id, action_id=action.id)

    if body.action_version != action.version:
        _fail(db, 409, "version_mismatch", "This proposal changed. Review it again.", operator=body.operator, incident_id=incident.id, action_id=action.id)

    if body.decision == "approve" and action.tier == "T3":
        _fail(db, 403, "forbidden", "This action is forbidden.", operator=body.operator, incident_id=incident.id, action_id=action.id)

    if body.decision == "approve" and action.tier == "T2":
        typed = (body.typed_confirmation or "").strip()
        if typed != (action.confirmation_phrase or ""):
            _fail(db, 422, "confirmation_mismatch", "Confirmation does not match.", operator=body.operator, incident_id=incident.id, action_id=action.id)

    if body.decision == "reject" and not (body.reason or "").strip():
        raise HTTPException(status_code=422, detail={"code": "reason_required", "message": "Add a reason for the rejection."})

    if body.decision == "investigate" and incident.state not in {"AWAITING_APPROVAL", "DIAGNOSED"}:
        _fail(db, 409, "bad_state", "Investigation is already underway.", operator=body.operator, incident_id=incident.id, action_id=action.id)

    now = datetime.now(timezone.utc)
    if body.decision == "approve":
        action.status = "approved"
        incident.state = "REMEDIATING"
        summary = f"Approved {action.tool}."
    elif body.decision == "reject":
        action.status = "rejected"
        incident.state = "DIAGNOSED"
        summary = "Rejected the proposed action."
    else:
        incident.state = "INVESTIGATING"
        summary = "Asked for more investigation."

    db.add(
        Approval(
            action_id=action.id,
            operator=body.operator,
            decision=body.decision,
            reason=(body.reason or "").strip() or None,
            typed_confirmation=(body.typed_confirmation or "").strip() or None,
            action_version=action.version,
            timestamp=now,
        )
    )
    event = append_audit(
        db,
        actor=body.operator,
        event_type="approval",
        summary=summary,
        incident_id=incident.id,
        payload={"decision": body.decision, "action_id": action.id, "version": action.version, "reason": body.reason},
        when=now,
    )
    db.commit()
    db.refresh(incident)
    publish(event)
    return incident_detail(db, incident)
