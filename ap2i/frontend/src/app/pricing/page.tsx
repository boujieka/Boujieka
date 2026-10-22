import { PageHeader } from "@/components/page-header";
import { SubscribeButton } from "@/components/subscribe-button";
import { ErrorState } from "@/components/states";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Table, TBody, TD, TH, THead, TR } from "@/components/ui/table";
import { getI18n } from "@/i18n/server";
import { label } from "@/i18n";
import { apiGet, getMe } from "@/lib/api";
import { fmtAmount } from "@/lib/format";

interface Plan { code: string; name_en: string; name_fr: string; price_amount: string | null; price_currency: string | null; billing_period: string | null; features: string[]; price_note: string | null }

export const metadata = { title: "Pricing" };

export default async function PricingPage() {
  const { d, locale } = await getI18n();
  const [plans, me] = await Promise.all([apiGet<Plan[]>("/plans"), getMe()]);
  if (!plans.ok) return <ErrorState d={d} status={plans.status} message={plans.error} />;
  const features = [...new Set(plans.data.flatMap((p) => p.features))];
  const price = (p: Plan) => (p.price_amount === null ? d.pricing.onRequest : `${fmtAmount(p.price_amount, p.price_currency, locale)} ${p.billing_period === "month" ? d.pricing.perMonth : p.billing_period === "year" ? d.pricing.perYear : ""}`);
  return (
    <div className="space-y-6">
      <PageHeader title={d.pricing.title} subtitle={d.pricing.subtitle} />
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {plans.data.map((p) => (
          <Card key={p.code} className="flex flex-col">
            <CardHeader title={locale === "fr" ? p.name_fr : p.name_en} description={<span className="text-lg font-bold text-navy">{price(p)}</span>} />
            <CardBody className="flex flex-1 flex-col justify-between gap-4">
              <ul className="space-y-1 text-sm">{p.features.map((f) => <li key={f}>✓ {label(d.pricing.feature, f)}</li>)}</ul>
              {p.code !== "public" ? <SubscribeButton plan={p.code} loggedIn={!!me} /> : null}
            </CardBody>
          </Card>
        ))}
      </div>
      <Card>
        <CardHeader title={d.pricing.features} />
        <Table caption={d.pricing.features}>
          <THead><TR><TH>{d.pricing.features}</TH>{plans.data.map((p) => <TH key={p.code} className="text-center">{locale === "fr" ? p.name_fr : p.name_en}</TH>)}</TR></THead>
          <TBody>{features.map((f) => (
            <TR key={f}><TD>{label(d.pricing.feature, f)}</TD>{plans.data.map((p) => <TD key={p.code} className="text-center">{p.features.includes(f) ? <span aria-label={d.common.yes}>✓</span> : <span aria-label={d.common.no} className="text-muted">—</span>}</TD>)}</TR>))}
          </TBody>
        </Table>
      </Card>
    </div>
  );
}
