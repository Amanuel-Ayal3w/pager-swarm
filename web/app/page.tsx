"use client";

import Link from "next/link";
import { ChevronDown, Copy, LayoutGrid, Radio } from "lucide-react";
import { useEffect, useState } from "react";

import { readOperator } from "@/lib/session";
import { ThemeToggle } from "@/components/theme";

const nav = [
  { href: "#swarm", index: "01", label: "Swarm" },
  { href: "#approval", index: "02", label: "Approval" },
  { href: "#tiers", index: "03", label: "Tiers" },
  { href: "/board", index: "04", label: "Board" },
  { href: "/audit", index: "05", label: "Audit" },
  { href: "#trace", index: "06", label: "Trace" },
];

const tabs = [
  { id: "triage", label: "Triage", line: "pager open INC-1048" },
  { id: "logs", label: "Logs", line: "pager logs api --since 5m" },
  { id: "cause", label: "Cause", line: "pager hypothesis --top" },
  { id: "action", label: "Action", line: "pager approve ACT-1048" },
  { id: "audit", label: "Audit", line: "pager audit INC-1048" },
];

const rail = ["LangGraph", "Postgres", "Redis", "FastAPI", "Next.js", "SSE", "Audit log", "Kill switch"];

const tiers = [
  { tier: "T0", name: "Read", text: "Logs and metrics. No approval." },
  { tier: "T1", name: "Narrow", text: "Restart one service. One click." },
  { tier: "T2", name: "Wide", text: "Rollback or config. Type the phrase." },
  { tier: "T3", name: "Forbidden", text: "Destructive actions never run." },
];

export default function LandingPage() {
  const [operator, setOperator] = useState<string | null>(null);
  const [tab, setTab] = useState(tabs[0]);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    setOperator(readOperator());
  }, []);

  const next = operator ? "/board" : "/login";

  async function copyLine() {
    try {
      await navigator.clipboard.writeText(tab.line);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1200);
    } catch {
      setCopied(false);
    }
  }

  return (
    <div className="frame min-h-screen">
      <div className="mx-auto min-h-screen max-w-[1280px] border-x border-line bg-canvas">
        <div className="glass sticky top-0 z-20 border-b border-line">
          <p className="border-b border-line px-4 py-2 text-center text-[11px] tracking-wide text-muted uppercase">
            Pager 0.1 is ready.{" "}
            <Link href={next} className="text-ink">
              Open the board
            </Link>
          </p>
          <header className="flex h-11 items-stretch">
            <Link href="/" className="flex shrink-0 items-center gap-2 border-r border-line px-4 font-display text-[13px] tracking-wide uppercase">
              <LayoutGrid size={14} strokeWidth={1.5} />
              Pager
            </Link>
            <nav className="hidden min-w-0 flex-1 items-stretch overflow-x-auto lg:flex">
              {nav.map((item) => (
                <Link key={item.href} href={item.href} className="flex shrink-0 items-center gap-2 border-r border-line px-4 text-[11px] tracking-wide text-muted uppercase transition-colors duration-150 hover:text-ink">
                  <span className="font-mono">{item.index}</span>
                  {item.label}
                </Link>
              ))}
            </nav>
            <div className="ml-auto flex items-stretch">
              <ThemeToggle className="border-l border-line" />
              <Link href={next} aria-label={operator ? "Open board" : "Sign in"} className="flex w-11 items-center justify-center border-l border-line text-muted transition-colors duration-150 hover:text-ink">
                <Radio size={14} strokeWidth={1.5} />
              </Link>
              <Link href={next} className="flex items-center bg-ink px-4 text-[10px] tracking-wide text-canvas uppercase transition-colors duration-150 hover:bg-ink/80">
                {operator ? "Board" : "Sign in"}
              </Link>
            </div>
          </header>
        </div>

        <section className="px-4 pt-20 pb-16 text-center sm:pt-28">
          <p className="font-mono text-[11px] tracking-wide text-muted uppercase">00 / Detect / Diagnose / Approve</p>
          <h1 className="mx-auto mt-6 max-w-[760px] font-display text-[40px] leading-[1.05] font-normal text-balance sm:text-[56px] lg:text-[64px]">
            Agents investigate. You approve.
          </h1>
          <p className="mx-auto mt-6 max-w-[460px] text-[14px] leading-normal text-muted">
            A swarm reads logs, metrics, and deploys. It ranks a cause, then waits for a person.
          </p>
          <Link href={next} className="mt-8 inline-flex h-9 items-center gap-2 bg-ink px-4 text-[10px] tracking-wide text-canvas uppercase transition-colors duration-150 hover:bg-ink/80">
            <ChevronDown size={12} strokeWidth={1.5} />
            Get started
          </Link>

          <div className="glass mx-auto mt-10 max-w-[680px] border border-line text-left">
            <div className="flex overflow-x-auto border-b border-line">
              {tabs.map((item) => (
                <button
                  key={item.id}
                  type="button"
                  onClick={() => setTab(item)}
                  className={`flex h-9 shrink-0 items-center px-4 text-[11px] tracking-wide uppercase transition-colors duration-150 ${
                    tab.id === item.id ? "bg-ink text-canvas" : "text-muted hover:text-ink"
                  }`}
                >
                  {item.label}
                </button>
              ))}
            </div>
            <div className="flex items-center gap-3 px-4 py-3 font-mono text-[13px]">
              <span className="text-accent">$</span>
              <span className="min-w-0 flex-1 truncate text-ink/85">{tab.line}</span>
              <button type="button" onClick={copyLine} aria-label="Copy command" className="text-muted transition-colors duration-150 hover:text-ink">
                <Copy size={14} strokeWidth={1.5} />
              </button>
            </div>
            {copied ? <p className="border-t border-line px-4 py-2 font-mono text-[11px] text-muted">Copied.</p> : null}
          </div>
        </section>

        <div className="overflow-hidden border-y border-line">
          <div className="rail flex w-max">
            {[...rail, ...rail].map((name, index) => (
              <span key={`${name}-${index}`} className="flex h-12 items-center border-r border-line px-8 text-[12px] tracking-wide text-muted uppercase">
                {name}
              </span>
            ))}
          </div>
        </div>

        <section id="swarm" className="grid border-b border-line lg:grid-cols-2">
          <article className="border-b border-line p-6 sm:p-8 lg:border-r lg:border-b-0">
            <p className="font-mono text-[11px] tracking-wide text-muted uppercase">03.1 / Swarm</p>
            <h2 className="mt-4 max-w-[360px] text-[24px] leading-[1.17] font-medium text-balance">Four looks at once.</h2>
            <p className="mt-3 max-w-[420px] text-[14px] leading-normal text-muted">Investigators split logs, metrics, deploys, and health. They share one board.</p>
            <pre className="glass mt-8 overflow-auto border border-line p-4 font-mono text-[12px] leading-relaxed text-ink/80">
              <span className="text-accent">$ pager investigate INC-1048</span>
              {"\n"}triager opened sev 1{"\n"}inv-logs 5xx hit 18%{"\n"}inv-deploys pooling turned off
            </pre>
          </article>
          <article id="approval" className="p-6 sm:p-8">
            <p className="font-mono text-[11px] tracking-wide text-muted uppercase">03.2 / Approval</p>
            <h2 className="mt-4 max-w-[360px] text-[24px] leading-[1.17] font-medium text-balance">Nothing runs until you agree.</h2>
            <p className="mt-3 max-w-[420px] text-[14px] leading-normal text-muted">A rollback shows the blast radius. You type the phrase before it runs.</p>
            <pre className="glass mt-8 overflow-auto border border-line p-4 font-mono text-[12px] leading-relaxed text-ink/80">
              <span className="text-muted">{"// ACT-1048"}</span>
              {"\n"}tool rollback_deploy{"\n"}tier T2{"\n"}
              <span className="text-accent">confirm rollback api</span>
            </pre>
          </article>
        </section>

        <section id="tiers" className="grid gap-px border-b border-line bg-line sm:grid-cols-2 lg:grid-cols-4">
          {tiers.map((item) => (
            <article key={item.tier} className="bg-canvas p-6">
              <p className="font-mono text-[11px] text-muted">{item.tier}</p>
              <h3 className="mt-3 text-[20px] font-medium">{item.name}</h3>
              <p className="mt-2 text-[14px] leading-normal text-muted">{item.text}</p>
            </article>
          ))}
        </section>

        <section id="trace" className="grid lg:grid-cols-2">
          <article className="border-b border-line p-6 sm:p-8 lg:border-r lg:border-b-0">
            <p className="font-mono text-[11px] tracking-wide text-muted uppercase">04 / Trace</p>
            <h2 className="mt-4 text-[24px] leading-[1.17] font-medium">Every step stays visible.</h2>
            <p className="mt-3 max-w-[420px] text-[14px] leading-normal text-muted">Tools, tokens, cost, and the approval sit on one timeline.</p>
          </article>
          <article className="p-6 sm:p-8">
            <p className="font-mono text-[11px] tracking-wide text-muted uppercase">05 / Kill switch</p>
            <h2 className="mt-4 text-[24px] leading-[1.17] font-medium">One control halts the swarm.</h2>
            <p className="mt-3 max-w-[420px] text-[14px] leading-normal text-muted">Agents stop. The next action stays blocked until you resume.</p>
          </article>
        </section>
      </div>
    </div>
  );
}
