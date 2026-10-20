from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from pager.storage.db import get_db
from pager.storage.models import Incident, Task
from pager.storage.schemas import IncidentOut, TaskOut

router = APIRouter(tags=["incidents"])


@router.get("/incidents", response_model=list[IncidentOut])
def list_incidents(db: Session = Depends(get_db)) -> list[Incident]:
    return list(db.scalars(select(Incident).order_by(Incident.opened_at.desc())))


@router.get("/incidents/{incident_id}", response_model=IncidentOut)
def get_incident(incident_id: str, db: Session = Depends(get_db)) -> Incident:
    row = db.get(Incident, incident_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Nothing here yet.")
    return row


@router.get("/agents", response_model=list[TaskOut])
def list_agents(db: Session = Depends(get_db)) -> list[Task]:
    return list(db.scalars(select(Task).where(Task.status == "running").order_by(Task.created_at)))
