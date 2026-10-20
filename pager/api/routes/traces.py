from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from pager.storage.db import get_db
from pager.storage.models import Incident, TraceStep
from pager.storage.schemas import TraceStepOut

router = APIRouter(tags=["traces"])


@router.get("/incidents/{incident_id}/trace", response_model=list[TraceStepOut])
def get_trace(incident_id: str, db: Session = Depends(get_db)) -> list[TraceStep]:
    if db.get(Incident, incident_id) is None:
        raise HTTPException(status_code=404, detail="Nothing here yet.")
    return list(
        db.scalars(
            select(TraceStep).where(TraceStep.incident_id == incident_id).order_by(TraceStep.step_no)
        )
    )
