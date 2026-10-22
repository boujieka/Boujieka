import Link from "next/link";
import { notFound } from "next/navigation";
import { VerificationBadge } from "@/components/badges";
import { PageHeader } from "@/components/page-header";
import { ErrorState } from "@/components/states";
import { Alert } from "@/components/ui/alert";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { DateV, V } from "@/components/value";
import { getI18n } from "@/i18n/server";
import { apiGet } from "@/lib/api";

interface SourceRecord {
  id: number; source_identifier: string; record_type: string; country_iso3: string | null; payload_format: string; payload_sha256: string; source_url: string | null;
  source_last_updated: string | null; retrieved_at: string | null; is_latest: boolean; processing_status: string; processing_note: string | null; verification_status: string;
  connector: { key: string; name: string; usage_terms: string | null }; payload?: unknown; raw_text?: string | null; payload_note?: string;
}

export const metadata = { title: "Source" };

export default async function SourcePage({ params }: { params: Promise<{ id: string }> }) {
  const id = (await params).id;
  if (!/^\d+$/.test(id)) notFound();
  const { d } = await getI18n();
  const r = await apiGet<SourceRecord>(`/sources/${id}`);
  if (!r.ok && r.status === 404) notFound();
  if (!r.ok) return <ErrorState d={d} status={r.status} message={r.error} />;
  const s = r.data;
  const projectRef = s.processing_note?.match(/AP2I-[A-Z]{3}-[A-Z]+-\d+/)?.[0];
  const rows: [string, React.ReactNode][] = [
    [d.project.connector, <span key="c">{s.connector.name} <span className="font-mono text-xs text-muted">({s.connector.key})</span></span>],
    [d.project.sourceId, <span key="s" className="font-mono">{s.source_identifier}</span>],
    [d.source.recordType, s.record_type],
    [d.common.country, s.country_iso3],
    ["URL", s.source_url ? <a key="u" className="link break-anywhere" href={s.source_url} target="_blank" rel="noopener noreferrer">{s.source_url}</a> : null],
    [d.project.retrieved, <DateV key="r" value={s.retrieved_at} time />],
    [d.source.sourceUpdated, s.source_last_updated],
    [d.source.format, s.payload_format],
    [d.source.sha, <span key="h" className="font-mono text-xs break-anywhere">{s.payload_sha256}</span>],
    [d.source.processing, <span key="p">{s.processing_status}{s.processing_note ? <span className="text-muted"> — {s.processing_note}</span> : null}{projectRef ? <> · <Link className="link" href={`/projects/${projectRef}`}>{projectRef}</Link></> : null}</span>],
    [d.common.verification, <VerificationBadge key="v" value={s.verification_status} />],
    [d.source.usageTerms, s.connector.usage_terms],
  ];
  return (
    <div className="space-y-4">
      <PageHeader eyebrow={d.source.title} title={`#${s.id} · ${s.source_identifier}`} />
      <Card><CardBody><dl className="divide-y divide-line text-sm">{rows.map(([k, v]) => <div key={k} className="grid gap-1 py-1.5 sm:grid-cols-[200px_1fr]"><dt className="text-muted">{k}</dt><dd className="min-w-0"><V value={v} /></dd></div>)}</dl></CardBody></Card>
      <Card>
        <CardHeader title={d.source.payload} />
        <CardBody>
          {s.payload !== undefined ? <pre className="max-h-[600px] overflow-auto rounded bg-gray-bg p-3 text-xs">{s.raw_text ?? JSON.stringify(s.payload, null, 2)}</pre> : <Alert tone="info">{s.payload_note} <Link className="link" href="/pricing">{d.common.seePricing}</Link></Alert>}
        </CardBody>
      </Card>
    </div>
  );
}
