import { Field } from "@/components/provenance";
import { Badge } from "@/components/ui/badge";
import { TBody, TD, TH, THead, TR, Table } from "@/components/ui/table";
import { formatDate, titleCase } from "@/lib/format";
import type { SourceCandidate, SourceOut } from "@/lib/types";

const CHECK_LABEL: Record<SourceCandidate["check"], { text: string; variant: "good" | "warning" | "critical" }> = {
  http_200: { text: "reachable", variant: "good" },
  http_403: { text: "blocked bots", variant: "warning" },
  search_only: { text: "search only", variant: "critical" },
};

function Candidates({ candidates }: { candidates: SourceCandidate[] }) {
  if (!candidates.length) return <span className="text-subtle italic">No URL proposed</span>;
  return (
    <details>
      <summary className="cursor-pointer text-muted">
        {candidates.length} proposed URL{candidates.length > 1 ? "s" : ""} (unconfirmed)
      </summary>
      <ul className="mt-1 space-y-1.5 whitespace-normal">
        {candidates.map((c) => (
          <li key={c.url} className="max-w-[420px]">
            <a href={c.url} className="break-all text-accent underline" rel="noopener noreferrer" target="_blank">
              {c.url}
            </a>
            <div className="flex flex-wrap items-center gap-1 text-xs text-muted">
              <Badge variant={CHECK_LABEL[c.check].variant} title={c.evidence}>
                {CHECK_LABEL[c.check].text}
              </Badge>
              {c.purpose}
            </div>
          </li>
        ))}
      </ul>
    </details>
  );
}

const STATUS_VARIANT: Record<string, "good" | "warning" | "critical" | "neutral"> = {
  active: "good",
  pending_configuration: "warning",
  failing: "critical",
  disabled: "neutral",
};

export function SourceTable({ sources }: { sources: SourceOut[] }) {
  if (!sources.length) return <p className="px-4 py-4 text-sm text-muted">None.</p>;
  return (
    <Table>
      <THead>
        <tr>
          <TH title="1 = most authoritative">Priority</TH>
          <TH>Source</TH>
          <TH>Category</TH>
          <TH>URL (confirmed / proposed)</TH>
          <TH>Status</TH>
          <TH>Last success</TH>
        </tr>
      </THead>
      <TBody>
        {sources.map((s) => (
          <TR key={s.source_id}>
            <TD className="num">{s.priority}</TD>
            <TD className="whitespace-normal">
              {s.name}
              {s.is_synthetic && (
                <Badge variant="synthetic" className="ml-2">
                  SYNTHETIC
                </Badge>
              )}
            </TD>
            <TD>{titleCase(s.category)}</TD>
            <TD className="text-[13px]">
              {s.base_url ? (
                <a href={s.base_url} className="text-accent underline" rel="noopener noreferrer" target="_blank">
                  {s.base_url}
                </a>
              ) : (
                <Candidates candidates={s.candidates} />
              )}
            </TD>
            <TD>
              <Badge variant={STATUS_VARIANT[s.status] ?? "neutral"}>{s.status.replace(/_/g, " ")}</Badge>
            </TD>
            <TD className="num">
              <Field value={formatDate(s.last_success_at)} />
            </TD>
          </TR>
        ))}
      </TBody>
    </Table>
  );
}
