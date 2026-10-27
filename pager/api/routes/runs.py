"""Open a real incident. The graph pauses when it needs an approval."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from pager.api.serialize import incident_detail
from pager.graph.board import PostgresBoard
from pager.graph.cancel import request_stop
from pager.graph.run import start_run
from pager.storage.db import SessionLocal, get_db
from pager.storage.models import Incident, Task
from pager.storage.schemas import RunIn, RunOut, StopIn, StopOut
from pager.target.scenarios import SCENARIOS

router = APIRouter(tags=["runs"])

_STOPPABLE = {"DETECTED", "INVESTIGATING", "DIAGNOSED", "REMEDIATING"}


def _stop_rows(incident_id: str | None) -> list[str]:
    request_stop(incident_id)
    with SessionLocal() as db:
        query = select(Task).where(Task.status == "running")
        if incident_id:
            query = query.where(Task.incident_id == incident_id)
        rows = list(db.scalars(query))
        ids = list(dict.fromkeys(task.incident_id for task in rows))
        for task in rows:
            task.status = "done"
            task.step = "Stopped."
        db.commit()
    board = PostgresBoard()
    stopped: list[str] = []
    with SessionLocal() as db:
        targets = ids or ([incident_id] if incident_id else [])
        for iid in targets:
            incident = db.get(Incident, iid)
            if incident is None:
                continue
            if incident.state in _STOPPABLE:
                board.set_state(iid, "ESCALATED", summary="Stopped.")
            board.note(iid, "operator", "state", "Stopped.")
            stopped.append(iid)
    return stopped


@router.post("/runs/stop", response_model=StopOut)
def stop_run(body: StopIn) -> StopOut:
    return StopOut(stopped=_stop_rows(body.incident_id))


@router.post("/runs", response_model=RunOut)
def open_run(body: RunIn, db: Session = Depends(get_db)) -> RunOut:
    if body.scenario not in SCENARIOS:
        raise HTTPException(status_code=404, detail="Nothing here yet.")
    try:
        result = start_run(body.scenario, model=body.model, api_key=body.api_key)
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        if type(exc).__name__ == "RateLimitError":
            raise HTTPException(status_code=400, detail="The model rate limit was reached. Wait a minute and try again.") from exc
        raise
    incident = db.get(Incident, result["incident_id"])
    if incident is None:
        raise HTTPException(status_code=500, detail="That didn't work. Try again.")
    return RunOut(paused=result["paused"], incident=incident_detail(db, incident))
