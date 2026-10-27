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

SUMMARIES = {
    "Error rate jumped after deploy": "Checkout error rate hit 42% in the minute after the api deploy. Payments calls are timing out.",
    "Worker memory keeps climbing": "Worker RSS climbs until the process is restarted. The checkout queue backs up while it is down.",
    "Checkout queries are slow": "orders_by_user is scanning the table. Checkout p95 is past the page budget.",
    "Disk filled on the database host": "The database disk is at 98%. Writes are failing and the api is returning 500s.",
    "Payments dependency timing out": "The payments client is timing out. Checkout fails closed while the dependency is slow.",
    "Certificate expires tonight": "The api certificate expires at 02:00Z. Clients will fail the handshake after that.",
    "Cache hit rate collapsed": "Redis hit rate fell to 11%. The api is reading through to postgres on every request.",
    "Queue depth stuck above 10k": "The worker queue is holding above 10,000 jobs and is not draining.",
    "Latency above the page budget": "The api p95 is above the page budget. The slow path is the checkout read.",
    "Spike was a health-check loop": "The error spike is the health checker retrying. Customer traffic is steady.",
}

CAUSES = {
    "Error rate jumped after deploy": "Deploy api@d4f1 lowered the payments timeout.",
    "Worker memory keeps climbing": "The worker process leaks memory on the checkout consumer.",
    "Checkout queries are slow": "orders_by_user does a sequential scan.",
    "Disk filled on the database host": "The database disk filled and writes started failing.",
    "Payments dependency timing out": "The payments dependency is past its timeout and the caller does not back off.",
    "Certificate expires tonight": "The api certificate expires tonight.",
    "Cache hit rate collapsed": "The cache stopped serving and every read falls through.",
    "Queue depth stuck above 10k": "The worker is not draining the queue.",
    "Latency above the page budget": "The checkout read is slower than the page budget.",
    "Spike was a health-check loop": "The spike is a health-check loop, not customer traffic.",
}

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
