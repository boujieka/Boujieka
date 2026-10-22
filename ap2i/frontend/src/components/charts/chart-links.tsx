"use client";

import Link from "next/link";

/** Accessible list of the drill-down links behind a chart (keyboard and screen-reader users). */
export function ChartLinks({ items, label }: { items: { label: string; href: string | null; value?: string }[]; label: string }) {
  return (
    <details className="mt-2 text-sm">
      <summary className="cursor-pointer text-muted">{label}</summary>
      <ul className="mt-2 grid gap-1 sm:grid-cols-2 lg:grid-cols-3">
        {items.map((it) => (
          <li key={it.label} className="min-w-0 truncate">
            {it.href ? <Link className="link" href={it.href}>{it.label}</Link> : <span>{it.label}</span>}
            {it.value ? <span className="text-muted"> — {it.value}</span> : null}
          </li>
        ))}
      </ul>
    </details>
  );
}
