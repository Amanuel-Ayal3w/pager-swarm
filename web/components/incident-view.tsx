"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { useLive } from "@/components/live";
import { useSession } from "@/components/shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Panel } from "@/components/ui/panel";
import { ApiError, getJSON, postJSON } from "@/lib/api";
import { severityLabel, severityTone, stateLabel, stateTone } from "@/lib/format";
import type { Action, IncidentDetail } from "@/lib/types";

export function IncidentView({ id }: { id: string }) {
  const { kill, pulse } = useLive();
  const { operator } = useSession();
  const [incident, setIncident] = useState<IncidentDetail | null>(null);
  const [missing, setMissing] = useState(false);
  const [error, setError] = useState("");
  const [reason, setReason] = useState("");
  const [phrase, setPhrase] = useState("");
  const [shake, setShake] = useState(false);
  const [pending, setPending] = useState(false);
  useEffect(() => {
    let cancelled = false;
    getJSON<IncidentDetail>(`/api/incidents/${id}`)
      .then((row) => {
        if (cancelled) return;
        setIncident(row);
        setMissing(false);
      })
      .catch((err: unknown) => {
        if (cancelled) return;
        if (err instanceof ApiError && err.status === 404) setMissing(true);
        else setError("That didn't work. Try again.");
      });
    return () => {
      cancelled = true;
    };
  }, [id, pulse]);

  if (missing) {
    return (
      <main className="mx-auto max-w-[544px] px-4 py-8">
        <p className="text-[16px] text-muted">Nothing here yet.</p>
      </main>
    );
  }
  if (!incident) {
    return (
      <main className="mx-auto max-w-[544px] px-4 py-8">
        <p className="text-[16px] text-muted">{error || "Loading."}</p>
      </main>
    );
  }

  const proposed = incident.actions.find((action) => action.status === "proposed") ?? incident.actions[0] ?? null;
  const waiting = incident.state === "AWAITING_APPROVAL" && proposed?.status === "proposed";

  async function decide(decision: "approve" | "reject" | "investigate") {
    if (!proposed || pending) return;
    setError("");
    setPending(true);
    try {
      const next = await postJSON<IncidentDetail>(`/api/actions/${proposed.id}/decision`, {
        decision,
        operator,
        reason: reason || null,
        typed_confirmation: phrase || null,
        action_version: proposed.version,
      });
      setIncident(next);
      setPhrase("");
      setReason("");
    } catch (err) {
      const api = err instanceof ApiError ? err : null;
      setError(api?.message || "That didn't work. Try again.");
      if (api?.code === "confirmation_mismatch") {
        setShake(true);
        window.setTimeout(() => setShake(false), 450);
      }
    } finally {
      setPending(false);
    }
  }

  return (
    <main className="mx-auto grid max-w-[1120px] gap-8 px-4 py-8 lg:grid-cols-[544px_minmax(0,1fr)]">
      <article>
        <Link href="/board" className="text-[13px] text-muted hover:text-ink">
          Board
        </Link>
        <p className="mt-4 font-mono text-[11px] text-muted">{incident.id}</p>
        <h1 className="mt-3 font-display text-[36px] leading-[1.11] font-normal text-balance">{incident.title}</h1>
        <div className="mt-4 flex flex-wrap gap-2">
          <Badge tone={severityTone(incident.severity)}>{severityLabel(incident.severity)}</Badge>
          <Badge tone={stateTone(incident.state)}>{stateLabel(incident.state)}</Badge>
        </div>
        <p className="mt-6 text-[16px] leading-normal text-ink/90">{incident.summary}</p>
        {incident.root_cause ? <p className="mt-4 text-[16px] leading-normal text-muted">Root cause. {incident.root_cause}</p> : null}
        {incident.resolution ? <p className="mt-2 text-[16px] leading-normal text-muted">Resolution. {incident.resolution}</p> : null}

        <h2 className="mt-10 text-[20px] leading-[1.2] font-medium">Hypotheses</h2>
        {incident.hypotheses.length === 0 ? <p className="mt-3 text-[14px] text-muted">Nothing here yet.</p> : null}
        <ul className="mt-4 space-y-4">
          {incident.hypotheses.map((item) => (
            <li key={item.id}>
              <div className="flex items-baseline justify-between gap-3">
                <p className="text-[16px]">{item.description}</p>
                <span className="font-mono text-[11px] text-muted">{Math.round(item.confidence * 100)}%</span>
              </div>
              <div className="mt-2 h-1 bg-line">
                <div
                  className={`h-1 ${item.status === "supported" ? "bg-accent" : "bg-ink/40"}`}
                  style={{ width: `${Math.round(item.confidence * 100)}%` }}
                />
              </div>
              <p className="mt-1 text-[11px] uppercase text-muted">{item.status}</p>
            </li>
          ))}
        </ul>

        <h2 className="mt-10 text-[20px] leading-[1.2] font-medium">Evidence</h2>
        {incident.findings.length === 0 ? <p className="mt-3 text-[14px] text-muted">Nothing here yet.</p> : null}
        <ul className="mt-4 space-y-3">
          {incident.findings.map((finding) => (
            <li key={finding.id} className="border-t border-line pt-3">
              <p className="text-[16px]">{finding.summary}</p>
              {finding.evidence_refs.map((ref) => (
                <details key={ref.id} className="mt-2">
                  <summary className="cursor-pointer text-[14px] text-muted">{ref.source} {ref.id}</summary>
                  <pre className="mt-2 overflow-auto font-mono text-[11px] text-ink">{ref.excerpt}</pre>
                </details>
              ))}
            </li>
          ))}
        </ul>
        <p className="mt-8">
          <Link href={`/incidents/${incident.id}/trace`} className="text-[14px] text-ink/70 hover:text-ink">
            Open trace
          </Link>
        </p>
      </article>
      <aside>
        <ActionCard
          action={proposed}
          waiting={waiting}
          blocked={Boolean(kill?.active)}
          operator={operator}
          reason={reason}
          phrase={phrase}
          shake={shake}
          pending={pending}
          error={error}
          onReason={setReason}
          onPhrase={setPhrase}
          onDecide={decide}
        />
      </aside>
    </main>
  );
}

function ActionCard({
  action,
  waiting,
  blocked,
  operator,
  reason,
  phrase,
  shake,
  pending,
  error,
  onReason,
  onPhrase,
  onDecide,
}: {
  action: Action | null;
  waiting: boolean;
  blocked: boolean;
  operator: string;
  reason: string;
  phrase: string;
  shake: boolean;
  pending: boolean;
  error: string;
  onReason: (value: string) => void;
  onPhrase: (value: string) => void;
  onDecide: (decision: "approve" | "reject" | "investigate") => void;
}) {
  if (!action) {
    return (
      <Panel className="p-4">
        <h2 className="text-[20px] font-medium">Proposed action</h2>
        <p className="mt-3 text-[16px] text-muted">Nothing proposed yet.</p>
      </Panel>
    );
  }
  return (
    <Panel className="p-4 shadow-[0_18px_50px_rgba(0,0,0,0.18)]">
      <div className="flex items-center justify-between gap-3">
        <h2 className="text-[20px] font-medium">Proposed action</h2>
        <Badge tone={action.tier === "T2" || action.tier === "T3" ? "inverse" : "muted"}>{action.tier}</Badge>
      </div>
      <p className="mt-4 font-mono text-[14px] text-ink">{action.tool}</p>
      <pre className="mt-2 overflow-auto font-mono text-[11px] text-muted">{JSON.stringify(action.args, null, 2)}</pre>
      <dl className="mt-4 space-y-3 text-[14px] leading-normal">
        <div>
          <dt className="text-muted">Risk</dt>
          <dd>{action.risk}</dd>
        </div>
        <div>
          <dt className="text-muted">Blast radius</dt>
          <dd>{action.blast_radius}</dd>
        </div>
        <div>
          <dt className="text-muted">Expected outcome</dt>
          <dd>{action.expected_outcome}</dd>
        </div>
        <div>
          <dt className="text-muted">Rollback</dt>
          <dd>{action.rollback_plan}</dd>
        </div>
      </dl>
      {waiting ? (
        <div className="mt-6 space-y-3">
          <p className="text-[13px] text-muted">Signed in as {operator}</p>
          {action.tier === "T2" ? (
            <label className="block text-[11px] uppercase text-muted">
              Type {action.confirmation_phrase} to confirm
              <input
                value={phrase}
                onChange={(event) => onPhrase(event.target.value)}
                className={`mt-1 h-11 w-full rounded-[3px] border border-line bg-canvas px-3 font-mono text-[14px] text-ink ${shake ? "animate-refuse" : ""}`}
              />
            </label>
          ) : null}
          <label className="block text-[11px] uppercase text-muted">
            Reason
            <textarea
              value={reason}
              onChange={(event) => onReason(event.target.value)}
              rows={3}
              className="mt-1 w-full rounded-[3px] border border-line bg-canvas px-3 py-2 text-[16px] text-ink"
            />
          </label>
          {error ? <p className="text-[14px] text-ink">{error}</p> : null}
          {blocked ? <p className="text-[14px] text-muted">Kill switch is on. Actions are blocked.</p> : null}
          <div className="flex flex-wrap gap-2">
            <Button variant="accent" disabled={pending || blocked} onClick={() => onDecide("approve")}>
              Approve
            </Button>
            <Button variant="ghost" disabled={pending} onClick={() => onDecide("reject")}>
              Reject
            </Button>
            <Button variant="primary" disabled={pending} onClick={() => onDecide("investigate")}>
              Investigate more
            </Button>
          </div>
        </div>
      ) : (
        <p className="mt-6 text-[14px] uppercase text-muted">{action.status}</p>
      )}
    </Panel>
  );
}
