"""Append-only audit rows and the Redis fan-out for the live feed."""

import hashlib
import json
from datetime import datetime, timezone

import redis
from sqlalchemy import select
from sqlalchemy.orm import Session

from pager.config import settings
from pager.storage.models import AuditEvent, StreamEvent

CHANNEL = "pager:events"


def _now() -> datetime:
    return datetime.now(timezone.utc)


def append_audit(
    db: Session,
    *,
    actor: str,
    event_type: str,
    summary: str,
    payload: dict | None = None,
    incident_id: str | None = None,
    when: datetime | None = None,
) -> StreamEvent:
    payload = {"summary": summary, **(payload or {})}
    last = db.scalar(select(AuditEvent).order_by(AuditEvent.id.desc()).limit(1))
    prev = last.this_hash if last else "0" * 64
    body = json.dumps(
        {"actor": actor, "event_type": event_type, "summary": summary, "payload": payload},
        sort_keys=True,
        default=str,
    )
    digest = hashlib.sha256(f"{prev}|{body}".encode()).hexdigest()
    now = when or _now()
    db.add(
        AuditEvent(
            timestamp=now,
            actor=actor,
            event_type=event_type,
            incident_id=incident_id,
            payload=payload,
            prev_hash=prev,
            this_hash=digest,
        )
    )
    event = StreamEvent(
        incident_id=incident_id,
        event_type=event_type,
        actor=actor,
        summary=summary,
        payload=payload,
        created_at=now,
    )
    db.add(event)
    db.flush()
    return event


def publish(event: StreamEvent) -> None:
    payload = {
        "id": event.id,
        "incident_id": event.incident_id,
        "event_type": event.event_type,
        "actor": event.actor,
        "summary": event.summary,
        "payload": event.payload,
        "created_at": event.created_at.isoformat(),
    }
    client = redis.Redis.from_url(settings.redis_url)
    try:
        client.publish(CHANNEL, json.dumps(payload))
    finally:
        client.close()
