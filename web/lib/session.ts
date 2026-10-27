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

const DEMO = "pager-demo";
const DEMO_KEY = "pager-demo-key";

export function readDemo() {
  if (typeof window === "undefined") return { on: false, hasKey: false };
  return { on: sessionStorage.getItem(DEMO) === "1", hasKey: Boolean(sessionStorage.getItem(DEMO_KEY)) };
}

export function readDemoKey() {
  if (typeof window === "undefined") return "";
  return sessionStorage.getItem(DEMO_KEY) || "";
}

export function writeDemo(on: boolean, apiKey: string | null) {
  sessionStorage.setItem(DEMO, on ? "1" : "0");
  if (apiKey !== null) {
    const key = apiKey.trim();
    if (key) sessionStorage.setItem(DEMO_KEY, key);
    else sessionStorage.removeItem(DEMO_KEY);
  }
  window.dispatchEvent(new Event("pager-demo"));
}
