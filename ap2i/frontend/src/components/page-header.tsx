export function PageHeader({ title, subtitle, actions, eyebrow }: { title: React.ReactNode; subtitle?: React.ReactNode; actions?: React.ReactNode; eyebrow?: React.ReactNode }) {
  return (
    <div className="mb-6 flex flex-wrap items-end justify-between gap-4">
      <div className="min-w-0">
        {eyebrow ? <div className="mb-1 text-xs font-semibold uppercase tracking-wider text-emerald">{eyebrow}</div> : null}
        <h1 className="text-2xl font-bold text-navy break-anywhere sm:text-3xl">{title}</h1>
        {subtitle ? <p className="mt-1 max-w-3xl text-sm text-muted sm:text-base">{subtitle}</p> : null}
      </div>
      {actions ? <div className="flex flex-wrap gap-2">{actions}</div> : null}
    </div>
  );
}

export function Kpi({ label, value, hint, href }: { label: React.ReactNode; value: React.ReactNode; hint?: React.ReactNode; href?: string }) {
  const inner = (
    <>
      <div className="text-xs font-semibold uppercase tracking-wide text-muted">{label}</div>
      <div className="mt-1 text-2xl font-bold text-navy tabular-nums break-anywhere">{value}</div>
      {hint ? <div className="mt-1 text-xs text-muted">{hint}</div> : null}
    </>
  );
  const cls = "block min-w-0 rounded-lg border border-line bg-white p-4 shadow-sm";
  return href ? (
    <a href={href} className={`${cls} no-underline hover:border-navy`}>
      {inner}
    </a>
  ) : (
    <div className={cls}>{inner}</div>
  );
}
