"use client";

import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import { Panel } from "@/components/ui/panel";
import { readDemo, writeDemo } from "@/lib/session";

export function SettingsDialog({ onClose }: { onClose: () => void }) {
  const [on, setOn] = useState(false);
  const [hasKey, setHasKey] = useState(false);
  const [key, setKey] = useState("");

  useEffect(() => {
    const demo = readDemo();
    setOn(demo.on);
    setHasKey(demo.hasKey);
  }, []);

  function save() {
    const typed = key.trim();
    writeDemo(on, typed ? key : hasKey ? null : "");
    onClose();
  }

  return (
    <div className="fixed inset-0 z-30 flex items-start justify-center bg-ink/40 px-4 pt-24">
      <Panel className="w-full max-w-[360px] p-4 shadow-[0_18px_50px_rgba(0,0,0,0.18)]">
        <h2 className="text-[16px] font-medium">Settings</h2>
        <p className="mt-2 text-[14px] text-muted">Demo mode uses a key you type here. It stays in this browser.</p>
        <button
          type="button"
          onClick={() => setOn((value) => !value)}
          className="mt-4 flex w-full items-center justify-between border border-line px-3 py-2 text-left text-[14px]"
          aria-pressed={on}
        >
          <span>Demo mode</span>
          <span className="font-mono text-[11px] uppercase tracking-wide">{on ? "On" : "Off"}</span>
        </button>
        <label className="mt-4 block text-[13px] text-muted" htmlFor="demo-key">
          Your OpenAI key
        </label>
        <input
          id="demo-key"
          type="password"
          autoComplete="off"
          value={key}
          onChange={(event) => setKey(event.target.value)}
          placeholder={hasKey ? "Key saved in this browser" : "sk-…"}
          className="mt-2 h-11 w-full border border-line bg-canvas px-3 text-[14px] outline-none"
        />
        <div className="mt-4 flex gap-2">
          <Button variant="primary" onClick={save}>
            Save
          </Button>
          <Button variant="ghost" onClick={onClose}>
            Cancel
          </Button>
        </div>
      </Panel>
    </div>
  );
}
