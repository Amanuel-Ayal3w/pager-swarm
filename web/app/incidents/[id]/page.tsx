export default async function IncidentPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return (
    <main className="mx-auto max-w-[544px] px-4 py-8">
      <p className="font-mono text-[11px] text-muted">{id}</p>
      <h1 className="mt-3 font-display text-[36px] leading-[1.11] font-normal text-balance">Incident</h1>
      <p className="mt-6 text-[16px] leading-normal text-muted">Nothing here yet.</p>
    </main>
  );
}
