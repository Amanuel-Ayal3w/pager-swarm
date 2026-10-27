"""Services and tools an agent is allowed to touch."""

SERVICES = frozenset({"api", "worker", "postgres", "redis", "payments"})

READ_TOOLS = frozenset(
    {
        "read_logs",
        "search_logs",
        "query_metrics",
        "list_recent_deploys",
        "get_git_diff",
        "docker_ps",
        "service_health",
    }
)

ACTION_TOOLS = frozenset(
    {
        "restart_service",
        "rollback_deploy",
        "scale_service",
        "update_config",
        "clear_cache",
    }
)

# Registered so a call is refused in code. The handler never runs.
FORBIDDEN_TOOLS = frozenset({"drop_database", "delete_volume"})

CONFIG_KEYS = frozenset({"enable_index", "payments_timeout_ms"})

MAX_ACTIONS_PER_HOUR = 5
MAX_REPLICAS = 5


class Denied(Exception):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(message)


def check_service(service: str) -> None:
    if service not in SERVICES:
        raise Denied("not_allowlisted", f"{service} is outside the service allowlist.")
