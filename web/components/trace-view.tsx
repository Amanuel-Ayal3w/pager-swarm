"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { getJSON } from "@/lib/api";
import { ago, money } from "@/lib/format";
import type { Approval, IncidentDetail, TraceStep } from "@/lib/types";

type Row =
  | { kind: "step"; at: string; step: TraceStep }
  | { kind: "approval"; at: string; approval: Approval };

export function TraceView({ id }: { id: string }) {
  const [rows, setRows] = useState<Row[] | null>(null);
  const [title, setTitle] = useState("");
  const [error, setError] = useState(false);

  useEffect(() => {
    let cancelled = false;
    Promise.all([getJSON<IncidentDetail>(`/api/incidents/${id}`), getJSON<TraceStep[]>(`/api/incidents/${id}/trace`)])
      .then(([incident, steps]) => {
        if (cancelled) return;
        setTitle(incident.title);
        const merged: Row[] = [
          ...steps.map((step) => ({ kind: "step" as const, at: step.created_at, step })),
          ...incident.approvals.map((approval) => ({ kind: "approval" as const, at: approval.timestamp, approval })),
        ];
        merged.sort((a, b) => new Date(a.at).getTime() - new Date(b.at).getTime());
        setRows(merged);
      })
      .catch(() => {
        if (!cancelled) setError(true);
      });
    return () => {
      cancelled = true;
    };
  }, [id]);

  return (
    <main className="mx-auto max-w-[1120px] px-4 py-8">
      <Link href={`/incidents/${id}`} className="text-[14px] text-muted hover:text-ink">
        Incident
      </Link>
      <p className="mt-4 font-mono text-[11px] text-muted">{id}</p>
      <h1 className="mt-3 font-display text-[36px] leading-[1.11] font-normal text-balance">{title || "Trace"}</h1>
      {error ? <p className="mt-6 text-[16px] text-muted">That didn't work. Try again.</p> : null}
      {rows && rows.length === 0 ? <p className="mt-6 text-[16px] text-muted">Nothing here yet.</p> : null}
      <ol className="relative mt-8 max-w-[640px] space-y-4 pl-6">
        <svg className="absolute top-2 bottom-2 left-[7px] h-[calc(100%-1rem)] w-px" viewBox="0 0 1 1" preserveAspectRatio="none" aria-hidden="true">
          <path d="M0.5 0 V1" pathLength={1} className="route-draw text-line" stroke="currentColor" strokeWidth="1" vectorEffect="non-scaling-stroke" fill="none" />
        </svg>
        {rows?.map((row, index) => (
          <li key={row.kind === "step" ? row.step.id : row.approval.id} className="rounded-[3px] border border-line bg-surface p-4" style={{ animationDelay: `${index * 70}ms` }}>
            {row.kind === "step" ? (
              <>
                <div className="flex items-baseline justify-between gap-3">
                  <p className="text-[14px] capitalize text-ink">
                    {row.step.agent_role} · step {row.step.step_no}
                  </p>
                  <p className="font-mono text-[11px] text-muted">{ago(row.step.created_at)}</p>
                </div>
                <p className="mt-2 text-[16px]">{row.step.response}</p>
                <p className="mt-2 font-mono text-[11px] text-muted">
                  {row.step.tool_calls.map((call) => call.name || call.tool).filter(Boolean).join(", ") || "no tool"} · {row.step.tokens_in + row.step.tokens_out} tokens · {money(row.step.cost)} · {row.step.latency_ms} ms
                </p>
              </>
            ) : (
              <>
                <div className="flex items-baseline justify-between gap-3">
                  <p className="text-[14px] text-accent">Approval · {row.approval.decision}</p>
                  <p className="font-mono text-[11px] text-muted">{ago(row.approval.timestamp)}</p>
                </div>
                <p className="mt-2 text-[16px]">
                  {row.approval.operator}
                  {row.approval.reason ? `. ${row.approval.reason}` : ""}
                </p>
              </>
            )}
          </li>
        ))}
      </ol>
    </main>
  );
}
