"""Incident phrases the seed and the simulator draw from."""

SERVICES = ["api", "worker", "postgres", "redis", "payments"]

TITLES = [
    ("Error rate jumped after deploy", "sev1", ["api"]),
    ("Worker memory keeps climbing", "sev2", ["worker"]),
    ("Checkout queries are slow", "sev2", ["api", "postgres"]),
    ("Disk filled on the database host", "sev1", ["postgres"]),
    ("Payments dependency timing out", "sev1", ["api", "payments"]),
    ("Certificate expires tonight", "sev3", ["api"]),
    ("Cache hit rate collapsed", "sev3", ["redis"]),
    ("Queue depth stuck above 10k", "sev2", ["worker"]),
    ("Latency above the page budget", "sev4", ["api"]),
    ("Spike was a health-check loop", "sev4", ["api"]),
]

FINDINGS = [
    ("inv-logs", "logs", "The error log shows the same exception on every request."),
    ("inv-metrics", "metrics", "The chart moved in the same minute as the deploy."),
    ("inv-deploys", "git", "The diff changes a timeout that the service depends on."),
    ("inv-infra", "infra", "The host is close to a limit the service cannot cross."),
]

HYPOTHESES = [
    "A recent deploy changed the path that is failing.",
    "One dependency is slow and the caller does not back off.",
    "A resource limit filled and new work cannot start.",
    "The signal is from a health check, not from customers.",
]

TRACE_LINES = [
    ("triager", "triager", "Opened the incident from the page.", "query_metrics"),
    ("investigator", "inv-logs", "Read the matching log lines.", "search_logs"),
    ("investigator", "inv-metrics", "Compared the metric window to the deploy.", "query_metrics"),
    ("diagnostician", "diagnostician", "Ranked the hypotheses.", "search_logs"),
    ("planner", "planner", "Wrote the proposed action and its rollback.", "list_recent_deploys"),
]

EXCERPTS = {
    "logs": ["error rate 18% on POST /checkout", "alloc resize buf 12MB", "lock wait orders 840ms"],
    "metrics": ["api_error_rate 0.18", "worker rss 1.4GB", "cache_hit_ratio 0.11"],
    "git": ["pool: false  # was true", "timeout_ms: 50  # was 2000", "replicas: 1"],
    "infra": ["disk 98% on /var", "notAfter 02:00Z", "queue depth 10442"],
}
