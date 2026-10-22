import Link from "next/link";
import type { Dict } from "@/i18n";
import { buttonClass } from "@/components/ui/button";

export function Pagination({ d, base, params, total, limit, offset }: { d: Dict; base: string; params: Record<string, string | undefined>; total: number; limit: number; offset: number }) {
  const page = Math.floor(offset / limit) + 1;
  const pages = Math.max(1, Math.ceil(total / limit));
  const href = (o: number) => {
    const u = new URLSearchParams();
    for (const [k, v] of Object.entries(params)) if (v) u.set(k, v);
    if (o > 0) u.set("offset", String(o));
    const s = u.toString();
    return s ? `${base}?${s}` : base;
  };
  return (
    <nav aria-label={d.common.page} className="flex flex-wrap items-center justify-between gap-2 px-4 py-3 text-sm">
      <span className="text-muted">{total} {d.common.results} · {d.common.page} {page} {d.common.of} {pages}</span>
      <span className="flex gap-2">
        {offset > 0 ? <Link className={buttonClass("outline", "sm")} href={href(Math.max(0, offset - limit))} rel="prev">← {d.common.previous}</Link> : null}
        {offset + limit < total ? <Link className={buttonClass("outline", "sm")} href={href(offset + limit)} rel="next">{d.common.next} →</Link> : null}
      </span>
    </nav>
  );
}
