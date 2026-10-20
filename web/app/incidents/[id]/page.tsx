import { IncidentView } from "@/components/incident-view";

export default async function IncidentPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return <IncidentView id={id} />;
}
