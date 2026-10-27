"""Checkpointed incident state. Values stay JSON-friendly."""

import operator
from typing import Annotated, TypedDict

from pager.target.scenarios import Scenario


class IncidentState(TypedDict):
    scenario_id: str
    incident_id: str
    thread_id: str
    model_name: str
    mode: str
    title: str
    summary: str
    severity: str
    services: list[str]
    target_url: str
    focus: str
    findings: Annotated[list[dict], operator.add]
    hypothesis: dict
    action: dict
    decision: str
    decision_payload: dict
    outcome: str
    halt: str
    tokens_used: Annotated[int, operator.add]
    rounds: Annotated[int, operator.add]
    verify_attempts: int


def new_state(scenario: Scenario, thread_id: str, model_name: str, target_url: str, mode: str = "swarm") -> IncidentState:
    return {
        "scenario_id": scenario.id,
        "incident_id": "",
        "thread_id": thread_id,
        "model_name": model_name,
        "mode": mode,
        "title": scenario.title,
        "summary": "",
        "severity": scenario.severity,
        "services": list(scenario.services),
        "target_url": target_url,
        "focus": "",
        "findings": [],
        "hypothesis": {},
        "action": {},
        "decision": "",
        "decision_payload": {},
        "outcome": "",
        "halt": "",
        "tokens_used": 0,
        "rounds": 0,
        "verify_attempts": 0,
    }
