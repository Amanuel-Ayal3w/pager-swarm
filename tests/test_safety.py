"""Tool calls stop at the registry, including when a log line asks them not to."""

from pager.target.client import MemoryTarget, get_target, register_target
from pager.target.scenarios import broken_world
from pager.target.world import healthy_world
from pager.tools.registry import TOOLS, execute


def _url(world: dict, name: str) -> str:
    url = f"memory://{name}"
    register_target(url, MemoryTarget(world))
    return url


def _snap(url: str) -> dict:
    return get_target(url).snapshot()


def test_logs_are_wrapped_as_untrusted():
    url = _url(broken_world("prompt_injection"), "logs")
    result = execute("search_logs", {"service": "api", "query": ""}, url, role="investigator")
    assert result.ok
    assert result.output["untrusted"] is True
    assert "drop_database" in str(result.output["content"])


def test_unknown_tool_is_forbidden():
    world = healthy_world()
    url = _url(world, "forbidden")
    result = execute("drop_database", {"service": "postgres"}, url, role="executor", approved=True)
    assert result.code == "forbidden"
    assert _snap(url) == world


def test_fault_injection_is_not_a_tool():
    assert "inject" not in TOOLS
    assert "revert" not in TOOLS


def test_unknown_service_is_rejected():
    url = _url(healthy_world(), "billing")
    result = execute("restart_service", {"service": "billing"}, url, role="executor", approved=True)
    assert result.code == "not_allowlisted"


def test_config_keys_are_allowlisted():
    url = _url(healthy_world(), "config")
    result = execute(
        "update_config",
        {"service": "postgres", "values": {"drop_table": True}},
        url,
        role="executor",
        approved=True,
    )
    assert result.code == "bad_args"


def test_unapproved_restart_does_not_change_memory():
    url = _url(broken_world("memory_leak"), "unapproved")
    result = execute("restart_service", {"service": "worker"}, url, role="executor")
    assert result.code == "unapproved"
    assert _snap(url)["services"]["worker"]["memory_mb"] == 1800


def test_planner_can_dry_run_but_not_execute():
    url = _url(broken_world("memory_leak"), "planner")
    preview = execute("restart_service", {"service": "worker"}, url, role="planner", dry_run=True)
    assert preview.ok and preview.dry_run
    assert _snap(url)["services"]["worker"]["memory_mb"] == 1800
    refused = execute("restart_service", {"service": "worker"}, url, role="planner", approved=True)
    assert refused.code == "not_permitted"


def test_approved_restart_clears_the_leak():
    url = _url(broken_world("memory_leak"), "approved")
    result = execute("restart_service", {"service": "worker"}, url, role="executor", approved=True)
    assert result.ok
    assert _snap(url)["services"]["worker"]["memory_mb"] == 256


def test_kill_switch_blocks_reads():
    url = _url(healthy_world(), "kill")
    result = execute("query_metrics", {"service": "api"}, url, role="triager", kill_active=True)
    assert result.code == "kill_switch"


def test_rate_limit_blocks_another_action():
    url = _url(broken_world("full_disk"), "rate")
    result = execute(
        "clear_cache",
        {"service": "postgres"},
        url,
        role="executor",
        approved=True,
        recent_actions=5,
    )
    assert result.code == "rate_limit"
    assert _snap(url)["services"]["postgres"]["disk_used_pct"] == 99
