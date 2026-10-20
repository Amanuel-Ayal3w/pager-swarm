"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { ThemeToggle } from "@/components/theme";
import { Button } from "@/components/ui/button";
import { Panel } from "@/components/ui/panel";
import { DEMO_NAME, DEMO_PASSWORD, writeOperator } from "@/lib/session";

export default function LoginPage() {
  const router = useRouter();
  const [name, setName] = useState(DEMO_NAME);
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [shake, setShake] = useState(false);

  function submit(event: React.FormEvent) {
    event.preventDefault();
    const operator = name.trim();
    if (!operator || password !== DEMO_PASSWORD) {
      setError("That didn't work. Try again.");
      setShake(true);
      window.setTimeout(() => setShake(false), 450);
      return;
    }
    writeOperator(operator);
    router.replace("/board");
  }

  return (
    <main className="relative flex min-h-screen items-center justify-center px-4">
      <ThemeToggle className="absolute top-3 right-3" />
      <Panel className={`w-full max-w-[360px] p-6 ${shake ? "animate-refuse" : ""}`}>
        <p className="font-display text-[16px] uppercase">Pager</p>
        <h1 className="mt-6 text-[24px] leading-[1.17] font-medium">Sign in</h1>
        <p className="mt-2 text-[14px] text-muted">The board keeps your name on each decision.</p>
        <form className="mt-6 space-y-3" onSubmit={submit}>
          <label className="block text-[14px] text-muted">
            Name
            <input
              value={name}
              onChange={(event) => setName(event.target.value)}
              autoComplete="username"
              className="mt-1 h-11 w-full rounded-[3px] border border-line bg-canvas px-3 text-[16px] text-ink"
            />
          </label>
          <label className="block text-[14px] text-muted">
            Password
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              autoComplete="current-password"
              className="mt-1 h-11 w-full rounded-[3px] border border-line bg-canvas px-3 text-[16px] text-ink"
            />
          </label>
          {error ? <p className="text-[14px] text-ink">{error}</p> : null}
          <Button variant="accent" type="submit" className="w-full">
            Sign in
          </Button>
        </form>
        <p className="mt-4 text-[13px] text-muted">
          Demo sign-in is {DEMO_NAME} / {DEMO_PASSWORD}.
        </p>
      </Panel>
    </main>
  );
}
