"""Read and action handlers. They call the target. They never inject a fault."""

from pager.safety.untrusted import wrap
from pager.target.client import Target


def read_logs(args, target: Target) -> dict:
    return wrap("logs", target.read_logs(args.service, args.limit))


def search_logs(args, target: Target) -> dict:
    return wrap("logs", target.search_logs(args.service, args.query, args.limit))


def query_metrics(args, target: Target) -> dict:
    return wrap("metrics", target.metrics(args.service))


def list_recent_deploys(args, target: Target) -> dict:
    return wrap("git", target.deploys(args.service))


def get_git_diff(args, target: Target) -> dict:
    return wrap("git", target.diff(args.deploy_id))


def docker_ps(_args, target: Target) -> dict:
    return wrap("infra", target.ps())


def service_health(args, target: Target) -> dict:
    return wrap("infra", target.health(args.service))


def preview_restart(args, _target: Target) -> dict:
    return {"dry_run": True, "tool": "restart_service", "service": args.service, "would": "restart the process"}


def preview_rollback(args, target: Target) -> dict:
    described = target.service(args.service)
    return {
        "dry_run": True,
        "tool": "rollback_deploy",
        "service": args.service,
        "would": f"roll {described['deploy']} back to {described['previous_deploy']}",
    }


def preview_scale(args, _target: Target) -> dict:
    return {"dry_run": True, "tool": "scale_service", "service": args.service, "would": f"set replicas to {args.replicas}"}


def preview_config(args, _target: Target) -> dict:
    return {"dry_run": True, "tool": "update_config", "service": args.service, "would": f"set {sorted(args.values)}"}


def preview_cache(args, _target: Target) -> dict:
    return {"dry_run": True, "tool": "clear_cache", "service": args.service, "would": "clear cached files on the host"}


def run_restart(args, target: Target) -> dict:
    return target.restart(args.service)


def run_rollback(args, target: Target) -> dict:
    return target.rollback(args.service)


def run_scale(args, target: Target) -> dict:
    return target.scale(args.service, args.replicas)


def run_config(args, target: Target) -> dict:
    return target.update_config(args.service, args.values)


def run_cache(args, target: Target) -> dict:
    return target.clear_cache(args.service)
