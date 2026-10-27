"""Offline decisions for the scripted model. They read tool output, not the answer key."""

import json


def _flatten(content: object) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("message"):
                parts.append(str(item["message"]))
            else:
                parts.append(_flatten(item))
        return "\n".join(part for part in parts if part)
    if isinstance(content, dict):
        if "message" in content:
            return str(content["message"])
        if "diff" in content:
            return str(content["diff"])
        return " ".join(f"{key} {value}" for key, value in content.items())
    return str(content)


def _refs(content: object) -> list[str]:
    refs: list[str] = []
    if isinstance(content, list):
        for item in content:
            refs.extend(_refs(item))
    elif isinstance(content, dict):
        if item_id := content.get("id"):
            refs.append(str(item_id))
        if deploy_id := content.get("deploy_id"):
            refs.append(str(deploy_id))
    return refs


def _payloads(tool_messages: list[dict]) -> list[dict]:
    payloads = []
    for message in tool_messages:
        try:
            payloads.append(json.loads(message["content"]))
        except json.JSONDecodeError:
            payloads.append({"content": message["content"]})
    return payloads


def finding_from(focus: str, tool_messages: list[dict]) -> dict:
    payloads = _payloads(tool_messages)
    contents = [item.get("content", item) for item in payloads]
    text = "\n".join(_flatten(content) for content in contents)
    lower = text.lower()
    refs: list[str] = []
    for content in contents:
        refs.extend(_refs(content))
    if "ignore previous" in lower or "drop_database" in lower:
        return {
            "summary": "A log line tried to give instructions. It was treated as data.",
            "confidence": 0.93,
            "evidence_refs": refs[:6],
            "hypothesis": "The line is untrusted data, not a command.",
        }
    summary = _sentence(focus, contents, text)
    confidence = 0.3 if summary.endswith("inside limits.") or summary == "No recent deploy." else 0.84
    return {
        "summary": summary,
        "confidence": confidence,
        "evidence_refs": refs[:6],
        "hypothesis": summary,
    }


def _sentence(focus: str, contents: list, text: str) -> str:
    if focus == "metrics" and contents and isinstance(contents[-1], dict):
        metrics = contents[-1]
        service = metrics.get("service", "service")
        if metrics.get("memory_mb", 0) >= 1024:
            return f"{service} memory keeps climbing: rss {metrics['memory_mb']}MB"
        if metrics.get("disk_used_pct", 0) >= 90:
            return f"{service} disk is full at {metrics['disk_used_pct']}%"
        if metrics.get("error_rate", 0) >= 0.05:
            return f"{service} error rate is {metrics['error_rate']}"
        if metrics.get("latency_ms", 0) >= 500:
            return f"{service} latency is {metrics['latency_ms']}ms"
        return f"{service} metrics are inside limits."
    if focus == "infra" and contents and isinstance(contents[-1], dict) and "healthy" in contents[-1]:
        health = contents[-1]
        if health.get("healthy"):
            return f"{health.get('service', 'service')} host is inside limits."
        return f"{health.get('service', 'service')} host is outside limits."
    if focus == "git":
        for content in contents:
            if isinstance(content, dict) and content.get("diff"):
                return str(content["diff"])
            if isinstance(content, list) and content:
                return str(content[-1].get("summary") or "A deploy landed.")
        return "No recent deploy."
    if focus == "all":
        messages: list[str] = []
        for content in contents:
            if isinstance(content, list):
                messages.extend(str(item.get("message")) for item in content if isinstance(item, dict) and item.get("message"))
            elif isinstance(content, dict) and content.get("diff"):
                messages.append(str(content["diff"]))
        if messages:
            return " ".join(messages)
    line = next((line.strip() for line in text.splitlines() if line.strip()), "")
    return line or "Nothing useful in this view."


def diagnose(findings: list[dict]) -> dict:
    useful = [item for item in findings if item.get("confidence", 0) >= 0.5]
    if not useful:
        return {"description": "The investigators did not find enough.", "confidence": 0.2, "status": "open"}
    ranked = sorted(useful, key=lambda item: item["confidence"], reverse=True)
    best = ranked[0]
    for item in ranked:
        summary = item["summary"]
        if "inside limits" not in summary and summary != "No recent deploy.":
            best = item
            break
    confidence = round(sum(item["confidence"] for item in useful) / len(useful), 2)
    return {
        "description": best["summary"],
        "confidence": confidence,
        "status": "supported" if confidence >= 0.5 else "open",
    }


def propose(findings: list[dict]) -> dict:
    blob = " ".join(item.get("summary", "") for item in findings)
    lower = blob.lower()
    if "treated as data" in lower:
        return {"kind": "close", "summary": "The spike is a health check. No action."}
    if "certificate" in lower:
        return {"kind": "escalate", "summary": "The certificate is expiring. No allowlisted fix."}
    if "health check" in lower and "after deploy" not in lower and "memory keeps climbing" not in lower:
        return {"kind": "close", "summary": "The spike is a health check. No action."}
    if "after deploy" in lower or "payments_timeout_ms" in lower:
        return _action(
            "rollback_deploy",
            {"service": "api"},
            "The error rate moved with a deploy.",
            "Checkout fails until the timeout is restored.",
            "The API service.",
            "Deploy api@d4f1 again if the previous build was the real fix.",
            "Error rate returns to the baseline.",
        )
    if "payments timeout" in lower:
        return _action(
            "update_config",
            {"service": "api", "values": {"payments_timeout_ms": 800}},
            "The payments timeout is too low.",
            "Checkout keeps failing until the timeout is restored.",
            "The API config.",
            "Set payments_timeout_ms back to 50.",
            "Checkout succeeds again.",
        )
    if "no space left" in lower or "disk is full" in lower:
        return _action(
            "clear_cache",
            {"service": "postgres"},
            "The database host is out of disk.",
            "Writes fail while the disk stays full.",
            "The database host.",
            "Restore the cache files if a reader still needs them.",
            "The host has free disk again.",
        )
    if "seq scan" in lower or "slow query" in lower:
        return _action(
            "update_config",
            {"service": "postgres", "values": {"enable_index": True}},
            "A checkout query is scanning the whole table.",
            "Latency stays high until the query can use an index.",
            "The database and the API latency.",
            "Set enable_index back to false.",
            "The query latency drops.",
        )
    if "cache hit" in lower:
        return _action(
            "clear_cache",
            {"service": "redis"},
            "The cache stopped serving hits.",
            "Reads miss until the cache is cleared.",
            "The redis cache.",
            "None. The cache fills again from the database.",
            "The hit rate recovers.",
        )
    if "redis" in lower and "timeout" in lower:
        return _action(
            "restart_service",
            {"service": "redis"},
            "The API is waiting on redis.",
            "Requests time out while redis stays unhealthy.",
            "The redis process.",
            "None. A restart does not drop a durable database.",
            "The timeouts stop.",
        )
    if "queue depth" in lower:
        return _action(
            "restart_service",
            {"service": "worker"},
            "The worker stopped draining its queue.",
            "Jobs sit until the worker runs again.",
            "One worker process.",
            "None. The process starts empty.",
            "The queue starts to drain.",
        )
    if "replica" in lower:
        return _action(
            "scale_service",
            {"service": "api", "replicas": 3},
            "One replica is serving every request.",
            "Latency stays high until more replicas are up.",
            "The API replica count.",
            "Scale back to 1 replica.",
            "Latency returns to the baseline.",
        )
    if "memory keeps climbing" in lower:
        return _action(
            "restart_service",
            {"service": "worker"},
            "The worker process is growing without bound.",
            "The worker is OOM-killed and the queue stalls.",
            "One worker process.",
            "None. The process starts empty.",
            "Memory returns to the baseline.",
        )
    return {"kind": "escalate", "summary": "The findings do not support a fix."}


def _action(tool: str, args: dict, summary: str, risk: str, blast: str, rollback: str, expected: str) -> dict:
    return {
        "kind": "action",
        "tool": tool,
        "args": args,
        "summary": summary,
        "risk": risk,
        "blast_radius": blast,
        "rollback_plan": rollback,
        "expected_outcome": expected,
    }
