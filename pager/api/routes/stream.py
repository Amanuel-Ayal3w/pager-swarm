import asyncio
import json

import redis.asyncio as aioredis
from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from pager.config import settings
from pager.storage.db import SessionLocal, get_db
from pager.storage.events import CHANNEL
from pager.storage.models import StreamEvent
from pager.storage.schemas import StreamEventOut

router = APIRouter(tags=["stream"])


@router.get("/events", response_model=list[StreamEventOut])
def list_events(limit: int = 40, db: Session = Depends(get_db)) -> list[StreamEvent]:
    limit = max(1, min(limit, 200))
    rows = list(db.scalars(select(StreamEvent).order_by(StreamEvent.id.desc()).limit(limit)))
    rows.reverse()
    return rows


def _backfill(last_id: int) -> list[dict]:
    db = SessionLocal()
    try:
        rows = db.scalars(
            select(StreamEvent).where(StreamEvent.id > last_id).order_by(StreamEvent.id).limit(200)
        ).all()
        return [
            {
                "id": row.id,
                "incident_id": row.incident_id,
                "event_type": row.event_type,
                "actor": row.actor,
                "summary": row.summary,
                "payload": row.payload,
                "created_at": row.created_at.isoformat(),
            }
            for row in rows
        ]
    finally:
        db.close()


@router.get("/stream")
async def stream(request: Request) -> StreamingResponse:
    header = request.headers.get("last-event-id")
    last_id = int(header) if header and header.isdigit() else 0

    async def generate():
        for item in _backfill(last_id):
            yield f"id: {item['id']}\ndata: {json.dumps(item)}\n\n"
        client = aioredis.from_url(settings.redis_url)
        pubsub = client.pubsub()
        await pubsub.subscribe(CHANNEL)
        try:
            while True:
                if await request.is_disconnected():
                    break
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=15.0)
                if message and message["type"] == "message":
                    data = message["data"]
                    if isinstance(data, bytes):
                        data = data.decode()
                    parsed = json.loads(data)
                    yield f"id: {parsed['id']}\ndata: {data}\n\n"
                else:
                    yield ": keepalive\n\n"
                await asyncio.sleep(0)
        finally:
            await pubsub.unsubscribe(CHANNEL)
            await pubsub.aclose()
            await client.aclose()

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
