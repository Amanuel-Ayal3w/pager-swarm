"""The tool layer talks to a target. Tests use an in-memory one. Runs use HTTP."""

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Protocol

from pager.target.world import (
    clear_cache,
    healthy_world,
    restart,
    rollback,
    scale,
    service_healthy,
    update_config,
)


class TargetDown(Exception):
    pass


class Target(Protocol):
    def search_logs(self, service: str, query: str, limit: int) -> list: ...
    def read_logs(self, service: str, limit: int) -> list: ...
    def metrics(self, service: str) -> dict: ...
    def deploys(self, service: str) -> list: ...
    def diff(self, deploy_id: str) -> dict: ...
    def ps(self) -> list: ...
    def health(self, service: str) -> dict: ...
    def service(self, service: str) -> dict: ...
    def restart(self, service: str) -> dict: ...
    def rollback(self, service: str) -> dict: ...
    def scale(self, service: str, replicas: int) -> dict: ...
    def update_config(self, service: str, values: dict) -> dict: ...
    def clear_cache(self, service: str) -> dict: ...
    def inject(self, scenario_id: str) -> None: ...
    def revert(self) -> None: ...


_LOCAL: dict[str, Target] = {}


def register_target(url: str, target: Target) -> None:
    _LOCAL[url] = target


def get_target(url: str) -> Target:
    if url in _LOCAL:
        return _LOCAL[url]
    if url.startswith("http://") or url.startswith("https://"):
        return HttpTarget(url)
    raise KeyError(url)


class MemoryTarget:
    """Same calls as the HTTP service, backed by the world dict."""

    def __init__(self, world: dict | None = None) -> None:
        self.world = world if world is not None else healthy_world()

    def snapshot(self) -> dict:
        return self.world

    def search_logs(self, service: str, query: str, limit: int) -> list:
        needle = query.lower()
        rows = [
            row
            for row in self.world["logs"]
            if row["service"] == service and (not needle or needle in row["message"].lower() or needle in row["level"].lower())
        ]
        return rows[:limit]

    def read_logs(self, service: str, limit: int) -> list:
        return [row for row in self.world["logs"] if row["service"] == service][:limit]

    def metrics(self, service: str) -> dict:
        row = self.world["services"][service]
        return {
            "service": row["name"],
            "error_rate": row["error_rate"],
            "memory_mb": row["memory_mb"],
            "latency_ms": row["latency_ms"],
            "queue_depth": row["queue_depth"],
            "disk_used_pct": row["disk_used_pct"],
            "replicas": row["replicas"],
        }

    def deploys(self, service: str) -> list:
        return [row for row in self.world["deploys"] if row["service"] == service]

    def diff(self, deploy_id: str) -> dict:
        return {"deploy_id": deploy_id, "diff": self.world["diffs"].get(deploy_id, "")}

    def ps(self) -> list:
        return [
            {"service": row["name"], "status": row["status"], "replicas": row["replicas"]}
            for row in self.world["services"].values()
        ]

    def health(self, service: str) -> dict:
        row = self.world["services"][service]
        return {
            "service": row["name"],
            "healthy": service_healthy(row),
            "status": row["status"],
            "error_rate": row["error_rate"],
            "memory_mb": row["memory_mb"],
            "latency_ms": row["latency_ms"],
            "disk_used_pct": row["disk_used_pct"],
        }

    def service(self, service: str) -> dict:
        row = self.world["services"][service]
        return {"service": row["name"], "deploy": row["deploy"], "previous_deploy": row["previous_deploy"]}

    def restart(self, service: str) -> dict:
        self.world = restart(self.world, service)
        return {"ok": True, "service": service, "status": self.world["services"][service]["status"]}

    def rollback(self, service: str) -> dict:
        self.world = rollback(self.world, service)
        return {"ok": True, "service": service, "deploy": self.world["services"][service]["deploy"]}

    def scale(self, service: str, replicas: int) -> dict:
        self.world = scale(self.world, service, replicas)
        return {"ok": True, "service": service, "replicas": replicas}

    def update_config(self, service: str, values: dict) -> dict:
        self.world = update_config(self.world, service, values)
        return {"ok": True, "service": service, "values": values}

    def clear_cache(self, service: str) -> dict:
        self.world = clear_cache(self.world, service)
        return {"ok": True, "service": service, "disk_used_pct": self.world["services"][service]["disk_used_pct"]}

    def inject(self, scenario_id: str) -> None:
        from pager.target.scenarios import broken_world

        self.world = broken_world(scenario_id)

    def revert(self) -> None:
        self.world = healthy_world()


class HttpTarget:
    def __init__(self, base: str) -> None:
        self.base = base.rstrip("/")

    def _call(self, method: str, path: str, query: dict | None = None, body: dict | None = None):
        url = self.base + path
        if query:
            url = f"{url}?{urllib.parse.urlencode(query)}"
        data = None if body is None else json.dumps(body).encode()
        headers = {"Content-Type": "application/json"} if data is not None else {}
        request = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                raw = response.read().decode()
        except urllib.error.URLError as exc:
            raise TargetDown(str(exc)) from exc
        return json.loads(raw) if raw else {}

    def search_logs(self, service: str, query: str, limit: int) -> list:
        return self._call("GET", "/logs", {"service": service, "query": query, "limit": limit})

    def read_logs(self, service: str, limit: int) -> list:
        return self._call("GET", "/logs", {"service": service, "limit": limit})

    def metrics(self, service: str) -> dict:
        return self._call("GET", "/metrics", {"service": service})

    def deploys(self, service: str) -> list:
        return self._call("GET", "/deploys", {"service": service})

    def diff(self, deploy_id: str) -> dict:
        return self._call("GET", "/diff", {"deploy_id": deploy_id})

    def ps(self) -> list:
        return self._call("GET", "/ps")

    def health(self, service: str) -> dict:
        return self._call("GET", "/health", {"service": service})

    def service(self, service: str) -> dict:
        return self._call("GET", "/service", {"service": service})

    def restart(self, service: str) -> dict:
        return self._call("POST", "/actions/restart", body={"service": service})

    def rollback(self, service: str) -> dict:
        return self._call("POST", "/actions/rollback", body={"service": service})

    def scale(self, service: str, replicas: int) -> dict:
        return self._call("POST", "/actions/scale", body={"service": service, "replicas": replicas})

    def update_config(self, service: str, values: dict) -> dict:
        return self._call("POST", "/actions/config", body={"service": service, "values": values})

    def clear_cache(self, service: str) -> dict:
        return self._call("POST", "/actions/cache", body={"service": service})

    def inject(self, scenario_id: str) -> None:
        self._call("POST", f"/faults/{scenario_id}/inject")

    def revert(self) -> None:
        self._call("POST", "/faults/revert")
