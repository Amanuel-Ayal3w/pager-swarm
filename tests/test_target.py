"""The target serves logs and actions. Fault injection is a separate route."""

from fastapi.testclient import TestClient

from pager.target.app import app, target


def test_inject_rollback_and_revert():
    target.revert()
    client = TestClient(app)
    injected = client.post("/faults/bad_deploy/inject")
    assert injected.status_code == 200
    metrics = client.get("/metrics", params={"service": "api"}).json()
    assert metrics["error_rate"] == 0.42
    logs = client.get("/logs", params={"service": "api", "query": "deploy"}).json()
    assert "after deploy" in logs[0]["message"]
    rolled = client.post("/actions/rollback", json={"service": "api"})
    assert rolled.status_code == 200
    health = client.get("/health", params={"service": "api"}).json()
    assert health["healthy"] is True
    client.post("/faults/revert")
    assert client.get("/metrics", params={"service": "api"}).json()["error_rate"] == 0.01


def test_unknown_fault_is_refused():
    client = TestClient(app)
    assert client.post("/faults/not-a-fault/inject").status_code == 404
