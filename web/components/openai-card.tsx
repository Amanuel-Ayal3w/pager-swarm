"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { useLive } from "@/components/live";
import { AgentWork } from "@/components/agent-work";
import { Button } from "@/components/ui/button";
import { Panel } from "@/components/ui/panel";
import { ApiError, getJSON, postJSON } from "@/lib/api";
import { money, stateLabel } from "@/lib/format";
import { readDemo, readDemoKey } from "@/lib/session";
import type { IncidentDetail, Task, TraceStep } from "@/lib/types";

const DEMO_SCENARIOS = ["bad_deploy", "memory_leak", "slow_query"] as const;

type RunResult = {
  paused: boolean;
  incident: IncidentDetail;
};

export function OpenAICard() {
  const { events } = useLive();
  const [since, setSince] = useState<number | null>(null);
  const [incidentId, setIncidentId] = useState<string | null>(null);
  const [detail, setDetail] = useState<IncidentDetail | null>(null);
  const [steps, setSteps] = useState<TraceStep[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [pending, setPending] = useState(false);
  const [stopping, setStopping] = useState(false);
  const [error, setError] = useState("");
  const [demo, setDemo] = useState(false);
  const [hasKey, setHasKey] = useState(false);

  useEffect(() => {
    function sync() {
      const current = readDemo();
      setDemo(current.on);
      setHasKey(current.hasKey);
    }
    sync();
    window.addEventListener("pager-demo", sync);
    return () => window.removeEventListener("pager-demo", sync);
  }, []);

  useEffect(() => {
    if (incidentId || since === null) return;
    const found = events.find((event) => event.id > since && event.incident_id);
    if (found?.incident_id) setIncidentId(found.incident_id);
  }, [events, incidentId, since]);

  useEffect(() => {
    if (!incidentId) return;
    let cancelled = false;
    async function pull() {
      try {
        const [incident, trace, running] = await Promise.all([
          getJSON<IncidentDetail>(`/api/incidents/${incidentId}`),
          getJSON<TraceStep[]>(`/api/incidents/${incidentId}/trace`),
          getJSON<Task[]>("/api/agents"),
        ]);
        if (cancelled) return;
        setDetail(incident);
        setSteps(trace);
        setTasks(running.filter((task) => task.incident_id === incidentId));
      } catch {
        if (!cancelled) return;
      }
    }
    void pull();
    if (!pending) {
      return () => {
        cancelled = true;
      };
    }
    const timer = window.setInterval(pull, 1000);
    return () => {
      cancelled = true;
      window.clearInterval(timer);
    };
  }, [incidentId, pending]);

  async function stop() {
    setStopping(true);
    setError("");
    try {
      await postJSON("/api/runs/stop", { incident_id: incidentId });
    } catch (err) {
      const api = err instanceof ApiError ? err : null;
      setError(api?.message || "That didn't work. Try again.");
    } finally {
      setStopping(false);
    }
  }

  async function simulate() {
    setError("");
    setDetail(null);
    setSteps([]);
    setIncidentId(null);
    setSince(events.at(-1)?.id ?? 0);
    setPending(true);
    const demoOn = readDemo().on;
    const apiKey = demoOn ? readDemoKey() : "";
    if (demoOn && !apiKey) {
      setError("Add your key in Settings, then press Simulate.");
      setPending(false);
      return;
    }
    const turn = Number(sessionStorage.getItem("pager-demo-turn") || "0");
    const scenario = demoOn ? DEMO_SCENARIOS[turn % DEMO_SCENARIOS.length] : "bad_deploy";
    try {
      const result = await postJSON<RunResult>("/api/runs", {
        scenario,
        model: "openai",
        ...(apiKey ? { api_key: apiKey } : {}),
      });
      if (demoOn) sessionStorage.setItem("pager-demo-turn", String(turn + 1));
      setIncidentId(result.incident.id);
      setDetail(result.incident);
    } catch (err) {
      const api = err instanceof ApiError ? err : null;
      setError(api?.message || "That didn't work. Try again.");
    } finally {
      setPending(false);
    }
  }

  const tokens = steps.reduce((sum, step) => sum + step.tokens_in + step.tokens_out, 0);
  const cost = steps.reduce((sum, step) => sum + step.cost, 0);
  const latest = steps.at(-1);

  return (
    <Panel className="p-4">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h2 className="text-[14px] font-medium">
            {demo ? "Demo" : "Cost"}
            {pending ? <i className="caret" aria-hidden="true" /> : null}
          </h2>
          <p className="mt-1 text-[13px] text-muted">
            {demo
              ? "Press Simulate. It opens a real incident with your key and pauses for approval."
              : "Press Simulate. One real incident runs on the server key so you can see the spend."}
          </p>
        </div>
        {pending ? (
          <Button variant="line" disabled={stopping} onClick={() => void stop()}>
            {stopping ? "Stopping" : "Stop"}
          </Button>
        ) : (
          <Button variant="accent" disabled={demo && !hasKey} onClick={() => void simulate()}>
            Simulate
          </Button>
        )}
      </div>
      {demo && !hasKey ? <p className="mt-4 text-[14px] text-muted">Add your key in Settings before you press Simulate.</p> : null}
      {error ? <p className="mt-4 text-[14px] text-ink">{error}</p> : null}
      {detail ? (
        <p className="mt-4 font-mono text-[11px] text-muted">
          <Link href={`/incidents/${detail.id}`} className="text-ink hover:text-ink/80">
            {detail.id}
          </Link>
          {" · "}
          {stateLabel(detail.state)}
          {" · "}
          {tokens} tokens · {money(cost)}
        </p>
      ) : null}
      {pending ? <div className="mt-4"><AgentWork tasks={tasks} liveOnly /></div> : null}
      {pending && !latest && tasks.length === 0 ? <p className="mt-4 text-[14px] text-muted">Waiting for the model.</p> : null}
      {latest ? (
        <div className="mt-4 border-t border-line pt-3">
          <p className="text-[14px] capitalize text-ink">
            {latest.agent_role} · step {latest.step_no}
          </p>
          <p className="mt-2 text-[16px] text-ink/90">{latest.response || "Calling the model."}</p>
          <p className="mt-2 font-mono text-[11px] text-muted">
            {latest.tool_calls.map((call) => call.name || call.tool).filter(Boolean).join(", ") || "no tool"} · {latest.tokens_in + latest.tokens_out} tokens · {money(latest.cost)}
          </p>
        </div>
      ) : null}
    </Panel>
  );
}
