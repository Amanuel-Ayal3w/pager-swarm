"""Decide whether a tool call may run, dry-run, or stop."""

from pager.safety.allowlist import ACTION_TOOLS, FORBIDDEN_TOOLS, MAX_ACTIONS_PER_HOUR, READ_TOOLS, Denied

T0 = "T0"
T1 = "T1"
T2 = "T2"
T3 = "T3"

READ_ROLES = frozenset({"triager", "investigator", "diagnostician", "planner"})
ACTION_ROLES = frozenset({"executor"})


def tier_of(name: str) -> str:
    if name in READ_TOOLS:
        return T0
    if name in {"restart_service", "scale_service", "clear_cache"}:
        return T1
    if name in {"rollback_deploy", "update_config"}:
        return T2
    return T3


def roles_for(name: str) -> frozenset[str]:
    if name in READ_TOOLS:
        return READ_ROLES
    if name in ACTION_TOOLS:
        return ACTION_ROLES
    return frozenset()


def confirmation_phrase(name: str, args: dict) -> str | None:
    if tier_of(name) != T2:
        return None
    verb = "rollback" if name == "rollback_deploy" else "update"
    service = str(args.get("service") or "").strip()
    return f"{verb} {service}".strip()


def authorize(
    name: str,
    *,
    role: str,
    approved: bool,
    dry_run: bool,
    kill_active: bool,
    recent_actions: int,
) -> str:
    """Return 'run' or 'dry_run'. Raise Denied when the call must not proceed."""
    if kill_active:
        raise Denied("kill_switch", "Kill switch is on. Actions are blocked.")
    tier = tier_of(name)
    if name in FORBIDDEN_TOOLS or tier == T3 or name not in READ_TOOLS | ACTION_TOOLS:
        raise Denied("forbidden", "This action is forbidden.")
    if role not in roles_for(name):
        if dry_run and role == "planner" and tier in {T1, T2}:
            return "dry_run"
        raise Denied("not_permitted", f"{role} cannot call {name}.")
    if tier == T0:
        return "run"
    if approved and not dry_run:
        if recent_actions >= MAX_ACTIONS_PER_HOUR:
            raise Denied("rate_limit", "The action rate limit was reached.")
        return "run"
    if dry_run:
        return "dry_run"
    raise Denied("unapproved", "This action needs approval before it can run.")


def approval_holds(
    *,
    status: str,
    version: int,
    approved_version: int,
    tier: str,
    kill: bool,
    decision: str,
    typed: str | None,
    phrase: str | None,
) -> bool:
    """True when a stored approval is still valid for this exact action."""
    if kill or decision != "approve" or status != "approved":
        return False
    if version != approved_version or tier not in {T1, T2}:
        return False
    if tier == T2:
        return bool(phrase) and (typed or "") == phrase
    return True
