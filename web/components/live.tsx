"use client";

import { createContext, useContext, useEffect, useMemo, useState } from "react";

import { API_URL, getJSON } from "@/lib/api";
import type { KillSwitch, StreamEvent } from "@/lib/types";

type LiveValue = {
  kill: KillSwitch | null;
  setKill: (row: KillSwitch) => void;
  events: StreamEvent[];
  pulse: number;
};

const LiveContext = createContext<LiveValue | null>(null);

export function useLive() {
  const value = useContext(LiveContext);
  if (!value) throw new Error("Live feed is missing.");
  return value;
}

export function LiveProvider({ children }: { children: React.ReactNode }) {
  const [kill, setKill] = useState<KillSwitch | null>(null);
  const [events, setEvents] = useState<StreamEvent[]>([]);
  const [pulse, setPulse] = useState(0);

  useEffect(() => {
    let cancelled = false;
    getJSON<KillSwitch>("/api/killswitch")
      .then((row) => {
        if (!cancelled) setKill(row);
      })
      .catch(() => {
        if (!cancelled) setKill(null);
      });
    getJSON<StreamEvent[]>("/api/events?limit=40")
      .then((rows) => {
        if (!cancelled) setEvents(rows);
      })
      .catch(() => {
        if (!cancelled) setEvents([]);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    const source = new EventSource(`${API_URL}/api/stream`);
    source.onmessage = (message) => {
      const event = JSON.parse(message.data) as StreamEvent;
      setEvents((current) => (current.some((item) => item.id === event.id) ? current : [...current, event]));
      setPulse((value) => value + 1);
      if (event.event_type === "kill_switch") {
        const active = Boolean(event.payload?.active);
        setKill({ active, actor: event.actor, updated_at: event.created_at });
      }
    };
    return () => source.close();
  }, []);

  const value = useMemo(() => ({ kill, setKill, events, pulse }), [kill, events, pulse]);
  return <LiveContext.Provider value={value}>{children}</LiveContext.Provider>;
}
