"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { createContext, useContext, useEffect, useState } from "react";

import { useLive } from "@/components/live";
import { Sidebar } from "@/components/sidebar";
import { ThemeToggle } from "@/components/theme";
import { Button } from "@/components/ui/button";
import { Panel } from "@/components/ui/panel";
import { postJSON } from "@/lib/api";
import { clearOperator, readOperator } from "@/lib/session";
import type { KillSwitch } from "@/lib/types";

const links = [
  { href: "/board", label: "Board" },
  { href: "/audit", label: "Audit" },
];

type SessionValue = {
  operator: string;
  signOut: () => void;
};

const SessionContext = createContext<SessionValue | null>(null);

export function useSession() {
  const value = useContext(SessionContext);
  if (!value) throw new Error("Sign-in is missing.");
  return value;
}

export function Shell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const { kill, setKill } = useLive();
  const [operator, setOperator] = useState<string | null | undefined>(undefined);
  const [pending, setPending] = useState(false);
  const [ask, setAsk] = useState(false);

  useEffect(() => {
    const name = readOperator();
    setOperator(name);
    const open = pathname === "/" || pathname === "/login";
    if (!name && !open) router.replace("/login");
    if (name && pathname === "/login") router.replace("/board");
  }, [pathname, router]);

  function signOut() {
    clearOperator();
    setOperator(null);
    router.replace("/login");
  }

  async function commit() {
    if (!kill || !operator || pending) return;
    setPending(true);
    try {
      const row = await postJSON<KillSwitch>("/api/killswitch", {
        active: !kill.active,
        operator,
      });
      setKill(row);
      setAsk(false);
    } finally {
      setPending(false);
    }
  }

  if (pathname === "/" || pathname === "/login") return children;
  if (!operator) return <div className="min-h-screen bg-canvas" />;

  return (
    <SessionContext.Provider value={{ operator, signOut }}>
      <div className="min-h-screen lg:grid lg:grid-cols-[auto_minmax(0,1fr)]">
        <Sidebar pathname={pathname} operator={operator} onSignOut={signOut} />
        <div className="min-w-0">
          <header className="sticky top-0 z-20 flex h-11 items-center gap-2 border-b border-line bg-canvas px-3 sm:px-4">
            <Link href="/board" className="font-display shrink-0 text-[16px] uppercase lg:hidden">
              Pager
            </Link>
            <nav className="flex min-w-0 items-center lg:hidden">
              <NavLinks pathname={pathname} />
            </nav>
            <div className="ml-auto flex shrink-0 items-center gap-3">
              <span className="hidden truncate text-[13px] text-muted sm:inline lg:hidden">{operator}</span>
              <button type="button" onClick={signOut} className="text-[13px] text-muted hover:text-ink lg:hidden">
                Sign out
              </button>
              <ThemeToggle className="h-8 w-8" />
              <button
                type="button"
                onClick={() => setAsk(true)}
                disabled={!kill || pending}
                className={`h-8 rounded-[3px] px-3 text-[10px] uppercase tracking-wide transition-colors duration-150 disabled:opacity-40 ${
                  kill?.active ? "bg-ink text-canvas" : "border border-line text-ink hover:bg-ink/10"
                }`}
              >
                {kill?.active ? "Resume" : "Kill switch"}
              </button>
            </div>
          </header>
          {kill?.active ? (
            <p className="bg-ink px-4 py-2 text-center text-[14px] text-canvas">Kill switch is on. Agents and actions are halted.</p>
          ) : null}
          {children}
        </div>
      </div>
      {ask && kill ? (
        <div className="fixed inset-0 z-30 flex items-start justify-center bg-ink/40 px-4 pt-24">
          <Panel className="w-full max-w-[360px] p-4 shadow-[0_18px_50px_rgba(0,0,0,0.18)]">
            <p className="text-[16px] leading-normal">{kill.active ? "Resume agents?" : "Halt every agent and block actions?"}</p>
            <div className="mt-4 flex gap-2">
              <Button variant="primary" onClick={commit} disabled={pending}>
                {kill.active ? "Resume" : "Halt"}
              </Button>
              <Button variant="ghost" onClick={() => setAsk(false)}>
                Cancel
              </Button>
            </div>
          </Panel>
        </div>
      ) : null}
    </SessionContext.Provider>
  );
}

function NavLinks({ pathname }: { pathname: string }) {
  return (
    <>
      {links.map((link) => {
        const active = link.href === "/board" ? pathname === "/board" : pathname.startsWith(link.href);
        return (
          <Link
            key={link.href}
            href={link.href}
            className={`inline-flex h-8 items-center rounded-[3px] px-3 text-[13px] normal-case transition-colors duration-150 ${
              active ? "bg-ink/[0.06] text-ink" : "text-ink/70 hover:bg-ink/[0.04] hover:text-ink"
            }`}
          >
            {link.label}
          </Link>
        );
      })}
    </>
  );
}
