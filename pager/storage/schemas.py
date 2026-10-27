from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class IncidentOut(ORMModel):
    id: str
    title: str
    summary: str
    severity: str
    state: str
    opened_at: datetime
    closed_at: datetime | None
    root_cause: str | None
    resolution: str | None
    thread_id: str | None
    affected_services: list[str]
    cost_usd: float = 0
    token_total: int = 0
    latest_work: str = ""


class TaskOut(ORMModel):
    id: str
    incident_id: str
    agent_id: str
    agent_role: str
    description: str
    status: str
    step: str
    tokens: int
    response: str = ""
    created_at: datetime


class FindingOut(ORMModel):
    id: str
    incident_id: str
    agent_id: str
    summary: str
    evidence_refs: list
    confidence: float
    created_at: datetime


class HypothesisOut(ORMModel):
    id: str
    incident_id: str
    description: str
    confidence: float
    status: str
    created_at: datetime


class ActionOut(ORMModel):
    id: str
    incident_id: str
    tool: str
    args: dict
    tier: str
    risk: str
    blast_radius: str
    rollback_plan: str
    expected_outcome: str
    confirmation_phrase: str | None
    status: str
    version: int
    created_at: datetime


class ApprovalOut(ORMModel):
    id: str
    action_id: str
    operator: str
    decision: str
    reason: str | None
    typed_confirmation: str | None
    action_version: int
    timestamp: datetime


class TraceStepOut(ORMModel):
    id: str
    incident_id: str
    agent_id: str
    agent_role: str
    step_no: int
    prompt_ref: str
    response: str
    tool_calls: list
    tokens_in: int
    tokens_out: int
    cost: float
    latency_ms: int
    created_at: datetime


class AuditEventOut(ORMModel):
    id: int
    timestamp: datetime
    actor: str
    event_type: str
    incident_id: str | None
    payload: dict
    prev_hash: str
    this_hash: str


class StreamEventOut(ORMModel):
    id: int
    incident_id: str | None
    event_type: str
    actor: str
    summary: str
    payload: dict
    created_at: datetime


class KillSwitchOut(ORMModel):
    active: bool
    actor: str | None
    updated_at: datetime


class KillSwitchIn(BaseModel):
    active: bool
    operator: str = Field(min_length=1, max_length=120)


class DecisionIn(BaseModel):
    decision: Literal["approve", "reject", "investigate"]
    operator: str = Field(min_length=1, max_length=120)
    reason: str | None = None
    typed_confirmation: str | None = None
    action_version: int


class HealthOut(BaseModel):
    status: str
    database: str
    redis: str


class IncidentDetail(IncidentOut):
    findings: list[FindingOut] = []
    hypotheses: list[HypothesisOut] = []
    actions: list[ActionOut] = []
    tasks: list[TaskOut] = []
    approvals: list[ApprovalOut] = []


class RunIn(BaseModel):
    scenario: str = "bad_deploy"
    model: Literal["scripted", "openai"] | None = None
    api_key: str | None = None


class RunOut(BaseModel):
    paused: bool
    incident: IncidentDetail


class StopIn(BaseModel):
    incident_id: str | None = None


class StopOut(BaseModel):
    stopped: list[str]
