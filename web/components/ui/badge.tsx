const tones = {
  accent: "border-accent/40 text-accent",
  inverse: "border-ink bg-ink text-canvas",
  solid: "border-ink/40 text-ink",
  muted: "border-line text-muted",
};

export function Badge({ children, tone = "muted" }: { children: string; tone?: keyof typeof tones }) {
  return (
    <span className={`inline-flex h-6 items-center rounded-full border px-3 text-[11px] uppercase ${tones[tone]}`}>
      {children}
    </span>
  );
}
