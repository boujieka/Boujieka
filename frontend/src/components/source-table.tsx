import { Field } from "@/components/provenance";
import { Badge } from "@/components/ui/badge";
import { TBody, TD, TH, THead, TR, Table } from "@/components/ui/table";
import { formatDate, titleCase } from "@/lib/format";
import type { SourceOut } from "@/lib/types";

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
          <TH>URL</TH>
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
            <TD className="max-w-[280px] truncate">
              {s.base_url ? (
                <a href={s.base_url} className="text-accent underline" rel="noopener noreferrer" target="_blank">
                  {s.base_url}
                </a>
              ) : (
                <span className="text-subtle italic">Not configured</span>
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
