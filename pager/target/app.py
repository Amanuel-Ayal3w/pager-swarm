"""Local target. Fault injection is not a tool."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from pager.safety.allowlist import MAX_REPLICAS
from pager.target.client import MemoryTarget

app = FastAPI(title="Pager target", version="0.1.0")
target = MemoryTarget()


class ServiceBody(BaseModel):
    service: str


class ScaleBody(BaseModel):
    service: str
    replicas: int = Field(ge=1, le=MAX_REPLICAS)


class ConfigBody(BaseModel):
    service: str
    values: dict


@app.get("/health")
def health(service: str = "") -> dict:
    if not service:
        return {"ok": True}
    try:
        return target.health(service)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Nothing here yet.") from exc


@app.get("/logs")
def logs(service: str, limit: int = 20, query: str = "") -> list:
    return target.search_logs(service, query, limit)


@app.get("/metrics")
def metrics(service: str) -> dict:
    return target.metrics(service)


@app.get("/deploys")
def deploys(service: str) -> list:
    return target.deploys(service)


@app.get("/diff")
def diff(deploy_id: str) -> dict:
    return target.diff(deploy_id)


@app.get("/ps")
def ps() -> list:
    return target.ps()


@app.get("/service")
def service(service: str) -> dict:
    return target.service(service)


@app.post("/actions/restart")
def restart(body: ServiceBody) -> dict:
    return target.restart(body.service)


@app.post("/actions/rollback")
def rollback(body: ServiceBody) -> dict:
    return target.rollback(body.service)


@app.post("/actions/scale")
def scale(body: ScaleBody) -> dict:
    return target.scale(body.service, body.replicas)


@app.post("/actions/config")
def config(body: ConfigBody) -> dict:
    return target.update_config(body.service, body.values)


@app.post("/actions/cache")
def cache(body: ServiceBody) -> dict:
    return target.clear_cache(body.service)


@app.post("/faults/{scenario_id}/inject")
def inject(scenario_id: str) -> dict:
    try:
        target.inject(scenario_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Nothing here yet.") from exc
    return {"ok": True}


@app.post("/faults/revert")
def revert() -> dict:
    target.revert()
    return {"ok": True}
