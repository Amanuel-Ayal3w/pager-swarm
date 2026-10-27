"""The incident graph pauses for approval and will not run a fix without one."""

from types import SimpleNamespace

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

from pager.graph.board import MemoryBoard
from pager.graph.build import build_graph
from pager.graph.loop import run_agent
from pager.graph.model import OpenAIModel, ScriptedModel
from pager.graph.nodes import bind, release
from pager.graph.state import new_state
from pager.target.client import MemoryTarget, get_target, register_target
from pager.target.scenarios import broken_world, get_scenario


def _drive(graph, payload, thread_id: str, board: MemoryBoard, model):
    bind(thread_id, board, model)
    try:
        return graph.invoke(payload, {"configurable": {"thread_id": thread_id}})
    finally:
        release(thread_id)


def _run(scenario_id: str, board: MemoryBoard | None = None, mode: str = "swarm", thread_id: str = "thread-1"):
    board = board or MemoryBoard()
    model = ScriptedModel()
    graph = build_graph(InMemorySaver())
    url = f"memory://{thread_id}-{scenario_id}-{mode}"
    register_target(url, MemoryTarget(broken_world(scenario_id)))
    state = new_state(get_scenario(scenario_id), thread_id, "scripted", url, mode=mode)
    result = _drive(graph, state, thread_id, board, model)
    return graph, board, model, result, url


def _mark_approved(board: MemoryBoard) -> None:
    action = board.actions[-1]
    action["status"] = "approved"
    action["decision"] = "approve"
    action["approved_version"] = action["version"]
    action["typed_confirmation"] = action["confirmation_phrase"]


def test_bad_deploy_pauses_on_a_t2_rollback():
    graph, board, model, result, url = _run("bad_deploy")
    assert "__interrupt__" in result
    assert len(board.findings) == 4
    action = board.actions[-1]
    assert action["tool"] == "rollback_deploy"
    assert action["tier"] == "T2"
    assert action["confirmation_phrase"] == "rollback api"
    assert "AWAITING_APPROVAL" in board.states
    assert get_target(url).snapshot()["services"]["api"]["error_rate"] == 0.42
    assert "world" not in graph.get_state({"configurable": {"thread_id": "thread-1"}}).values
    del model


def test_resume_without_approval_does_not_change_the_service():
    graph, board, model, _result, url = _run("bad_deploy", thread_id="thread-unapproved")
    _drive(graph, Command(resume={"decision": "approve"}), "thread-unapproved", board, model)
    snap = graph.get_state({"configurable": {"thread_id": "thread-unapproved"}})
    assert get_target(url).snapshot()["services"]["api"]["error_rate"] == 0.42
    assert snap.values["outcome"] == "escalated"


def test_approved_rollback_resolves_the_incident():
    graph, board, model, _result, url = _run("bad_deploy", thread_id="thread-approved")
    _mark_approved(board)
    _drive(
        graph,
        Command(resume={"decision": "approve", "typed_confirmation": "rollback api", "action_version": 1}),
        "thread-approved",
        board,
        model,
    )
    snap = graph.get_state({"configurable": {"thread_id": "thread-approved"}})
    assert get_target(url).snapshot()["services"]["api"]["error_rate"] == 0.01
    assert snap.values["outcome"] == "resolved"
    assert board.states[-1] == "RESOLVED"


def test_baseline_uses_one_investigator():
    _graph, board, _model, result, _url = _run("bad_deploy", mode="baseline", thread_id="thread-base")
    assert "__interrupt__" in result
    assert len(board.findings) == 1
    assert board.actions[-1]["tool"] == "rollback_deploy"


def test_memory_leak_proposes_a_t1_restart():
    _graph, board, _model, result, _url = _run("memory_leak")
    assert "__interrupt__" in result
    action = board.actions[-1]
    assert action["tool"] == "restart_service"
    assert action["args"]["service"] == "worker"
    assert action["tier"] == "T1"
    assert action["confirmation_phrase"] is None


def test_injection_does_not_become_an_action():
    _graph, board, _model, result, _url = _run("prompt_injection")
    assert "__interrupt__" not in result
    assert board.actions == []
    assert "CLOSED_NO_ACTION" in board.states
    assert any("treated as data" in finding["summary"] for finding in board.findings)


def test_kill_switch_opens_nothing_actionable():
    board = MemoryBoard()
    board.kill = True
    _graph, board, _model, result, _url = _run("bad_deploy", board, thread_id="thread-kill")
    assert "__interrupt__" not in result
    assert board.actions == []
    assert "ESCALATED" in board.states


def test_openai_loop_runs_the_tool_then_stops():
    calls = []

    class Responses:
        def create(self, **kwargs):
            calls.append(kwargs)
            usage = SimpleNamespace(input_tokens=4, output_tokens=3)
            if len(calls) == 1:
                item = SimpleNamespace(
                    type="function_call",
                    call_id="t1",
                    name="search_logs",
                    arguments='{"service": "api", "query": ""}',
                )
                return SimpleNamespace(output=[item], output_text="", usage=usage)
            return SimpleNamespace(
                output=[],
                output_text='{"summary": "checkout failed after deploy", "confidence": 0.8, "evidence_refs": ["L1"], "hypothesis": "deploy"}',
                usage=usage,
            )

    board = MemoryBoard()
    url = "memory://openai"
    register_target(url, MemoryTarget(broken_world("bad_deploy")))
    result = run_agent(
        OpenAIModel(client=SimpleNamespace(responses=Responses())),
        board,
        incident_id="INC-1",
        role="investigator",
        agent_id="inv-logs",
        focus="logs",
        services=["api"],
        target_url=url,
        prompt="Look at the logs.",
        tool_names=["search_logs"],
    )
    assert "after deploy" in result["text"]
    assert calls[0]["tools"][0]["type"] == "function"
    assert calls[1]["input"][-1]["type"] == "function_call_output"
    assert board.traces[0]["tool_calls"][0]["name"] == "search_logs"
