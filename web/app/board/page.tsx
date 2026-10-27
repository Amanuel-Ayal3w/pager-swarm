"use client";

import Link from "next/link";
import { Activity } from "lucide-react";
import { useEffect, useState } from "react";

import { useLive } from "@/components/live";
import { OpenAICard } from "@/components/openai-card";
import { AgentWork } from "@/components/agent-work";
import { Typed } from "@/components/typed";
import { Badge } from "@/components/ui/badge";
import { Panel } from "@/components/ui/panel";
import { getJSON, postJSON } from "@/lib/api";
import { agentText, ago, money, severityLabel, severityTone, stateLabel, stateTone } from "@/lib/format";
import type { Incident, Task } from "@/lib/types";

export default function HomePage() {
  const { events, pulse } = useLive();
  const [incidents, setIncidents] = useState<Incident[] | null>(null);
  const [agents, setAgents] = useState<Task[]>([]);
  const [error, setError] = useState(false);

  useEffect(() => {
    let cancelled = false;
    async function pull() {
      try {
        const [rows, running] = await Promise.all([getJSON<Incident[]>("/api/incidents"), getJSON<Task[]>("/api/agents")]);
        if (cancelled) return;
        setIncidents(rows);
        setAgents(running);
        setError(false);
      } catch {
        if (!cancelled) setError(true);
      }
    }
    void pull();
    const timer = window.setInterval(pull, 1000);
    return () => {
      cancelled = true;
      window.clearInterval(timer);
    };
  }, [pulse]);

  const open = incidents?.filter((item) => item.state !== "RESOLVED" && item.state !== "CLOSED_NO_ACTION").length;
  const waiting = incidents?.filter((item) => item.state === "AWAITING_APPROVAL").length;
  const escalated = incidents?.filter((item) => item.state === "ESCALATED").length;

  return (
    <main className="px-4 py-6 sm:px-6">
      <h1 className="font-display text-[30px] leading-[1.13] font-normal">Board</h1>
      <p className="mt-2 text-[14px] text-muted">Open incidents, agents, and the live feed.</p>
      <div className="mt-6 grid grid-cols-2 gap-3 xl:grid-cols-4">
        <Stat label="Open" value={open} />
        <Stat label="Awaiting approval" value={waiting} />
        <Stat label="Escalated" value={escalated} />
        <Stat label="Agents" value={incidents ? agents.length : undefined} />
      </div>
      <div className="mt-6 grid gap-6 xl:grid-cols-[minmax(0,1fr)_320px]">
      <section>
        {error ? <p className="mt-6 text-[16px] text-muted">That didn't work. Try again.</p> : null}
        {incidents && incidents.length === 0 ? <p className="mt-6 text-[16px] text-muted">Nothing here yet.</p> : null}
        <ul className="divide-y divide-line border-y border-line">
          {incidents?.map((incident) => {
            const working = agents.filter((agent) => agent.incident_id === incident.id);
            const active = incident.state === "INVESTIGATING" || incident.state === "REMEDIATING" || incident.state === "AWAITING_APPROVAL";
            return (
            <li key={incident.id}>
              <Link href={`/incidents/${incident.id}`} className="grid gap-2 py-4 transition-colors duration-150 hover:bg-ink/[0.04] sm:grid-cols-[112px_minmax(0,1fr)_auto] sm:items-start sm:gap-4">
                <span className="flex items-center gap-2 font-mono text-[11px] text-muted">
                  {working.length > 0 ? <i className="live-dot" aria-hidden="true" /> : <i className={`inline-block h-1.5 w-1.5 rounded-full ${active ? "bg-accent" : "bg-line"}`} aria-hidden="true" />}
                  {incident.id}
                </span>
                <span className="min-w-0">
                  <span className="block text-[16px] text-ink">{incident.title}</span>
                  <span className="mt-1 block text-[14px] text-muted">{incident.summary}</span>
                  {incident.latest_work && agentText(incident.latest_work) !== incident.summary ? (
                    <span className="mt-1 block line-clamp-3 text-[14px] text-ink/80">{agentText(incident.latest_work)}</span>
                  ) : null}
                  <span className="mt-1 block text-[13px] text-muted">{incident.affected_services.join(" · ")}</span>
                  {working.length > 0 ? (
                    <div className="mt-3">
                      <AgentWork tasks={working} liveOnly />
                    </div>
                  ) : null}
                </span>
                <span className="flex flex-wrap items-center gap-2 sm:justify-end">
                  <Badge tone={severityTone(incident.severity)}>{severityLabel(incident.severity)}</Badge>
                  <Badge tone={stateTone(incident.state)}>{stateLabel(incident.state)}</Badge>
                  <span className="font-mono text-[11px] text-muted">{ago(incident.opened_at)}</span>
                  <span className="font-mono text-[11px] text-muted">{money(incident.cost_usd)}</span>
                </span>
              </Link>
            </li>
            );
          })}
        </ul>
      </section>
      <aside className="space-y-4">
        <OpenAICard />
        <Panel className="p-4">
          <div className="flex items-center justify-between gap-3">
            <h2 className="flex items-center gap-2 text-[14px] font-medium">
              <Activity size={14} strokeWidth={1.5} />
              Agents
            </h2>
            {agents.length > 0 ? (
              <button type="button" onClick={() => void postJSON("/api/runs/stop", {})} className="text-[13px] text-muted hover:text-ink">
                Stop
              </button>
            ) : null}
          </div>
          {agents.length === 0 ? <p className="mt-3 text-[14px] text-muted">No agents running.</p> : <div className="mt-3"><AgentWork tasks={agents} liveOnly showIncident /></div>}
        </Panel>
        <Panel className="p-4">
          <h2 className="flex items-center gap-2 text-[14px] font-medium">
            Activity
            <i className="caret" aria-hidden="true" />
          </h2>
          {events.length === 0 ? <p className="mt-3 text-[14px] text-muted">Nothing here yet.</p> : null}
          <ol className="mt-3 max-h-[420px] space-y-2 overflow-auto font-mono text-[11px] leading-relaxed">
            {events.map((event, index) => (
              <li key={event.id} className="text-ink/80">
                <span className="text-muted">{event.actor}</span>{" "}
                <Typed text={event.summary} active={index === events.length - 1} />
              </li>
            ))}
          </ol>
        </Panel>
      </aside>
      </div>
    </main>
  );
}

function Stat({ label, value }: { label: string; value: number | undefined }) {
  return (
    <Panel className="p-4">
      <p className="text-[13px] text-muted">{label}</p>
      <p className="mt-2 font-display text-[30px] leading-none">{value === undefined ? "—" : value}</p>
    </Panel>
  );
}
