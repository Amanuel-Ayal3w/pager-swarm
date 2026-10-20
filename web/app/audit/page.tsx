"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import { getJSON } from "@/lib/api";
import { ago } from "@/lib/format";
import type { AuditEvent } from "@/lib/types";

export default function AuditPage() {
  const [rows, setRows] = useState<AuditEvent[] | null>(null);
  const [error, setError] = useState(false);
  const [incidentId, setIncidentId] = useState("");
  const [actor, setActor] = useState("");
  const [eventType, setEventType] = useState("");

  function load(next?: { incidentId?: string; actor?: string; eventType?: string }) {
    const params = new URLSearchParams();
    const incident = next?.incidentId ?? incidentId;
    const who = next?.actor ?? actor;
    const kind = next?.eventType ?? eventType;
    if (incident) params.set("incident_id", incident);
    if (who) params.set("actor", who);
    if (kind) params.set("event_type", kind);
    const query = params.toString();
    getJSON<AuditEvent[]>(`/api/audit${query ? `?${query}` : ""}`)
      .then((items) => {
        setRows(items);
        setError(false);
      })
      .catch(() => setError(true));
  }

  useEffect(() => {
    load();
    // initial load only
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <main className="mx-auto max-w-[1120px] px-4 py-8">
      <h1 className="font-display text-[36px] leading-[1.11] font-normal text-balance">Audit log</h1>
      <form
        className="mt-6 flex flex-wrap items-end gap-3"
        onSubmit={(event) => {
          event.preventDefault();
          load();
        }}
      >
        <label className="text-[11px] uppercase text-muted">
          Incident
          <input value={incidentId} onChange={(event) => setIncidentId(event.target.value)} className="mt-1 block h-11 w-40 rounded-[3px] border border-line bg-canvas px-3 font-mono text-[14px] text-ink" />
        </label>
        <label className="text-[11px] uppercase text-muted">
          Actor
          <input value={actor} onChange={(event) => setActor(event.target.value)} className="mt-1 block h-11 w-40 rounded-[3px] border border-line bg-canvas px-3 text-[16px] text-ink" />
        </label>
        <label className="text-[11px] uppercase text-muted">
          Event
          <select value={eventType} onChange={(event) => setEventType(event.target.value)} className="mt-1 block h-11 w-44 rounded-[3px] border border-line bg-canvas px-3 text-[14px] text-ink">
            <option value="">Any</option>
            <option value="approval">Approval</option>
            <option value="finding">Finding</option>
            <option value="action_proposed">Action proposed</option>
            <option value="kill_switch">Kill switch</option>
            <option value="incident_opened">Incident opened</option>
          </select>
        </label>
        <Button variant="primary" type="submit">
          Filter
        </Button>
      </form>
      {error ? <p className="mt-6 text-[16px] text-muted">That didn't work. Try again.</p> : null}
      {rows && rows.length === 0 ? <p className="mt-6 text-[16px] text-muted">Nothing here yet.</p> : null}
      <div className="mt-6 overflow-x-auto">
        <table className="w-full min-w-[720px] text-left text-[14px]">
          <thead className="text-[11px] uppercase text-muted">
            <tr className="border-b border-line">
              <th className="py-2 pr-4 font-normal">When</th>
              <th className="py-2 pr-4 font-normal">Actor</th>
              <th className="py-2 pr-4 font-normal">Event</th>
              <th className="py-2 pr-4 font-normal">Incident</th>
              <th className="py-2 font-normal">Summary</th>
            </tr>
          </thead>
          <tbody>
            {rows?.map((row) => (
              <tr key={row.id} className="border-b border-line">
                <td className="py-3 pr-4 font-mono text-[11px] text-muted">{ago(row.timestamp)}</td>
                <td className="py-3 pr-4">{row.actor}</td>
                <td className="py-3 pr-4 font-mono text-[11px]">{row.event_type}</td>
                <td className="py-3 pr-4 font-mono text-[11px]">
                  {row.incident_id ? <Link href={`/incidents/${row.incident_id}`}>{row.incident_id}</Link> : "—"}
                </td>
                <td className="py-3 text-ink/80">{String(row.payload.summary ?? row.event_type)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
