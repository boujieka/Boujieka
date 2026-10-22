import Link from "next/link";
import { buttonClass } from "@/components/ui/button";
import type { Dict } from "@/i18n";

export type FilterField =
  | { name: string; label: string; type: "select"; options: [string, string][]; value?: string; allLabel?: string }
  | { name: string; label: string; type: "text" | "number"; value?: string; placeholder?: string; min?: number; max?: number }
  | { name: string; label: string; type: "checkbox"; value?: string };

const field = "w-full rounded-md border border-line bg-white px-3 py-2 text-sm focus:border-navy focus:outline-none focus:ring-2 focus:ring-gold";

/** Plain GET form: filters are reflected in the URL (shareable, server-rendered, works without JS). */
export function FilterBar({ d, action, fields, hidden }: { d: Dict; action: string; fields: FilterField[]; hidden?: Record<string, string> }) {
  return (
    <form method="get" action={action} className="mb-4 rounded-lg border border-line bg-white p-3">
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-6">
        {fields.map((f) => {
          const id = `f-${f.name}`;
          return (
            <div key={f.name} className="min-w-0">
              {f.type === "checkbox" ? (
                <label htmlFor={id} className="mt-6 flex items-center gap-2 text-sm">
                  <input id={id} type="checkbox" name={f.name} value="true" defaultChecked={f.value === "true"} className="h-4 w-4 accent-[#082B50]" />
                  {f.label}
                </label>
              ) : (
                <>
                  <label htmlFor={id} className="mb-1 block text-xs font-semibold uppercase tracking-wide text-muted">{f.label}</label>
                  {f.type === "select" ? (
                    <select id={id} name={f.name} defaultValue={f.value ?? ""} className={field}>
                      <option value="">{f.allLabel ?? d.common.all}</option>
                      {f.options.map(([v, l]) => <option key={v} value={v}>{l}</option>)}
                    </select>
                  ) : (
                    <input id={id} name={f.name} type={f.type} defaultValue={f.value ?? ""} placeholder={"placeholder" in f ? f.placeholder : undefined}
                      min={"min" in f ? f.min : undefined} max={"max" in f ? f.max : undefined} className={field} />
                  )}
                </>
              )}
            </div>
          );
        })}
      </div>
      {hidden ? Object.entries(hidden).map(([k, v]) => <input key={k} type="hidden" name={k} value={v} />) : null}
      <div className="mt-3 flex flex-wrap gap-2">
        <button type="submit" className={buttonClass("primary", "sm")}>{d.common.apply}</button>
        <Link href={action} className={buttonClass("outline", "sm")}>{d.common.reset}</Link>
      </div>
    </form>
  );
}

export type SP = Promise<Record<string, string | string[] | undefined>>;

export function one(v: string | string[] | undefined): string | undefined {
  const s = Array.isArray(v) ? v[0] : v;
  return s === undefined || s === "" ? undefined : s;
}

export const YEARS = Array.from({ length: 2026 - 2000 + 1 }, (_, i) => String(2026 - i));
