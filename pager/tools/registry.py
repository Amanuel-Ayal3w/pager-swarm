"""Validate, authorize, then run. The model never skips this path."""

from dataclasses import dataclass
from typing import Callable

from pydantic import BaseModel, ValidationError

from pager.safety.allowlist import Denied
from pager.safety.gates import authorize, tier_of
from pager.target.client import TargetDown, get_target
from pager.tools import handlers
from pager.tools.schemas import (
    Empty,
    GitDiff,
    ListDeploys,
    QueryMetrics,
    ReadLogs,
    ScaleService,
    SearchLogs,
    ServiceName,
    UpdateConfig,
)


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    model: type[BaseModel]
    run: Callable
    preview: Callable


@dataclass
class ToolResult:
    ok: bool
    output: dict
    target_url: str
    tier: str
    dry_run: bool = False
    error: str | None = None
    code: str | None = None


def _read(name: str, description: str, model: type[BaseModel], handler: Callable) -> ToolSpec:
    return ToolSpec(name, description, model, handler, handler)


TOOLS: dict[str, ToolSpec] = {
    spec.name: spec
    for spec in (
        _read("read_logs", "Read recent logs for one service.", ReadLogs, handlers.read_logs),
        _read("search_logs", "Search logs for one service.", SearchLogs, handlers.search_logs),
        _read("query_metrics", "Read current metrics for one service.", QueryMetrics, handlers.query_metrics),
        _read("list_recent_deploys", "List recent deploys for one service.", ListDeploys, handlers.list_recent_deploys),
        _read("get_git_diff", "Show the diff for one deploy.", GitDiff, handlers.get_git_diff),
        _read("docker_ps", "List service status in the target.", Empty, handlers.docker_ps),
        _read("service_health", "Check whether one service is healthy.", ServiceName, handlers.service_health),
        ToolSpec(
            "restart_service",
            "Restart one service process.",
            ServiceName,
            handlers.run_restart,
            handlers.preview_restart,
        ),
        ToolSpec(
            "rollback_deploy",
            "Roll one service back to its previous deploy.",
            ServiceName,
            handlers.run_rollback,
            handlers.preview_rollback,
        ),
        ToolSpec(
            "scale_service",
            "Change the replica count of one service.",
            ScaleService,
            handlers.run_scale,
            handlers.preview_scale,
        ),
        ToolSpec(
            "update_config",
            "Change an allowlisted config key on one service.",
            UpdateConfig,
            handlers.run_config,
            handlers.preview_config,
        ),
        ToolSpec(
            "clear_cache",
            "Clear cached files on one service host.",
            ServiceName,
            handlers.run_cache,
            handlers.preview_cache,
        ),
    )
}


def tier(name: str) -> str:
    return tier_of(name)


def specs_for(names: list[str]) -> list[dict]:
    specs = []
    for name in names:
        spec = TOOLS[name]
        specs.append(
            {
                "name": spec.name,
                "description": spec.description,
                "input_schema": spec.model.model_json_schema(),
            }
        )
    return specs


def execute(
    name: str,
    args: dict | None,
    target_url: str,
    *,
    role: str,
    approved: bool = False,
    dry_run: bool = False,
    kill_active: bool = False,
    recent_actions: int = 0,
) -> ToolResult:
    rank = tier_of(name)
    try:
        mode = authorize(
            name,
            role=role,
            approved=approved,
            dry_run=dry_run,
            kill_active=kill_active,
            recent_actions=recent_actions,
        )
    except Denied as exc:
        return ToolResult(False, {}, target_url, rank, error=str(exc), code=exc.code)

    spec = TOOLS.get(name)
    if spec is None:
        return ToolResult(False, {}, target_url, rank, error="This action is forbidden.", code="forbidden")
    try:
        parsed = spec.model.model_validate(args or {})
    except Denied as exc:
        return ToolResult(False, {}, target_url, rank, error=str(exc), code=exc.code)
    except ValidationError as exc:
        return ToolResult(False, {}, target_url, rank, error=exc.errors()[0]["msg"], code="bad_args")

    try:
        target = get_target(target_url)
    except KeyError:
        return ToolResult(False, {}, target_url, rank, error="The target is not available.", code="target_down")

    try:
        if mode == "dry_run":
            return ToolResult(True, spec.preview(parsed, target), target_url, rank, dry_run=True)
        output = spec.run(parsed, target)
    except TargetDown as exc:
        return ToolResult(False, {}, target_url, rank, error=str(exc), code="target_down")
    return ToolResult(True, output, target_url, rank)
