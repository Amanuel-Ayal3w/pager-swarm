"""One agent: call the model, run the tool through the registry, repeat."""

import json

from pager.graph.model import Turn
from pager.safety.budget import Budget, BudgetExceeded
from pager.tools.registry import execute, specs_for


class Halt(Exception):
    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(reason)


def run_agent(
    model,
    board,
    *,
    incident_id: str,
    role: str,
    agent_id: str,
    focus: str,
    services: list[str],
    target_url: str,
    prompt: str,
    tool_names: list[str],
    max_steps: int = 6,
    dry_run: bool = False,
    approved: bool = False,
) -> dict:
    messages: list[dict] = [{"role": "user", "content": prompt}]
    budget = Budget(max_steps=max_steps)
    tools = specs_for(tool_names) if tool_names else []
    while True:
        if board.kill_active():
            raise Halt("kill_switch")
        turn: Turn = model.complete(messages, tools, role=role, focus=focus, services=services)
        try:
            budget.charge(turn.tokens_in + turn.tokens_out)
        except BudgetExceeded as exc:
            raise Halt(exc.reason) from exc
        calls = []
        if turn.tool_calls:
            messages.append(
                {
                    "role": "assistant",
                    "content": turn.text,
                    "tool_calls": [{"id": call.id, "name": call.name, "args": call.args} for call in turn.tool_calls],
                }
            )
            for call in turn.tool_calls:
                result = execute(
                    call.name,
                    call.args,
                    target_url,
                    role=role,
                    approved=approved,
                    dry_run=dry_run or role == "planner",
                    kill_active=board.kill_active(),
                    recent_actions=board.recent_action_count(),
                )
                calls.append(
                    {
                        "name": call.name,
                        "args": call.args,
                        "ok": result.ok,
                        "code": result.code,
                        "output": result.output,
                    }
                )
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call.id,
                        "name": call.name,
                        "content": json.dumps(result.output or {"error": result.error, "code": result.code}),
                    }
                )
                if result.code == "kill_switch":
                    board.add_trace(
                        incident_id,
                        agent_id,
                        role,
                        prompt[:180],
                        result.error or "Kill switch is on.",
                        calls,
                        turn.tokens_in,
                        turn.tokens_out,
                    )
                    raise Halt("kill_switch")
            board.add_trace(incident_id, agent_id, role, prompt[:180], turn.text, calls, turn.tokens_in, turn.tokens_out)
            continue
        board.add_trace(incident_id, agent_id, role, prompt[:180], turn.text, [], turn.tokens_in, turn.tokens_out)
        return {"text": turn.text, "tokens": budget.tokens}
