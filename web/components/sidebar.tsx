"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import {
  ChevronRight,
  CircleDot,
  FileText,
  Folder,
  LayoutGrid,
  LogOut,
  PanelLeftClose,
  PanelLeftOpen,
  ScrollText,
  Sparkles,
  UserRound,
  type LucideIcon,
} from "lucide-react";

import { useLive } from "@/components/live";
import { getJSON } from "@/lib/api";
import type { Incident } from "@/lib/types";

export function Sidebar({
  pathname,
  operator,
  onSignOut,
}: {
  pathname: string;
  operator: string;
  onSignOut: () => void;
}) {
  const { pulse } = useLive();
  const [incidents, setIncidents] = useState<Incident[] | null>(null);
  const [minimized, setMinimized] = useState(false);
  const [openGroups, setOpenGroups] = useState({ work: true, incidents: true, session: true });
  const [openList, setOpenList] = useState(true);

  useEffect(() => {
    let cancelled = false;
    getJSON<Incident[]>("/api/incidents")
      .then((rows) => {
        if (!cancelled) setIncidents(rows);
      })
      .catch(() => {
        if (!cancelled) setIncidents([]);
      });
    return () => {
      cancelled = true;
    };
  }, [pulse]);

  const crumb = pathname.startsWith("/audit")
    ? "Audit"
    : pathname.includes("/trace")
      ? "Trace"
      : pathname.startsWith("/incidents/")
        ? "Incident"
        : "Board";

  function toggle(group: keyof typeof openGroups) {
    setOpenGroups((current) => ({ ...current, [group]: !current[group] }));
  }

  if (minimized) {
    return (
      <aside className="sticky top-0 hidden h-screen w-14 shrink-0 flex-col items-center border-r border-line bg-canvas lg:flex">
        <div className="flex h-11 w-full items-center justify-center border-b border-line">
          <IconButton label="Expand sidebar" onClick={() => setMinimized(false)}>
            <PanelLeftOpen size={14} strokeWidth={1.5} />
          </IconButton>
        </div>
        <nav className="flex flex-col items-center gap-1 py-3">
          <IconLink href="/board" label="Board" active={pathname === "/board"}>
            <CircleDot size={14} strokeWidth={1.5} />
          </IconLink>
          <IconLink href="/audit" label="Audit" active={pathname.startsWith("/audit")}>
            <ScrollText size={14} strokeWidth={1.5} />
          </IconLink>
          <IconButton label="Incidents" onClick={() => { setMinimized(false); setOpenGroups((current) => ({ ...current, incidents: true })); setOpenList(true); }}>
            <Folder size={14} strokeWidth={1.5} />
          </IconButton>
          <IconButton label="Sign out" onClick={onSignOut}>
            <LogOut size={14} strokeWidth={1.5} />
          </IconButton>
        </nav>
      </aside>
    );
  }

  return (
    <aside className="sticky top-0 hidden h-screen w-[280px] shrink-0 flex-col border-r border-line bg-canvas lg:flex">
      <div className="flex h-11 items-center gap-2 border-b border-line px-4">
        <LayoutGrid size={14} strokeWidth={1.5} />
        <Link href="/board" className="font-display text-[13px] tracking-wide uppercase">
          Pager
        </Link>
        <span className="truncate text-[13px] text-muted">/ {crumb}</span>
        <button
          type="button"
          onClick={() => setMinimized(true)}
          aria-label="Minimize sidebar"
          title="Minimize sidebar"
          className="ml-auto text-muted transition-colors duration-150 hover:text-ink"
        >
          <PanelLeftClose size={14} strokeWidth={1.5} />
        </button>
      </div>
      <nav className="min-h-0 flex-1 overflow-y-auto">
        <Section icon={Sparkles} label="Work" open={openGroups.work} onToggle={() => toggle("work")}>
          <Branch icon={CircleDot} label="Board" href="/board" active={pathname === "/board"} />
          <Branch icon={ScrollText} label="Audit" href="/audit" active={pathname.startsWith("/audit")} last />
        </Section>
        <Section icon={Folder} label="Incidents" open={openGroups.incidents} onToggle={() => toggle("incidents")}>
          <Branch icon={Folder} label="Open" open={openList} onToggle={() => setOpenList((current) => !current)} last>
            {incidents === null ? null : incidents.length === 0 ? (
              <Branch icon={FileText} label="Nothing here yet." last />
            ) : (
              incidents.map((incident, index) => (
                <Branch
                  key={incident.id}
                  icon={FileText}
                  label={incident.title}
                  href={`/incidents/${incident.id}`}
                  active={pathname.startsWith(`/incidents/${incident.id}`)}
                  last={index === incidents.length - 1}
                />
              ))
            )}
          </Branch>
        </Section>
        <Section icon={UserRound} label="Session" open={openGroups.session} onToggle={() => toggle("session")}>
          <Branch icon={UserRound} label={operator} />
          <Branch icon={LogOut} label="Sign out" onClick={onSignOut} last />
        </Section>
      </nav>
    </aside>
  );
}

function IconButton({ label, onClick, children }: { label: string; onClick: () => void; children: React.ReactNode }) {
  return (
    <button type="button" onClick={onClick} aria-label={label} title={label} className="flex h-8 w-8 items-center justify-center text-muted transition-colors duration-150 hover:text-ink">
      {children}
    </button>
  );
}

function IconLink({ href, label, active, children }: { href: string; label: string; active: boolean; children: React.ReactNode }) {
  return (
    <Link href={href} aria-label={label} title={label} className={`flex h-8 w-8 items-center justify-center transition-colors duration-150 ${active ? "text-ink" : "text-muted hover:text-ink"}`}>
      {children}
    </Link>
  );
}

function Section({
  icon: Icon,
  label,
  open,
  onToggle,
  children,
}: {
  icon: LucideIcon;
  label: string;
  open: boolean;
  onToggle: () => void;
  children: React.ReactNode;
}) {
  return (
    <section className="border-b border-line px-3 py-3">
      <button
        type="button"
        onClick={onToggle}
        aria-expanded={open}
        className="flex w-full items-center gap-2 px-1 text-[11px] font-normal tracking-wide text-muted uppercase transition-colors duration-150 hover:text-ink"
      >
        <Icon size={14} strokeWidth={1.5} />
        <span className="flex-1 text-left">{label}</span>
        <ChevronRight size={14} strokeWidth={1.5} className={`transition-transform duration-150 ${open ? "rotate-90" : ""}`} />
      </button>
      {open ? <ul className="mt-1 ml-[7px]">{children}</ul> : null}
    </section>
  );
}

function Branch({
  icon: Icon,
  label,
  href,
  active,
  last,
  open = true,
  onToggle,
  onClick,
  children,
}: {
  icon: LucideIcon;
  label: string;
  href?: string;
  active?: boolean;
  last?: boolean;
  open?: boolean;
  onToggle?: () => void;
  onClick?: () => void;
  children?: React.ReactNode;
}) {
  const folded = Boolean(children) && !open;
  const tone = active ? "text-ink" : "text-muted hover:text-ink";
  const row = (
    <span className={`flex h-7 min-w-0 items-center gap-2 text-[13px] transition-colors duration-150 ${tone}`}>
      {children ? (
        <ChevronRight size={14} strokeWidth={1.5} className={`shrink-0 transition-transform duration-150 ${open ? "rotate-90" : ""}`} />
      ) : null}
      <Icon size={14} strokeWidth={1.5} className="shrink-0" />
      <span className="truncate">{label}</span>
    </span>
  );

  return (
    <li className="relative">
      <span className={`absolute top-0 left-0 w-px bg-line ${last && (folded || !children) ? "h-3.5" : "bottom-0"}`} />
      <span className="absolute top-3.5 left-0 h-px w-3 bg-line" />
      <div className="pl-4">
        {href ? (
          <Link href={href} title={label} className="block">
            {row}
          </Link>
        ) : onToggle ? (
          <button type="button" onClick={onToggle} aria-expanded={open} title={open ? `Minimize ${label}` : `Expand ${label}`} className="block w-full text-left">
            {row}
          </button>
        ) : onClick ? (
          <button type="button" onClick={onClick} className="block w-full text-left">
            {row}
          </button>
        ) : (
          row
        )}
      </div>
      {!folded && children ? <ul className="ml-4">{children}</ul> : null}
    </li>
  );
}
