"use client";

import Link from "next/link";
import { useState } from "react";
import { Alert } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Textarea } from "@/components/ui/form";
import { label } from "@/i18n";
import { currencyEntries, fmtAmount } from "@/lib/format";
import type { AssistantAnswer } from "@/lib/types";
import { apiSend } from "./download";
import { useI18n } from "./i18n-provider";
import { NatureBadge } from "./badges";

const AP2I_RE = /^AP2I-[A-Z]{3}-[A-Z_]+-\d+$/;

function Cell({ k, v }: { k: string; v: unknown }) {
  const { d, locale } = useI18n();
  if (v === null || v === undefined || v === "") return <span className="italic text-muted">{d.common.na}</span>;
  if (typeof v === "string" && AP2I_RE.test(v)) return <Link className="link font-mono text-xs" href={`/projects/${v}`}>{v}</Link>;
  if (k.includes("by_currency") && typeof v === "object" && !Array.isArray(v)) {
    const e = currencyEntries(v as Record<string, string>);
    return e.length ? <ul>{e.map(([c, x]) => <li key={c} className="whitespace-nowrap tabular-nums">{fmtAmount(x, c, locale)}</li>)}</ul> : <span className="italic text-muted">{d.common.na}</span>;
  }
  if (Array.isArray(v)) return v.length ? <ul className="space-y-0.5">{v.map((x, i) => <li key={i}><Cell k={k} v={x} /></li>)}</ul> : <span className="text-muted">—</span>;
  if (typeof v === "object") {
    const o = v as Record<string, unknown>;
    const cur = typeof o.currency === "string" ? o.currency : null;
    return (
      <span className="text-xs">
        {Object.entries(o).filter(([kk]) => kk !== "currency").map(([kk, vv]) => (
          <span key={kk} className="mr-2 inline-block">
            <span className="text-muted">{kk}:</span>{" "}
            {cur && ["committed", "disbursed", "amount", "value"].includes(kk) && (typeof vv === "string" || typeof vv === "number")
              ? <span className="tabular-nums">{fmtAmount(vv, cur, locale) ?? d.common.na}</span>
              : vv === null || vv === undefined ? <span className="italic text-muted">{d.common.na}</span> : String(typeof vv === "object" ? JSON.stringify(vv) : vv)}
          </span>
        ))}
      </span>
    );
  }
  return <span className="break-anywhere">{String(v)}</span>;
}

function RecordTable({ rows }: { rows: Record<string, unknown>[] }) {
  const { d } = useI18n();
  if (!rows.length) return <p className="text-sm text-muted">{d.intelligence.empty}</p>;
  const keys = [...new Set(rows.flatMap((r) => Object.keys(r)))];
  return (
    <div className="max-h-[480px] overflow-auto">
      <table className="w-full text-sm">
        <thead className="sticky top-0 bg-gray-bg text-left text-xs uppercase text-muted"><tr>{keys.map((k) => <th key={k} scope="col" className="px-2 py-1">{k.replace(/_/g, " ")}</th>)}</tr></thead>
        <tbody className="divide-y divide-line">{rows.map((r, i) => <tr key={i} className="align-top">{keys.map((k) => <td key={k} className="px-2 py-1"><Cell k={k} v={r[k]} /></td>)}</tr>)}</tbody>
      </table>
    </div>
  );
}

function List({ items }: { items: string[] }) {
  const { d } = useI18n();
  return items.length ? <ul className="list-disc space-y-1 pl-5 text-sm">{items.map((x, i) => <li key={i}>{x}</li>)}</ul> : <p className="text-sm text-muted">{d.intelligence.empty}</p>;
}

export function Assistant() {
  const { d } = useI18n();
  const [q, setQ] = useState("");
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const [ans, setAns] = useState<AssistantAnswer | null>(null);
  const examples = [d.intelligence.ex1, d.intelligence.ex2, d.intelligence.ex3, d.intelligence.ex4, d.intelligence.ex5, d.intelligence.ex6];

  async function ask(question: string) {
    if (question.trim().length < 3) return;
    setQ(question);
    setBusy(true);
    setErr(null);
    const r = await apiSend<AssistantAnswer>("assistant/ask", "POST", { question: question.trim(), country: "CMR" });
    setBusy(false);
    if (r.ok && r.data) setAns(r.data);
    else setErr(`${r.status}: ${r.error}`);
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardBody>
          <form onSubmit={(e) => { e.preventDefault(); ask(q); }} className="space-y-3">
            <label htmlFor="question" className="sr-only">{d.intelligence.placeholder}</label>
            <Textarea id="question" rows={3} maxLength={1000} value={q} onChange={(e) => setQ(e.target.value)} placeholder={d.intelligence.placeholder} />
            <Button type="submit" disabled={busy || q.trim().length < 3}>{busy ? d.common.loading : d.intelligence.ask}</Button>
          </form>
          <div className="mt-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-muted">{d.intelligence.examples}</p>
            <ul className="mt-2 flex flex-wrap gap-2">
              {examples.map((x) => (
                <li key={x}><button type="button" onClick={() => ask(x)} disabled={busy} className="rounded-full border border-navy/30 bg-navy-50 px-3 py-1 text-left text-sm text-navy hover:bg-navy hover:text-white disabled:opacity-50">{x}</button></li>
              ))}
            </ul>
          </div>
        </CardBody>
      </Card>
      {err ? <Alert tone="danger" title={d.common.error}>{err}</Alert> : null}
      {ans ? (
        <div className="space-y-4" aria-live="polite">
          <div className="flex flex-wrap items-center gap-2 text-sm">
            <span className="font-semibold text-navy">“{ans.question}”</span>
            <Badge tone="outline">{d.intelligence.intent}: {ans.parsed.intent}</Badge>
            <Badge tone="outline">{d.intelligence.provider}: {ans.provider}</Badge>
          </div>
          <Alert tone="warning">{ans.disclaimer}</Alert>
          <Card><CardHeader title={<>{d.intelligence.facts} <NatureBadge value={ans.data_nature.facts} /></>} /><CardBody><RecordTable rows={ans.facts} /></CardBody></Card>
          <Card><CardHeader title={<>{d.intelligence.calculations} <NatureBadge value={ans.data_nature.calculations} /></>} /><CardBody><RecordTable rows={ans.calculations} /></CardBody></Card>
          <div className="grid gap-4 md:grid-cols-2">
            <Card><CardHeader title={<>{d.intelligence.interpretations} <Badge tone="gold">{label(d.natures, ans.data_nature.interpretations ?? "")}</Badge></>} /><CardBody><List items={ans.interpretations} /></CardBody></Card>
            <Card><CardHeader title={d.intelligence.recommendations} /><CardBody><List items={ans.recommendations} /></CardBody></Card>
          </div>
          <Card><CardHeader title={d.intelligence.missing} /><CardBody><List items={ans.missing_information} /></CardBody></Card>
          <Card>
            <CardHeader title={`${d.intelligence.citations} (${ans.citations.length})`} />
            <CardBody>
              {ans.citations.length ? (
                <ul className="max-h-80 space-y-1 overflow-auto text-sm">
                  {ans.citations.map((c) => <li key={c.ap2i_id}><Link className="link font-mono text-xs" href={`/projects/${c.ap2i_id}`}>{c.ap2i_id}</Link> — {c.title} <span className="text-xs text-muted">[{c.sources.join(", ")}]</span></li>)}
                </ul>
              ) : <p className="text-sm text-muted">{d.intelligence.empty}</p>}
            </CardBody>
          </Card>
          <Card>
            <CardHeader title={<>{d.intelligence.narrative} {ans.narrative ? <Badge tone="danger">{d.intelligence.aiGenerated}</Badge> : null}</>} />
            <CardBody className="space-y-3 text-sm">
              {ans.narrative ? <p className="whitespace-pre-line">{ans.narrative}</p> : <p className="text-muted">{d.intelligence.groundingNone}</p>}
              <div>
                <h3 className="font-semibold">{d.intelligence.grounding}</h3>
                {ans.grounding && Object.keys(ans.grounding).length ? (
                  ans.grounding.passed ? <p className="text-emerald">{d.intelligence.groundingPassed} ({ans.grounding.numbers_in_narrative ?? 0})</p> : (
                    <p className="text-danger">{d.intelligence.groundingFailed}{ans.grounding.error ? `: ${ans.grounding.error}` : ""}{ans.grounding.unsupported_numbers?.length ? ` — ${d.intelligence.unsupported}: ${ans.grounding.unsupported_numbers.join(", ")}` : ""}</p>
                  )
                ) : <p className="text-muted">{d.intelligence.groundingNone}</p>}
              </div>
            </CardBody>
          </Card>
        </div>
      ) : null}
    </div>
  );
}
