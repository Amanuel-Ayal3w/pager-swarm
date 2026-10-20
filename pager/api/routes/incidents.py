from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from pager.api.serialize import incident_detail, with_cost
from pager.storage.db import get_db
from pager.storage.models import Incident, Task
from pager.storage.schemas import IncidentDetail, IncidentOut, TaskOut

router = APIRouter(tags=["incidents"])


@router.get("/incidents", response_model=list[IncidentOut])
def list_incidents(db: Session = Depends(get_db)) -> list[IncidentOut]:
    rows = list(db.scalars(select(Incident).order_by(Incident.opened_at.desc())))
    return with_cost(db, rows)


@router.get("/incidents/{incident_id}", response_model=IncidentDetail)
def get_incident(incident_id: str, db: Session = Depends(get_db)) -> IncidentDetail:
    row = db.get(Incident, incident_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Nothing here yet.")
    return incident_detail(db, row)


@router.get("/agents", response_model=list[TaskOut])
def list_agents(db: Session = Depends(get_db)) -> list[Task]:
    return list(db.scalars(select(Task).where(Task.status == "running").order_by(Task.created_at)))
