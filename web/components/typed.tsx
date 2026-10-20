"use client";

import { useEffect, useState } from "react";

function reduced() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

export function Typed({ text, active }: { text: string; active: boolean }) {
  const [count, setCount] = useState(text.length);

  useEffect(() => {
    if (!active || reduced()) {
      setCount(text.length);
      return;
    }
    setCount(0);
    let index = 0;
    const timer = window.setInterval(() => {
      index += 1;
      setCount(index);
      if (index >= text.length) window.clearInterval(timer);
    }, 16);
    return () => window.clearInterval(timer);
  }, [text, active]);

  const typing = active && count < text.length;
  return (
    <span>
      {text.slice(0, count)}
      {typing ? <i className="caret" aria-hidden="true" /> : null}
    </span>
  );
}
