import Link from "next/link";

import { Field, VerificationBadge } from "@/components/provenance";
import { TBody, TD, TH, THead, TR, Table } from "@/components/ui/table";
import { Card } from "@/components/ui/card";
import { api } from "@/lib/api";

export default async function CountriesPage() {
  const countries = await api.countries();
  return (
    <div className="space-y-4">
      <h1 className="text-lg font-semibold">Countries</h1>
      <Card>
        <Table>
          <caption className="sr-only">Monitored countries</caption>
          <THead>
            <tr>
              <TH>Country</TH>
              <TH>ISO</TH>
              <TH>Currency</TH>
              <TH>Monetary zone</TH>
              <TH>Central bank</TH>
              <TH>Debt management</TH>
              <TH>Reference data</TH>
            </tr>
          </THead>
          <TBody>
            {countries.map((c) => (
              <TR key={c.iso3}>
                <TD>
                  <Link href={`/countries/${c.iso3}`} className="font-medium text-accent hover:underline">
                    {c.name}
                  </Link>
                </TD>
                <TD className="num">{c.iso3}</TD>
                <TD>{c.currency}</TD>
                <TD>{c.monetary_zone === "NONE" ? "—" : c.monetary_zone}</TD>
                <TD className="whitespace-normal">
                  <Field value={c.central_bank} status={c.field_status.central_bank} />
                </TD>
                <TD className="whitespace-normal">
                  <Field value={c.debt_management_office} status={c.field_status.debt_management_office} />
                </TD>
                <TD>
                  <VerificationBadge status={c.provenance.verification_status} />
                </TD>
              </TR>
            ))}
          </TBody>
        </Table>
      </Card>
      <p className="text-xs text-muted">
        Country reference data is <strong>unverified</strong> seed data and must be confirmed against official sources.
      </p>
    </div>
  );
}
