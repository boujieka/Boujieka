import Link from "next/link";

export function Kpi({
  label,
  value,
  hint,
  href,
}: {
  label: string;
  value: React.ReactNode;
  hint?: React.ReactNode;
  href?: string;
}) {
  const body = (
    <>
      <div className="text-[11px] font-semibold uppercase tracking-wide text-muted">{label}</div>
      <div className="mt-1 text-2xl font-semibold leading-tight">{value}</div>
      {hint && <div className="mt-1 text-xs text-muted">{hint}</div>}
    </>
  );
  const cls = "block rounded-md border border-border bg-surface px-4 py-3";
  return href ? (
    <Link href={href} className={`${cls} hover:border-border-strong`}>
      {body}
    </Link>
  ) : (
    <div className={cls}>{body}</div>
  );
}
