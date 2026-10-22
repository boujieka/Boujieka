"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Field, Input, Select } from "@/components/ui/form";
import { downloadVia } from "./download";
import { useI18n } from "./i18n-provider";

export function ReportForm({ types, sectors, partners, countries }: { types: { code: string; title: string }[]; sectors: [string, string][]; partners: [string, string][]; countries: [string, string][] }) {
  const { d } = useI18n();
  const router = useRouter();
  const [f, setF] = useState({ report_type: types[0]?.code ?? "", format: "pdf", country: "CMR", year_from: "2011", year_to: "2026", sector: "", partner: "" });
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);
  const set = (k: keyof typeof f) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => setF({ ...f, [k]: e.target.value });
  return (
    <form className="space-y-3" onSubmit={async (e) => {
      e.preventDefault();
      setBusy(true);
      setMsg(null);
      const body: Record<string, string | number> = { report_type: f.report_type, format: f.format };
      if (f.country) body.country = f.country;
      if (f.year_from) body.year_from = Number(f.year_from);
      if (f.year_to) body.year_to = Number(f.year_to);
      if (f.sector) body.sector = f.sector;
      if (f.partner) body.partner = f.partner;
      const r = await downloadVia("/api/proxy/reports", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(body) });
      setBusy(false);
      setMsg(r.ok ? d.common.success : `${r.status}: ${r.error}`);
      if (r.ok) router.refresh();
    }}>
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <Field label={d.reports.type} htmlFor="r-type"><Select id="r-type" value={f.report_type} onChange={set("report_type")}>{types.map((t) => <option key={t.code} value={t.code}>{t.title}</option>)}</Select></Field>
        <Field label={d.reports.format} htmlFor="r-format"><Select id="r-format" value={f.format} onChange={set("format")}><option value="pdf">PDF</option><option value="xlsx">Excel (xlsx)</option><option value="csv">CSV</option></Select></Field>
        <Field label={d.common.country} htmlFor="r-country"><Select id="r-country" value={f.country} onChange={set("country")}>{countries.map(([c, n]) => <option key={c} value={c}>{n}</option>)}</Select></Field>
        <Field label={d.common.sector} htmlFor="r-sector"><Select id="r-sector" value={f.sector} onChange={set("sector")}><option value="">{d.common.all}</option>{sectors.map(([c, n]) => <option key={c} value={c}>{n}</option>)}</Select></Field>
        <Field label={`${d.common.years} — ${d.common.from}`} htmlFor="r-yf"><Input id="r-yf" type="number" min={1960} max={2100} value={f.year_from} onChange={set("year_from")} /></Field>
        <Field label={`${d.common.years} — ${d.common.to}`} htmlFor="r-yt"><Input id="r-yt" type="number" min={1960} max={2100} value={f.year_to} onChange={set("year_to")} /></Field>
        <Field label={d.common.partner} htmlFor="r-partner"><Select id="r-partner" value={f.partner} onChange={set("partner")}><option value="">{d.common.all}</option>{partners.map(([c, n]) => <option key={c} value={c}>{n}</option>)}</Select></Field>
      </div>
      <p className="text-xs text-muted">{d.reports.exportsNote}</p>
      <Button type="submit" disabled={busy}>{busy ? d.reports.generating : d.reports.generate}</Button>
      {msg ? <p role="status" className="text-sm break-anywhere">{msg}</p> : null}
    </form>
  );
}
