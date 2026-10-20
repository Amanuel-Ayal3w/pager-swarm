"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

import { getJSON, postJSON } from "@/lib/api";
import type { KillSwitch } from "@/lib/types";

const links = [
  { href: "/", label: "Incidents" },
  { href: "/audit", label: "Audit" },
];

export function Header() {
  const pathname = usePathname();
  const [kill, setKill] = useState<KillSwitch | null>(null);
  const [pending, setPending] = useState(false);

  useEffect(() => {
    let cancelled = false;
    getJSON<KillSwitch>("/api/killswitch")
      .then((row) => {
        if (!cancelled) setKill(row);
      })
      .catch(() => {
        if (!cancelled) setKill(null);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  async function toggle() {
    if (!kill || pending) return;
    const next = !kill.active;
    const confirmed = window.confirm(next ? "Halt every agent and block actions?" : "Resume agents?");
    if (!confirmed) return;
    setPending(true);
    try {
      const row = await postJSON<KillSwitch>("/api/killswitch", {
        active: next,
        operator: "on-call",
      });
      setKill(row);
    } finally {
      setPending(false);
    }
  }

  return (
    <>
      <header className="sticky top-0 z-20 flex h-11 items-center justify-between border-b border-line bg-canvas/80 px-4 backdrop-blur-md">
        <div className="flex items-center gap-4">
          <Link href="/" className="font-display text-[16px] uppercase tracking-normal">
            Pager
          </Link>
          <nav className="flex items-center">
            {links.map((link) => {
              const active = link.href === "/" ? pathname === "/" : pathname.startsWith(link.href);
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`inline-flex h-11 items-center px-4 text-[16px] uppercase transition-colors duration-150 ${
                    active ? "text-ink" : "text-white/70 hover:bg-white/[0.035] hover:text-ink"
                  }`}
                >
                  {link.label}
                </Link>
              );
            })}
          </nav>
        </div>
        <button
          type="button"
          onClick={toggle}
          disabled={!kill || pending}
          className={`h-8 rounded-[3px] px-4 text-[10px] uppercase tracking-wide transition-colors duration-150 focus-visible:outline focus-visible:outline-1 focus-visible:outline-white focus-visible:outline-offset-2 disabled:opacity-40 ${
            kill?.active ? "bg-ink text-canvas" : "border border-line text-ink hover:bg-white/10"
          }`}
        >
          {kill?.active ? "Resume" : "Kill switch"}
        </button>
      </header>
      {kill?.active ? (
        <p className="bg-ink px-4 py-2 text-center text-[14px] text-canvas">
          Kill switch is on. Agents and actions are halted.
        </p>
      ) : null}
    </>
  );
}
