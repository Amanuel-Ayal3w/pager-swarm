"use client";

import { Typed } from "@/components/typed";
import { agentText } from "@/lib/format";
import type { Task } from "@/lib/types";

function lineFor(task: Task) {
  const response = task.response?.trim();
  if (response) return agentText(response);
  return task.step || task.description;
}

export function AgentWork({ tasks, liveOnly = false, showIncident = false }: { tasks: Task[]; liveOnly?: boolean; showIncident?: boolean }) {
  const rows = (liveOnly ? tasks.filter((task) => task.status === "running") : tasks).filter((task) => task.step || task.description || task.response);
  if (rows.length === 0) return null;
  return (
    <ul className="space-y-3" aria-label="Agent work">
      {rows.map((task) => {
        const running = task.status === "running";
        const line = lineFor(task);
        return (
          <li key={task.id}>
            <div className="flex items-center gap-2 text-[13px]">
              {running ? <i className="live-dot" aria-hidden="true" /> : <i className="inline-block h-1.5 w-1.5 rounded-full bg-line" aria-hidden="true" />}
              <span className="font-mono text-[11px] text-ink">{task.agent_id}</span>
              {task.agent_role !== task.agent_id ? <span className="capitalize text-muted">{task.agent_role}</span> : null}
              {showIncident ? <span className="font-mono text-[11px] text-muted">{task.incident_id}</span> : null}
            </div>
            <p className={`mt-1 text-[14px] leading-normal ${running ? "text-ink" : "text-muted"}`}>
              {running ? <Typed text={line} active /> : line}
            </p>
            {running ? <span className="mt-2 block h-1 task-scan" /> : null}
          </li>
        );
      })}
    </ul>
  );
}
