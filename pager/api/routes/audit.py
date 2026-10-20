from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from pager.storage.db import get_db
from pager.storage.models import AuditEvent
from pager.storage.schemas import AuditEventOut

router = APIRouter(tags=["audit"])


@router.get("/audit", response_model=list[AuditEventOut])
def list_audit(
    incident_id: str | None = None,
    actor: str | None = None,
    event_type: str | None = None,
    db: Session = Depends(get_db),
) -> list[AuditEvent]:
    query = select(AuditEvent)
    if incident_id:
        query = query.where(AuditEvent.incident_id == incident_id)
    if actor:
        query = query.where(AuditEvent.actor.ilike(f"%{actor}%"))
    if event_type:
        query = query.where(AuditEvent.event_type == event_type)
    query = query.order_by(AuditEvent.id.desc()).limit(200)
    return list(db.scalars(query))
