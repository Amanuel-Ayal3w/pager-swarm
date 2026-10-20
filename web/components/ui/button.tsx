import type { ButtonHTMLAttributes } from "react";

const styles = {
  accent: "bg-accent text-on-accent hover:bg-accent/90",
  primary: "bg-ink text-canvas hover:bg-ink/80",
  ghost: "bg-transparent text-ink/70 hover:bg-ink/[0.05] hover:text-ink",
  line: "border border-line text-ink hover:bg-ink/10",
};

export function Button({
  variant = "ghost",
  className = "",
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & { variant?: keyof typeof styles }) {
  return (
    <button
      type="button"
      className={`inline-flex h-11 items-center justify-center rounded-[3px] px-5 text-[10px] uppercase tracking-wide transition-colors duration-150 disabled:opacity-40 ${styles[variant]} ${className}`}
      {...props}
    />
  );
}
