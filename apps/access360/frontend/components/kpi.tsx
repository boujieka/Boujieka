import { cn } from "@/lib/utils";

export function Kpi({ label, value, sub, className, testId }: { label: string; value: string; sub?: string; className?: string; testId?: string }) {
  return (
    <div className={cn("rounded-lg border border-border bg-surface px-4 py-3", className)} data-testid={testId}>
      <div className="text-xs text-muted-foreground">{label}</div>
      <div className="mt-1 text-lg font-semibold tracking-tight text-navy-900 tabular break-words">{value}</div>
      {sub ? <div className="mt-0.5 text-xs text-subtle-foreground">{sub}</div> : null}
    </div>
  );
}
