export type KillSwitch = {
  active: boolean;
  actor: string | null;
  updated_at: string;
};

export type Health = {
  status: string;
  database: string;
  redis: string;
};
