export function Panel({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <section className={`rounded-[3px] border border-line bg-surface ${className}`}>{children}</section>;
}
