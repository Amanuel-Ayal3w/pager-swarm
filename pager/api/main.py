from contextlib import asynccontextmanager

import redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from pager.config import settings
from pager.storage.db import SessionLocal, init_db
from pager.storage.models import KillSwitch
from pager.api.routes import approvals, audit, incidents, killswitch, stream, traces


def _ensure_kill_switch() -> None:
    db = SessionLocal()
    try:
        if db.get(KillSwitch, 1) is None:
            db.add(KillSwitch(id=1, active=False, actor=None))
            db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    _ensure_kill_switch()
    yield


app = FastAPI(title="Pager", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.web_origin,
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(incidents.router, prefix="/api")
app.include_router(traces.router, prefix="/api")
app.include_router(approvals.router, prefix="/api")
app.include_router(audit.router, prefix="/api")
app.include_router(killswitch.router, prefix="/api")
app.include_router(stream.router, prefix="/api")


@app.get("/api/health")
def health() -> dict:
    database = "ok"
    redis_status = "ok"
    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
    except Exception:
        database = "down"
    try:
        client = redis.Redis.from_url(settings.redis_url)
        client.ping()
        client.close()
    except Exception:
        redis_status = "down"
    return {"status": "ok" if database == "ok" and redis_status == "ok" else "degraded", "database": database, "redis": redis_status}
