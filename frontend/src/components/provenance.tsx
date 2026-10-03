import { Badge } from "@/components/ui/badge";
import { emptyLabel, formatDate } from "@/lib/format";
import type { DataNature, FieldStatus, Provenance } from "@/lib/types";
import { cn } from "@/lib/utils";

const NATURE: Record<DataNature, { label: string; variant: "fact" | "calc" | "estimate" | "ai" | "synthetic"; title: string }> = {
  FACT: { label: "FACT", variant: "fact", title: "As published by the cited source" },
  CALCULATION: { label: "CALC", variant: "calc", title: "Derived deterministically from published values" },
  ESTIMATE: { label: "ESTIMATE", variant: "estimate", title: "Modelled or assumed value" },
  AI_INTERPRETATION: { label: "AI", variant: "ai", title: "AI-written interpretation; not a data source" },
  SYNTHETIC: { label: "SYNTHETIC", variant: "synthetic", title: "Generated development data — not real market data" },
};

export function NatureBadge({ nature }: { nature: DataNature }) {
  const n = NATURE[nature];
  return (
    <Badge variant={n.variant} title={n.title}>
      {n.label}
    </Badge>
  );
}

const VERIFICATION_VARIANT: Record<string, "good" | "warning" | "critical" | "synthetic" | "neutral"> = {
  verified: "good",
  unverified: "warning",
  conflicting: "critical",
  rejected: "critical",
  synthetic: "synthetic",
};

export function VerificationBadge({ status }: { status: string }) {
  const icon = status === "verified" ? "✓" : status === "synthetic" ? "⚠" : status === "unverified" ? "?" : "!";
  return (
    <Badge variant={VERIFICATION_VARIANT[status] ?? "neutral"}>
      <span aria-hidden>{icon}</span>
      {status}
    </Badge>
  );
}

/** Renders a value, or the explicit reason it is missing. Never a blank or a guess. */
export function Field({
  value,
  status,
  className,
}: {
  value: string | number | null | undefined;
  status?: FieldStatus;
  className?: string;
}) {
  if (value === null || value === undefined || value === "") {
    return <span className={cn("text-subtle italic", className)}>{emptyLabel(status)}</span>;
  }
  return <span className={className}>{value}</span>;
}

export function ProvenancePanel({ p }: { p: Provenance }) {
  const rows: [string, React.ReactNode][] = [
    ["Data nature", <NatureBadge key="n" nature={p.data_nature} />],
    ["Verification", <VerificationBadge key="v" status={p.verification_status} />],
    ["Source", <Field key="s" value={p.source ? `${p.source.name}` : null} />],
    [
      "Source URL",
      p.source_url ? (
        <a key="u" href={p.source_url} className="text-accent underline break-all" rel="noopener noreferrer" target="_blank">
          {p.source_url}
        </a>
      ) : (
        <Field key="u" value={null} />
      ),
    ],
    ["Source document", <Field key="d" value={p.source_document_id ? `#${p.source_document_id}` : null} />],
    ["Published", <Field key="pd" value={formatDate(p.publication_date)} />],
    ["Extracted", <Field key="e" value={formatDate(p.extracted_at)} />],
    ["Confidence", <Field key="c" value={p.confidence_score} />],
  ];
  return (
    <div>
      <dl className="grid grid-cols-[auto_1fr] gap-x-4 gap-y-1.5 text-[13px]">
        {rows.map(([k, v]) => (
          <div key={k} className="contents">
            <dt className="text-muted">{k}</dt>
            <dd className="min-w-0">{v}</dd>
          </div>
        ))}
      </dl>
      {p.notes && <p className="mt-3 border-t border-border pt-2 text-xs text-muted">{p.notes}</p>}
    </div>
  );
}

export function SyntheticBanner() {
  return (
    <div
      role="note"
      className="border-b border-[var(--nature-synthetic)] bg-[color-mix(in_srgb,var(--nature-synthetic)_8%,transparent)] px-4 py-1.5 text-center text-xs text-foreground"
    >
      <strong className="text-[var(--nature-synthetic)]">SYNTHETIC DATA</strong> — market data shown
      is generated for development and is <strong>not real</strong>. Do not use it for any decision.
    </div>
  );
}
