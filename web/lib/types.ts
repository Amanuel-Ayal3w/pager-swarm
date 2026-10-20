export type KillSwitch = {
  active: boolean;
  actor: string | null;
  updated_at: string;
};

export type Evidence = {
  id: string;
  source: string;
  excerpt: string;
};

export type Incident = {
  id: string;
  title: string;
  summary: string;
  severity: string;
  state: string;
  opened_at: string;
  closed_at: string | null;
  root_cause: string | null;
  resolution: string | null;
  thread_id: string | null;
  affected_services: string[];
  cost_usd: number;
  token_total: number;
};

export type Task = {
  id: string;
  incident_id: string;
  agent_id: string;
  agent_role: string;
  description: string;
  status: string;
  step: string;
  tokens: number;
  created_at: string;
};

export type Finding = {
  id: string;
  incident_id: string;
  agent_id: string;
  summary: string;
  evidence_refs: Evidence[];
  confidence: number;
  created_at: string;
};

export type Hypothesis = {
  id: string;
  incident_id: string;
  description: string;
  confidence: number;
  status: string;
  created_at: string;
};

export type Action = {
  id: string;
  incident_id: string;
  tool: string;
  args: Record<string, unknown>;
  tier: string;
  risk: string;
  blast_radius: string;
  rollback_plan: string;
  expected_outcome: string;
  confirmation_phrase: string | null;
  status: string;
  version: number;
  created_at: string;
};

export type Approval = {
  id: string;
  action_id: string;
  operator: string;
  decision: string;
  reason: string | null;
  typed_confirmation: string | null;
  action_version: number;
  timestamp: string;
};

export type IncidentDetail = Incident & {
  findings: Finding[];
  hypotheses: Hypothesis[];
  actions: Action[];
  tasks: Task[];
  approvals: Approval[];
};

export type TraceStep = {
  id: string;
  incident_id: string;
  agent_id: string;
  agent_role: string;
  step_no: number;
  prompt_ref: string;
  response: string;
  tool_calls: { tool?: string; tier?: string }[];
  tokens_in: number;
  tokens_out: number;
  cost: number;
  latency_ms: number;
  created_at: string;
};

export type AuditEvent = {
  id: number;
  timestamp: string;
  actor: string;
  event_type: string;
  incident_id: string | null;
  payload: Record<string, unknown>;
  prev_hash: string;
  this_hash: string;
};

export type StreamEvent = {
  id: number;
  incident_id: string | null;
  event_type: string;
  actor: string;
  summary: string;
  payload: Record<string, unknown>;
  created_at: string;
};
