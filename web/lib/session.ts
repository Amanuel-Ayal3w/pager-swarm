const KEY = "pager-operator";

export const DEMO_NAME = "on-call";
export const DEMO_PASSWORD = "pager";

export function readOperator() {
  if (typeof window === "undefined") return null;
  return sessionStorage.getItem(KEY);
}

export function writeOperator(name: string) {
  sessionStorage.setItem(KEY, name.trim());
}

export function clearOperator() {
  sessionStorage.removeItem(KEY);
}
