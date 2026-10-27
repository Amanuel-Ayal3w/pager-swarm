"use client";

import Link from "next/link";
import { useEffect, useRef, useState } from "react";

import { useLive } from "@/components/live";
import { AgentWork } from "@/components/agent-work";
import { useSession } from "@/components/shell";
import { Badge } from "@/components/ui/badge";
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
  const [shake, setShake] = useState(false);
  const [pending, setPending] = useState(false);
  useEffect(() => {
    let cancelled = false;
    let timer = 0;
    async function pull() {
      try {
        const row = await getJSON<IncidentDetail>(`/api/incidents/${id}`);
        if (cancelled) return;
        setIncident(row);
        setMissing(false);
        const live = row.state === "INVESTIGATING" || row.state === "REMEDIATING" || row.tasks.some((task) => task.status === "running");
        if (live && !timer) timer = window.setInterval(() => void pull(), 1000);
        if (!live && timer) {
          window.clearInterval(timer);
          timer = 0;
        }
      } catch (err: unknown) {
        if (cancelled) return;
        if (err instanceof ApiError && err.status === 404) setMissing(true);
        else setError("That didn't work. Try again.");
      }
    }
    void pull();
    return () => {
      cancelled = true;
      if (timer) window.clearInterval(timer);
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

  async function decide(
    decision: "approve" | "reject" | "investigate",
    extra?: { reason?: string; phrase?: string },
  ): Promise<boolean> {
    if (!proposed || pending) return false;
    setError("");
    setPending(true);
    try {
      const next = await postJSON<IncidentDetail>(`/api/actions/${proposed.id}/decision`, {
        decision,
        operator,
        reason: extra?.reason || null,
        typed_confirmation: extra?.phrase || null,
        action_version: proposed.version,
      });
      setIncident(next);
      return true;
    } catch (err) {
      const api = err instanceof ApiError ? err : null;
      setError(api?.message || "That didn't work. Try again.");
      if (api?.code === "confirmation_mismatch") {
        setShake(true);
        window.setTimeout(() => setShake(false), 450);
      }
      return false;
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
        {incident.tasks.length > 0 ? (
          <div className="mt-6">
            <div className="flex items-center justify-between gap-3">
              <h2 className="text-[20px] leading-[1.2] font-medium">Work</h2>
              {incident.tasks.some((task) => task.status === "running") ? (
                <button
                  type="button"
                  onClick={() => void postJSON(`/api/runs/stop`, { incident_id: incident.id })}
                  className="text-[13px] text-muted hover:text-ink"
                >
                  Stop
                </button>
              ) : null}
            </div>
            <div className="mt-4">
              <AgentWork tasks={incident.tasks} />
            </div>
          </div>
        ) : null}
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
              {finding.evidence_refs.map((ref, index) => (
                <details key={`${finding.id}-${ref.id}-${index}`} className="mt-2">
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
          shake={shake}
          pending={pending}
          error={error}
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
  shake,
  pending,
  error,
  onDecide,
}: {
  action: Action | null;
  waiting: boolean;
  blocked: boolean;
  operator: string;
  shake: boolean;
  pending: boolean;
  error: string;
  onDecide: (
    decision: "approve" | "reject" | "investigate",
    extra?: { reason?: string; phrase?: string },
  ) => Promise<boolean>;
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
        <CliApproval
          action={action}
          operator={operator}
          blocked={blocked}
          pending={pending}
          error={error}
          shake={shake}
          onDecide={onDecide}
        />
      ) : (
        <p className="mt-6 text-[14px] uppercase text-muted">{action.status}</p>
      )}
    </Panel>
  );
}

type PromptStep = "choice" | "phrase" | "reason";
type PromptLine = { prompt: string; answer: string };

function CliApproval({
  action,
  operator,
  blocked,
  pending,
  error,
  shake,
  onDecide,
}: {
  action: Action;
  operator: string;
  blocked: boolean;
  pending: boolean;
  error: string;
  shake: boolean;
  onDecide: (
    decision: "approve" | "reject" | "investigate",
    extra?: { reason?: string; phrase?: string },
  ) => Promise<boolean>;
}) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [step, setStep] = useState<PromptStep>("choice");
  const [draft, setDraft] = useState("");
  const [lines, setLines] = useState<PromptLine[]>([]);
  const [note, setNote] = useState("");

  useEffect(() => {
    setStep("choice");
    setDraft("");
    setLines([]);
    setNote("");
  }, [action.id, action.version]);

  useEffect(() => {
    inputRef.current?.focus();
  }, [step, action.id]);

  const prompt = step === "phrase" ? `Type \`${action.confirmation_phrase}\`:` : step === "reason" ? "reason:" : "approve?";

  async function answer(raw: string) {
    const value = raw.trim();
    if (pending || (step === "choice" && !value)) return;
    setNote("");
    if (step === "choice") {
      const choice = value.toLowerCase();
      if (choice === "y" || choice === "yes") {
        setLines((rows) => [...rows, { prompt: "approve?", answer: value }]);
        setDraft("");
        if (blocked) {
          setNote("Kill switch is on. Actions are blocked.");
          return;
        }
        if (action.tier === "T2") {
          setStep("phrase");
          return;
        }
        await onDecide("approve");
        return;
      }
      if (choice === "n" || choice === "no") {
        setLines((rows) => [...rows, { prompt: "approve?", answer: value }]);
        setDraft("");
        setStep("reason");
        return;
      }
      if (choice === "i" || choice === "investigate") {
        setLines((rows) => [...rows, { prompt: "approve?", answer: value }]);
        setDraft("");
        await onDecide("investigate");
        return;
      }
      setLines((rows) => [...rows, { prompt: "approve?", answer: value }]);
      setDraft("");
      setNote("Answer y, n, or i.");
      return;
    }
    if (step === "phrase") {
      const ok = await onDecide("approve", { phrase: value });
      if (ok) {
        setLines((rows) => [...rows, { prompt, answer: value }]);
        setDraft("");
      }
      return;
    }
    const ok = await onDecide("reject", { reason: value });
    if (ok) {
      setLines((rows) => [...rows, { prompt, answer: value }]);
      setDraft("");
    }
  }

  return (
    <form
      className="mt-6 border border-line bg-canvas p-3 font-mono text-[13px] leading-relaxed"
      onSubmit={(event) => {
        event.preventDefault();
        void answer(inputRef.current?.value ?? draft);
      }}
    >
      <p className="text-ink">
        {action.incident_id} proposes {action.tool} ({action.tier}).
      </p>
      <p className="text-muted">Signed in as {operator}</p>
      {lines.map((line, index) => (
        <p key={`${line.prompt}-${index}`}>
          <span className="text-muted">{line.prompt}</span> <span className="text-ink">{line.answer}</span>
        </p>
      ))}
      <label className="mt-1 flex items-center gap-2">
        <span className="text-accent">{prompt}</span>
        <input
          ref={inputRef}
          value={draft}
          disabled={pending}
          onChange={(event) => setDraft(event.target.value)}
          aria-label={prompt}
          className={`min-w-0 flex-1 bg-transparent text-ink outline-none disabled:opacity-40 ${shake ? "animate-refuse" : ""}`}
          autoComplete="off"
          spellCheck={false}
        />
      </label>
      {step === "choice" ? (
        <p className="mt-2 flex gap-3 text-[11px] text-muted">
          <button type="button" className="hover:text-ink" disabled={pending} onClick={() => void answer("y")}>
            y approve
          </button>
          <button type="button" className="hover:text-ink" disabled={pending} onClick={() => void answer("n")}>
            n reject
          </button>
          <button type="button" className="hover:text-ink" disabled={pending} onClick={() => void answer("i")}>
            i investigate
          </button>
        </p>
      ) : null}
      {note ? <p className="mt-2 text-ink">{note}</p> : null}
      {error ? <p className="mt-2 text-ink">{error}</p> : null}
      {blocked ? <p className="mt-2 text-muted">Kill switch is on. Actions are blocked.</p> : null}
    </form>
  );
}
