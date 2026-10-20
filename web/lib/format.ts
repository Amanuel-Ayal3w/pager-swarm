export function stateLabel(state: string) {
  const text = state.replaceAll("_", " ").toLowerCase();
  return text.charAt(0).toUpperCase() + text.slice(1);
}

export function severityLabel(severity: string) {
  const level = severity.replace("sev", "");
  return `Sev ${level}`;
}

export function ago(iso: string) {
  const minutes = Math.round((Date.now() - new Date(iso).getTime()) / 60000);
  if (minutes < 1) return "Just now";
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.round(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  return `${Math.round(hours / 24)}d ago`;
}

export function money(value: number) {
  if (value === 0) return "$0.00";
  return `$${value.toFixed(value < 0.01 ? 4 : 2)}`;
}

export function stateTone(state: string) {
  if (state === "RESOLVED" || state === "AWAITING_APPROVAL") return "accent";
  if (state === "ESCALATED") return "inverse";
  return "muted";
}

export function severityTone(severity: string) {
  if (severity === "sev1") return "inverse";
  if (severity === "sev2") return "solid";
  return "muted";
}
