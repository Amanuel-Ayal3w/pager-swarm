from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from pager.storage.db import get_db
from pager.storage.events import append_audit, publish
from pager.storage.models import KillSwitch
from pager.storage.schemas import KillSwitchIn, KillSwitchOut

router = APIRouter(tags=["killswitch"])


def _row(db: Session) -> KillSwitch:
    row = db.get(KillSwitch, 1)
    if row is None:
        row = KillSwitch(id=1, active=False, actor=None, updated_at=datetime.now(timezone.utc))
        db.add(row)
        db.commit()
        db.refresh(row)
    return row


@router.get("/killswitch", response_model=KillSwitchOut)
def get_killswitch(db: Session = Depends(get_db)) -> KillSwitch:
    return _row(db)


@router.post("/killswitch", response_model=KillSwitchOut)
def set_killswitch(body: KillSwitchIn, db: Session = Depends(get_db)) -> KillSwitch:
    row = _row(db)
    row.active = body.active
    row.actor = body.operator
    row.updated_at = datetime.now(timezone.utc)
    summary = "Kill switch is on." if body.active else "Kill switch is off."
    event = append_audit(
        db,
        actor=body.operator,
        event_type="kill_switch",
        summary=summary,
        payload={"active": body.active},
    )
    db.commit()
    db.refresh(row)
    db.refresh(event)
    publish(event)
    return row
