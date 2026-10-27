"""Start an investigation, or resume one after an approval."""

import argparse
import uuid
from contextlib import contextmanager

from langgraph.types import Command

from pager.config import settings
from pager.graph.board import PostgresBoard
from pager.graph.build import build_graph
from pager.graph.cancel import Stopped, caused_by_stop, close_run, open_run
from pager.graph.model import resolve_model
from pager.graph.nodes import bind, release
from pager.graph.state import new_state
from pager.target.scenarios import SCENARIOS, get_scenario


def checkpoint_url() -> str:
    return settings.database_url.replace("postgresql+psycopg", "postgresql", 1)


@contextmanager
def graph_session():
    from langgraph.checkpoint.postgres import PostgresSaver

    with PostgresSaver.from_conn_string(checkpoint_url()) as saver:
        saver.setup()
        yield build_graph(saver)


def _config(thread_id: str) -> dict:
    return {"configurable": {"thread_id": thread_id}}


_RUN_KEYS: dict[str, str] = {}


def start_run(
    scenario_id: str,
    model: str | None = None,
    thread_id: str | None = None,
    mode: str = "swarm",
    api_key: str | None = None,
) -> dict:
    from pager.target.server import ensure_running, inject

    scenario = get_scenario(scenario_id)
    thread_id = thread_id or str(uuid.uuid4())
    key = (api_key or "").strip()
    if key:
        _RUN_KEYS[thread_id] = key
    control = open_run(thread_id)
    model_name, chosen = resolve_model(model, api_key=key or None, control=control)
    url = ensure_running()
    inject(scenario_id, url)
    state = new_state(scenario, thread_id, model_name, url, mode=mode)
    board = PostgresBoard()
    board.upsert_scenario(scenario)
    config = _config(thread_id)
    stopped = False
    snap = None
    with graph_session() as graph:
        bind(thread_id, board, chosen)
        try:
            try:
                graph.invoke(state, config)
            except Stopped:
                stopped = True
            except Exception as exc:
                if not caused_by_stop(exc):
                    raise
                stopped = True
            if not stopped:
                snap = graph.get_state(config)
        finally:
            release(thread_id)
            close_run(thread_id)
    if stopped:
        return {
            "incident_id": board.incident_id,
            "thread_id": thread_id,
            "paused": False,
            "outcome": "stopped",
        }
    values = (snap.values or {}) if snap is not None else {}
    return {
        "incident_id": values.get("incident_id") or board.incident_id,
        "thread_id": thread_id,
        "paused": bool(snap.next) if snap is not None else False,
        "outcome": values.get("outcome") or "",
    }


def resume_if_paused(thread_id: str, decision: dict) -> bool:
    config = _config(thread_id)
    with graph_session() as graph:
        snap = graph.get_state(config)
        if not getattr(snap, "next", None):
            return False
        model_name = (snap.values or {}).get("model_name")
        _name, chosen = resolve_model(model_name, api_key=_RUN_KEYS.get(thread_id))
        board = PostgresBoard()
        bind(thread_id, board, chosen)
        try:
            graph.invoke(Command(resume=decision), config)
        finally:
            release(thread_id)
    return True


def decision_from_answer(
    answer: str,
    *,
    version: int,
    reason: str = "",
    typed: str = "",
    operator: str = "on-call",
):
    from pager.storage.schemas import DecisionIn

    choice = answer.strip().lower()
    if choice in {"y", "yes"}:
        return DecisionIn(decision="approve", operator=operator, typed_confirmation=typed or None, action_version=version)
    if choice in {"n", "no"}:
        return DecisionIn(decision="reject", operator=operator, reason=reason, action_version=version)
    if choice in {"i", "investigate"}:
        return DecisionIn(decision="investigate", operator=operator, action_version=version)
    return None


def prompt_decision(action: dict):
    while True:
        answer = input("approve? y/n/i ")
        typed = ""
        reason = ""
        if answer.strip().lower() in {"y", "yes"} and action.get("tier") == "T2":
            typed = input(f"Type `{action.get('confirmation_phrase')}`: ")
        if answer.strip().lower() in {"n", "no"}:
            reason = input("reason: ")
        body = decision_from_answer(answer, version=action["version"], reason=reason, typed=typed)
        if body is not None:
            return body
        print("Answer y, n, or i.")


def submit_decision(action: dict, body) -> str:
    from fastapi import HTTPException

    from pager.api.routes.approvals import decide
    from pager.storage.db import SessionLocal

    db = SessionLocal()
    try:
        detail = decide(action["id"], body, db)
    except HTTPException as exc:
        payload = exc.detail if isinstance(exc.detail, dict) else {"message": str(exc.detail)}
        return str(payload.get("message") or "That didn't work. Try again.")
    finally:
        db.close()
    return f"{detail.id} is {detail.state}."


def _proposal(incident_id: str) -> dict | None:
    from sqlalchemy import select

    from pager.storage.db import SessionLocal
    from pager.storage.models import Action

    with SessionLocal() as db:
        action = db.scalar(
            select(Action).where(Action.incident_id == incident_id, Action.status == "proposed").order_by(Action.created_at.desc())
        )
        if action is None:
            return None
        return {
            "id": action.id,
            "incident_id": action.incident_id,
            "tool": action.tool,
            "tier": action.tier,
            "version": action.version,
            "confirmation_phrase": action.confirmation_phrase,
        }


def latest_waiting() -> dict | None:
    from sqlalchemy import select

    from pager.storage.db import SessionLocal
    from pager.storage.models import Incident

    with SessionLocal() as db:
        incident = db.scalar(
            select(Incident).where(Incident.state == "AWAITING_APPROVAL").order_by(Incident.opened_at.desc())
        )
    if incident is None:
        return None
    return _proposal(incident.id)


def approve_action(action: dict) -> str:
    print(f"{action['incident_id']} proposes {action['tool']} ({action['tier']}).")
    return submit_decision(action, prompt_decision(action))


def main() -> None:
    parser = argparse.ArgumentParser(description="Open an incident and investigate it.")
    parser.add_argument("--scenario", default="bad_deploy", choices=sorted(SCENARIOS))
    parser.add_argument("--model", default=None, choices=["scripted", "openai"])
    parser.add_argument("--mode", default="swarm", choices=["swarm", "baseline"])
    parser.add_argument("--approve", action="store_true", help="Ask approve? y/n/i after the graph pauses.")
    parser.add_argument("--latest", action="store_true", help="Decide the incident that is already waiting.")
    args = parser.parse_args()
    if args.latest:
        action = latest_waiting()
        if action is None:
            print("Nothing is waiting.")
            return
        if args.approve:
            print(approve_action(action))
            return
        print(f"paused on {action['incident_id']}. Approve it on the board.")
        return
    result = start_run(args.scenario, model=args.model, mode=args.mode)
    if result["paused"] and args.approve:
        action = _proposal(result["incident_id"])
        if action is None:
            print(f"paused on {result['incident_id']}. Approve it on the board.")
            return
        print(approve_action(action))
        return
    if result["paused"]:
        print(f"paused on {result['incident_id']}. Approve it on the board.")
        return
    print(f"{result['incident_id']} {result['outcome']}.")


if __name__ == "__main__":
    main()
