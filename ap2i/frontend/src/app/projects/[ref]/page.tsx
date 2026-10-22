import Link from "next/link";
import { notFound } from "next/navigation";
import { LevelBadge, NatureBadge, OperationalBadge, ReviewBadge, StatusBadge, VerificationBadge } from "@/components/badges";
import { CoverageNotice } from "@/components/coverage";
import { PageHeader } from "@/components/page-header";
import { ProjectFlowsChart } from "@/components/project-flows-chart";
import { ErrorState } from "@/components/states";
import { Alert } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { buttonClass } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";
import { Amount, DateV, NA, Num, Pct, Text, V } from "@/components/value";
import { getI18n } from "@/i18n/server";
import { label } from "@/i18n";
import { apiGet } from "@/lib/api";
import type { Indicator, ProjectDetail } from "@/lib/types";

export async function generateMetadata({ params }: { params: Promise<{ ref: string }> }) {
  return { title: decodeURIComponent((await params).ref) };
}

type Flow = { flow_type: string; amount: string | null; currency: string | null; value_date: string | null; is_counted: boolean; source_record_id: number | null; data_nature: string | null; agreement: string | null };

function IndicatorValue({ i }: { i: Indicator }) {
  if (i.value === null || i.value === undefined) return <NA />;
  if (i.unit === "ratio") return <Pct value={i.value} />;
  return <><Num value={i.value} digits={2} /> {i.unit}</>;
}

function SrcLink({ id }: { id: number | null | undefined }) {
  if (!id) return <NA />;
  return <Link className="link font-mono text-xs" href={`/sources/${id}`}>#{id}</Link>;
}

export default async function ProjectPage({ params }: { params: Promise<{ ref: string }> }) {
  const ref = decodeURIComponent((await params).ref);
  const { d, locale } = await getI18n();
  const [r, flows] = await Promise.all([apiGet<ProjectDetail>(`/projects/${encodeURIComponent(ref)}`), apiGet<Flow[]>(`/projects/${encodeURIComponent(ref)}/flows`)]);
  if (!r.ok && r.status === 404) notFound();
  if (!r.ok) return <ErrorState d={d} status={r.status} message={r.error} />;
  const p = r.data;
  const sectorName = p.sector ? (locale === "fr" ? p.sector.name_fr : p.sector.name_en) : null;
  const facts: [string, React.ReactNode][] = [
    [d.common.country, p.country ? <Link key="c" className="link" href={`/countries/${p.country}`}>{p.country}</Link> : null],
    [d.common.sector, p.sector ? <Link key="s" className="link" href={`/sectors/${p.sector.code}`}>{sectorName}</Link> : null],
    [d.project.executingAgency, p.executing_agency],
    [d.project.implementingAgency, p.implementing_agency],
    [d.project.supervisingMinistry, p.supervising_ministry],
    [d.project.fundingType, p.funding_type],
    [d.project.approvalDate, p.original_approval_date ? <DateV key="a" value={p.original_approval_date} /> : null],
    [d.project.startDate, p.implementation_start_date ? <DateV key="b" value={p.implementation_start_date} /> : null],
    [d.project.plannedEnd, p.original_completion_date ? <DateV key="e" value={p.original_completion_date} /> : null],
    [d.project.actualEnd, p.actual_completion_date ? <DateV key="f" value={p.actual_completion_date} /> : null],
    [d.project.operational, <OperationalBadge key="o" value={p.operational_status} />],
    [d.project.estimatedCost, p.original_estimated_cost ? <Amount key="g" value={p.original_estimated_cost} currency={p.cost_currency} /> : null],
    [d.project.physicalProgress, p.physical_progress_pct ? <span key="h"><Num value={p.physical_progress_pct} /> % (<DateV value={p.physical_progress_date} />)</span> : null],
    [d.common.lastUpdate, p.last_source_update_at ? <DateV key="i" value={p.last_source_update_at} time /> : null],
  ];
  const sections = [["financing", d.project.agreements], ["indicators", d.project.indicators], ["alerts", d.project.alerts], ["flows", d.project.flows], ["sources", d.project.sources], ["quality", d.project.dataQuality]];

  return (
    <div className="space-y-6">
      <PageHeader eyebrow={<span className="font-mono">{p.ap2i_id}</span>} title={p.title}
        actions={<Link href={`/rescue?project=${encodeURIComponent(p.ap2i_id)}`} className={buttonClass("outline")}>{d.project.createRescue}</Link>} />
      <div className="-mt-3 flex flex-wrap gap-2">
        <StatusBadge value={p.status} /><VerificationBadge value={p.verification_status} /><NatureBadge value={p.data_nature} />
        {sectorName ? <Badge tone="outline">{sectorName}</Badge> : null}
        {p.partners.map((x) => <Badge key={x} tone="navy">{x}</Badge>)}
        {p.private ? <Badge tone="gold">private</Badge> : null}
      </div>
      <nav aria-label={d.project.header} className="flex flex-wrap gap-x-4 gap-y-1 text-sm">
        {sections.map(([id, t]) => <a key={id} className="link" href={`#${id}`}>{t}</a>)}
      </nav>
      {p.pending_match_candidates > 0 ? <Alert tone="warning" title={`${d.project.pendingMatches}: ${p.pending_match_candidates}`} /> : null}

      <div className="grid gap-4 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)]">
        <Card>
          <CardHeader title={d.project.description} />
          <CardBody className="space-y-4 text-sm">
            <Text value={p.description} />
            <div><h3 className="font-semibold text-navy">{d.project.objectives}</h3><Text value={p.objectives} /></div>
          </CardBody>
        </Card>
        <Card>
          <CardHeader title={d.common.details} />
          <CardBody>
            <dl className="divide-y divide-line text-sm">
              {facts.map(([k, v]) => <div key={k} className="grid grid-cols-2 gap-2 py-1.5"><dt className="text-muted">{k}</dt><dd className="min-w-0 break-anywhere"><V value={v} /></dd></div>)}
            </dl>
          </CardBody>
        </Card>
      </div>

      <Card id="financing">
        <CardHeader title={d.project.agreements} description={p.financials?.note} />
        <Table caption={d.project.agreements}>
          <THead><TR><TH>{d.common.partner}</TH><TH>{d.project.sourceId}</TH><TH>{d.common.instrument}</TH><TH>{d.project.approvalDate}</TH><TH>{d.project.closing}</TH><TH>{d.common.currency}</TH><TH>{d.countries.committed}</TH><TH>{d.project.disbursedCumulative}</TH><TH>{d.project.undisbursed}</TH><TH>{d.common.source}</TH></TR></THead>
          <TBody>
            {p.agreements.map((a) => {
              const pos = p.financials?.agreements.find((x) => x.agreement_id === a.id);
              return (
                <TR key={a.id}>
                  <TD>{a.partner?.name ?? <NA />}<div className="mt-1"><NatureBadge value={a.data_nature} /> <VerificationBadge value={a.verification_status} /></div></TD>
                  <TD className="font-mono text-xs">{a.source_identifier ?? <NA />}{a.parent_source_identifier ? <div className="text-muted">↳ {a.parent_source_identifier}</div> : null}</TD>
                  <TD>{a.instrument ?? a.instrument_label ?? <NA />}</TD>
                  <TD className="whitespace-nowrap"><DateV value={a.approval_date} /></TD>
                  <TD className="whitespace-nowrap"><DateV value={a.closing_date_current} />{a.closing_date_original && a.closing_date_original !== a.closing_date_current ? <div className="text-xs text-muted">orig. <DateV value={a.closing_date_original} /></div> : null}</TD>
                  <TD>{a.currency ?? <NA />}</TD>
                  <TD className="min-w-48"><Amount value={pos?.committed ?? null} currency={pos?.currency ?? a.currency} /><div className="text-xs text-muted">{d.project.committedBasis}: {pos?.committed_basis ?? a.amount_label ?? d.common.na}</div></TD>
                  <TD className="min-w-48"><Amount value={pos?.disbursed ?? null} currency={pos?.currency ?? a.currency} />{pos?.disbursed_as_of ? <span className="text-xs text-muted"> {d.project.asOf} <DateV value={pos.disbursed_as_of} /></span> : null}<div className="text-xs text-muted">{d.project.disbursedBasis}: {pos?.disbursed_basis ?? d.common.na}</div></TD>
                  <TD><Amount value={pos?.undisbursed ?? null} currency={pos?.currency ?? a.currency} /></TD>
                  <TD>{a.source ? <><SrcLink id={a.source.record_id} /> <span className="text-xs text-muted">{a.source.connector}</span>{a.source.url ? <div><a className="link text-xs" href={a.source.url} target="_blank" rel="noopener noreferrer">URL ↗</a></div> : null}</> : <NA />}</TD>
                </TR>
              );
            })}
          </TBody>
        </Table>
        <CardBody className="space-y-4">
          {p.agreements.map((a) => a.commitments.length ? (
            <div key={a.id}>
              <h3 className="text-sm font-semibold text-navy">{d.project.commitmentsList} — <span className="font-mono">{a.source_identifier}</span></h3>
              <Table caption={d.project.commitmentsList}>
                <THead><TR><TH>{d.common.type}</TH><TH>{d.common.amount}</TH><TH>{d.common.date}</TH><TH>{d.project.counted}</TH><TH>{d.project.countingNote}</TH><TH>{d.common.source}</TH></TR></THead>
                <TBody>{a.commitments.map((c, i) => (
                  <TR key={i}><TD>{c.commitment_type}</TD><TD><Amount value={c.amount} currency={c.currency} /></TD><TD><DateV value={c.value_date} /></TD>
                    <TD>{c.is_counted ? <Badge tone="emerald">{d.project.counted}</Badge> : <Badge tone="outline">{d.project.notCounted}</Badge>}</TD>
                    <TD className="text-xs"><V value={c.counting_note} /></TD><TD><SrcLink id={c.source_record_id} /></TD></TR>))}
                </TBody>
              </Table>
            </div>
          ) : null)}
          {p.financials?.totals_by_currency ? (
            <div>
              <h3 className="text-sm font-semibold text-navy">{d.project.totalsByCurrency}</h3>
              <Table caption={d.project.totalsByCurrency}>
                <THead><TR><TH>{d.common.currency}</TH><TH>{d.countries.committed}</TH><TH>{d.countries.disbursed}</TH><TH>{d.project.cancelled}</TH></TR></THead>
                <TBody>{Object.entries(p.financials.totals_by_currency).map(([cur, t]) => (
                  <TR key={cur}><TD>{cur}</TD><TD><Amount value={t.committed ?? null} currency={cur} /></TD><TD><Amount value={t.disbursed ?? null} currency={cur} /></TD><TD><Amount value={t.cancelled ?? null} currency={cur} /></TD></TR>))}
                </TBody>
              </Table>
            </div>
          ) : null}
        </CardBody>
      </Card>

      <Card id="indicators">
        <CardHeader title={d.project.indicators} />
        <Table caption={d.project.indicators}>
          <THead><TR><TH>{d.common.name}</TH><TH>{d.common.value}</TH><TH>{d.project.formula}</TH><TH>{d.project.inputs}</TH><TH>{d.project.missingInputs}</TH><TH>{d.project.limitations}</TH></TR></THead>
          <TBody>{(p.financials?.indicators ?? []).map((i, k) => (
            <TR key={`${i.code}-${k}`}>
              <TD className="min-w-40">{i.label}<div className="mt-1"><NatureBadge value={i.data_nature} /></div>{i.as_of ? <div className="text-xs text-muted">{d.project.asOf} <DateV value={i.as_of} /></div> : null}</TD>
              <TD className="whitespace-nowrap font-semibold"><IndicatorValue i={i} /></TD>
              <TD className="min-w-48 font-mono text-xs">{i.formula}</TD>
              <TD className="min-w-48 text-xs">{i.inputs.length ? <ul>{i.inputs.map((x, j) => <li key={j}><span className="text-muted">{x.name}:</span> {x.value === null || x.value === undefined ? <NA /> : Array.isArray(x.value) ? x.value.map((v) => <span key={String(v)} className="mr-1"><SrcLink id={Number(v)} /></span>) : String(x.value)}{x.currency ? ` ${x.currency}` : ""}</li>)}</ul> : <NA />}</TD>
              <TD className="text-xs">{i.missing_inputs.length ? <ul className="text-danger">{i.missing_inputs.map((m) => <li key={m}>{m}</li>)}</ul> : "—"}</TD>
              <TD className="text-xs">{i.limitations.length ? <ul>{i.limitations.map((m) => <li key={m}>{m}</li>)}</ul> : "—"}</TD>
            </TR>))}
          </TBody>
        </Table>
      </Card>

      <Card id="alerts">
        <CardHeader title={d.project.alerts} description={d.performance.disclaimer} />
        <CardBody className="space-y-3">
          {p.alerts.length === 0 ? <p className="text-sm text-muted">{d.project.noAlerts}</p> : p.alerts.map((a) => (
            <div key={a.id} className="rounded-md border border-line p-3 text-sm">
              <div className="flex flex-wrap items-center gap-2"><LevelBadge value={a.level} /><Link className="link font-mono text-xs" href={`/performance?rule=${a.rule_code}`}>{a.rule_code}</Link><span className="text-xs text-muted">{a.alert_id} · {d.project.asOf} <DateV value={a.as_of} /></span><ReviewBadge value={a.review_status} /></div>
              <dl className="mt-2 grid gap-1 sm:grid-cols-[180px_1fr]">
                <dt className="text-muted">{d.project.observed}</dt><dd>{a.observed_value}</dd>
                <dt className="text-muted">{d.project.threshold}</dt><dd>{a.threshold}</dd>
                <dt className="text-muted">{d.common.source}</dt><dd>{a.source} {(a.source_record_ids ?? []).map((id) => <span key={id} className="mr-1"><SrcLink id={id} /></span>)}</dd>
                <dt className="text-muted">{d.project.explanation}</dt><dd>{a.explanation}</dd>
                <dt className="text-muted">{d.project.recommendedVerification}</dt><dd>{a.recommended_verification}</dd>
              </dl>
            </div>
          ))}
        </CardBody>
      </Card>

      <Card id="flows">
        <CardHeader title={d.project.annualFlows} description={d.common.perCurrency} />
        <CardBody>
          {p.annual_flows.length ? <ProjectFlowsChart flows={p.annual_flows} projectId={p.ap2i_id} /> : <p className="text-sm italic text-muted">{d.common.noData}</p>}
          {flows.ok && flows.data.length ? (
            <details className="mt-4">
              <summary className="cursor-pointer text-sm text-navy">{d.explorer.transactions} ({flows.data.length})</summary>
              <Table caption={d.explorer.transactions}>
                <THead><TR><TH>{d.explorer.valueDate}</TH><TH>{d.explorer.flow}</TH><TH>{d.common.amount}</TH><TH>{d.explorer.agreement}</TH><TH>{d.project.counted}</TH><TH>{d.common.dataNature}</TH><TH>{d.common.source}</TH></TR></THead>
                <TBody>{flows.data.map((f, i) => (
                  <TR key={i}><TD><DateV value={f.value_date} /></TD><TD>{f.flow_type}</TD><TD><Amount value={f.amount} currency={f.currency} /></TD><TD className="font-mono text-xs">{f.agreement}</TD><TD>{f.is_counted ? d.common.yes : d.common.no}</TD><TD><NatureBadge value={f.data_nature} /></TD><TD><SrcLink id={f.source_record_id} /></TD></TR>))}
                </TBody>
              </Table>
            </details>
          ) : null}
        </CardBody>
      </Card>

      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader title={d.project.documents} />
          <CardBody>{p.documents.length ? <ul className="space-y-1 text-sm">{p.documents.map((x) => <li key={x.id}>{x.url ? <a className="link" href={x.url} target="_blank" rel="noopener noreferrer">{x.title ?? x.url}</a> : x.title} <span className="text-xs text-muted">{x.doc_type}{x.published_date ? ` · ${x.published_date}` : ""}</span></li>)}</ul> : <p className="text-sm text-muted">{d.project.noDocuments}</p>}</CardBody>
        </Card>
        <Card>
          <CardHeader title={d.project.locations} />
          <CardBody>{p.locations.length ? <ul className="space-y-1 text-sm">{p.locations.map((x, i) => <li key={i}>{x.place_name ?? <NA />} <span className="text-xs text-muted">({x.latitude ?? "?"}, {x.longitude ?? "?"}) · {d.project.precision}: {x.precision ?? d.common.na}</span></li>)}</ul> : <p className="text-sm text-muted">{d.project.noLocations}</p>}</CardBody>
        </Card>
      </div>

      <Card>
        <CardHeader title={d.project.statusHistory} />
        <Table caption={d.project.statusHistory}>
          <THead><TR><TH>{d.common.status}</TH><TH>{d.project.previous}</TH><TH>{d.project.effective}</TH><TH>{d.project.recorded}</TH><TH>{d.common.note}</TH><TH>{d.common.source}</TH></TR></THead>
          <TBody>{p.status_history.map((h, i) => (
            <TR key={i}><TD><StatusBadge value={h.status} /></TD><TD>{h.previous_status ? label(d.projectStatus, h.previous_status) : "—"}</TD><TD><DateV value={h.effective_date} /></TD><TD><DateV value={h.recorded_at} time /></TD><TD className="text-xs">{h.note}</TD><TD><SrcLink id={h.source_record_id} /></TD></TR>))}
          </TBody>
        </Table>
      </Card>

      <Card id="supervision">
        <CardHeader title={d.project.supervision} />
        <CardBody className="space-y-3 text-sm">
          <p className="text-muted">{d.project.supervisionIntro}</p>
          {p.development_results ? <p><span className="font-semibold text-navy">{d.project.developmentResults} : </span>{p.development_results}</p> : null}
          {p.implementation_progress.length ? (
            <ul className="space-y-3">{p.implementation_progress.map((x, i) => (
              <li key={i} className="rounded border border-line p-3">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="font-semibold"><DateV value={x.report_date} /></span>
                  {x.document ? (x.document.url ? <a className="link text-xs" href={x.document.url} target="_blank" rel="noopener noreferrer">{x.document.doc_type ?? x.document.title}</a> : <span className="text-xs">{x.document.doc_type}</span>) : null}
                  <NatureBadge value={x.data_nature} />
                  <SrcLink id={x.source_record_id} />
                </div>
                {x.rating ? <div className="mt-1 flex flex-wrap gap-1 text-xs"><span className="text-muted">{d.project.ratings} :</span>{x.rating.split("|").map((r) => <Badge key={r} tone="outline">{r.replace("=", " : ")}</Badge>)}</div> : null}
                {x.financial_progress_pct !== null ? <div className="mt-1 text-xs"><span className="text-muted">{d.project.disbursedPct} : </span><Num value={x.financial_progress_pct} digits={2} /> %</div> : null}
                {x.narrative ? <details className="mt-1"><summary className="cursor-pointer text-xs text-muted">{x.narrative.slice(0, 160)}{x.narrative.length > 160 ? "…" : ""}</summary><p className="mt-1 whitespace-pre-line text-xs">{x.narrative}</p></details> : null}
              </li>))}
            </ul>
          ) : <p className="text-muted">{d.project.noSupervision}</p>}
        </CardBody>
      </Card>

      <Card>
        <CardHeader title={d.project.results} />
        {p.results.length ? (
          <Table caption={d.project.results}>
            <THead><TR><TH>{d.common.name}</TH><TH>{d.sectors.unit}</TH><TH>{d.project.baseline}</TH><TH>{d.project.target}</TH><TH>{d.project.observations}</TH></TR></THead>
            <TBody>{p.results.map((x, i) => (
              <TR key={i}><TD className="min-w-56">{x.name}</TD><TD><V value={x.unit} /></TD><TD><Num value={x.baseline_value} digits={2} /></TD><TD><Num value={x.target_value} digits={2} />{x.target_date ? <div className="text-xs text-muted"><DateV value={x.target_date} /></div> : null}</TD>
                <TD className="text-xs">{x.observations.length ? <ul>{x.observations.map((o, j) => <li key={j}>{o.value !== null ? <Num value={o.value} digits={2} /> : <V value={o.value_text} />} <span className="text-muted">({o.period_end ?? d.common.na})</span> <NatureBadge value={o.data_nature} /></li>)}</ul> : <span className="italic text-muted">{d.sectors.noObservations}</span>}</TD></TR>))}
            </TBody>
          </Table>
        ) : <CardBody><p className="text-sm text-muted">{d.project.noResults}</p></CardBody>}
      </Card>

      <Card id="sources">
        <CardHeader title={d.project.sources} />
        <Table caption={d.project.sources}>
          <THead><TR><TH>{d.project.sourceRecord}</TH><TH>{d.project.connector}</TH><TH>{d.project.sourceId}</TH><TH>URL</TH><TH>{d.project.retrieved}</TH><TH>{d.project.linkType}</TH><TH>{d.project.matchRule}</TH></TR></THead>
          <TBody>{p.sources.map((s) => (
            <TR key={s.record_id}><TD><SrcLink id={s.record_id} />{s.is_latest ? null : <Badge tone="outline" className="ml-1">old</Badge>}</TD><TD className="min-w-40">{s.connector_name}<div className="font-mono text-xs text-muted">{s.connector}</div></TD><TD className="font-mono text-xs">{s.source_identifier}</TD>
              <TD>{s.url ? <a className="link text-xs break-anywhere" href={s.url} target="_blank" rel="noopener noreferrer">{s.url}</a> : <NA />}</TD><TD className="whitespace-nowrap"><DateV value={s.retrieved_at} time /></TD><TD>{s.link_type}</TD><TD><V value={s.match_rule} /></TD></TR>))}
          </TBody>
        </Table>
        <CardBody className="text-sm">
          <h3 className="font-semibold text-navy">{d.project.aliases}</h3>
          <ul className="mt-1 flex flex-wrap gap-2">
            {p.identifiers.map((x) => <li key={x.scheme + x.identifier}><Badge tone="outline">{x.scheme}: <span className="ml-1 font-mono">{x.identifier}</span></Badge></li>)}
            {p.aliases.map((x) => <li key={x.alias}><Badge tone="neutral">{x.alias}{x.language ? ` (${x.language})` : ""}</Badge></li>)}
          </ul>
        </CardBody>
      </Card>

      <Card id="quality">
        <CardHeader title={d.project.dataQuality} description={p.data_quality?.assessed_at ? <DateV value={p.data_quality.assessed_at} time /> : undefined} />
        <CardBody className="grid gap-4 md:grid-cols-2">
          {p.data_quality ? (
            <dl className="space-y-1 text-sm">
              {(["completeness", "timeliness", "traceability", "consistency", "source_reliability", "duplicate_risk"] as const).map((k) => (
                <div key={k} className="flex justify-between gap-2"><dt>{d.project.scores[k]}</dt><dd><Pct value={p.data_quality![k]} digits={0} /></dd></div>))}
            </dl>
          ) : <NA />}
          <div className="text-sm">
            <h3 className="font-semibold text-navy">{d.project.missingFields}</h3>
            {p.data_quality?.missing_fields.length ? <ul className="mt-1 flex flex-wrap gap-1">{p.data_quality.missing_fields.map((m) => <li key={m}><Badge tone="outline">{m}</Badge></li>)}</ul> : <p>—</p>}
            {p.validation_issues.length ? (<><h3 className="mt-3 font-semibold text-navy">{d.project.validationIssues}</h3><ul className="mt-1 space-y-1">{p.validation_issues.map((v, i) => <li key={i}><Badge tone={v.severity === "error" ? "danger" : "gold"}>{v.severity}</Badge> {v.rule}: {v.message} <span className="text-xs text-muted">({v.status})</span></li>)}</ul></>) : null}
          </div>
        </CardBody>
      </Card>

      <Card>
        <CardHeader title={d.project.fieldObservations} />
        {p.observations ? (
          <Table caption={d.project.fieldObservations}>
            <THead><TR><TH>{d.project.field}</TH><TH>{d.project.sourceField}</TH><TH>{d.common.value}</TH><TH>{d.project.reportingDate}</TH><TH>{d.common.dataNature}</TH><TH>{d.common.verification}</TH><TH>{d.common.source}</TH></TR></THead>
            <TBody>{p.observations.map((o, i) => (
              <TR key={i}><TD className="font-mono text-xs">{o.field}</TD><TD className="font-mono text-xs"><V value={o.source_field} /></TD>
                <TD className="max-w-md text-xs break-anywhere">{o.value_numeric !== null ? <Amount value={o.value_numeric} currency={o.currency} /> : o.value_date ? <DateV value={o.value_date} /> : <V value={o.value_text?.slice(0, 300)} />}</TD>
                <TD><DateV value={o.reporting_date} /></TD><TD><NatureBadge value={o.data_nature} /></TD><TD><VerificationBadge value={o.verification_status} /></TD><TD><SrcLink id={o.source_record_id} /></TD></TR>))}
            </TBody>
          </Table>
        ) : <CardBody><Alert tone="info">{p.observations_note} <Link className="link" href="/pricing">{d.common.seePricing}</Link></Alert></CardBody>}
      </Card>
      <CoverageNotice d={d} />
    </div>
  );
}
