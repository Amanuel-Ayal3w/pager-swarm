import { TraceView } from "@/components/trace-view";

export default async function TracePage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return <TraceView id={id} />;
}
