"use client";

import { Chart } from "@/components/charts/echart";
import { toNumber } from "@/lib/format";
import { useI18n } from "./i18n-provider";

/** One chart per currency (amounts in different currencies are never on a shared, summed axis). */
export function ProjectFlowsChart({ flows, projectId }: { flows: { year: number; currency: string; flow: string; amount: string }[]; projectId: string }) {
  const { d } = useI18n();
  const currencies = [...new Set(flows.map((f) => f.currency))].sort();
  return (
    <div className="space-y-4">
      {currencies.map((cur) => {
        const rows = flows.filter((f) => f.currency === cur);
        const years = [...new Set(rows.map((r) => r.year))].sort();
        const kinds = [...new Set(rows.map((r) => r.flow))];
        const colors: Record<string, string> = { commitment: "#082B50", disbursement: "#087F5B", expenditure: "#D9A323" };
        return (
          <div key={cur}>
            <h4 className="text-sm font-semibold text-navy">{cur}</h4>
            <Chart ariaLabel={`${d.project.annualFlows} ${cur}`} categories={years.map(String)} unit={cur}
              links={years.map(() => `/projects/${projectId}#flows`)}
              series={kinds.map((k) => ({
                name: k === "commitment" ? d.explorer.flowCommitment : k === "disbursement" ? d.explorer.flowDisbursement : k === "expenditure" ? d.explorer.flowExpenditure : k,
                color: colors[k],
                data: years.map((y) => {
                  const r = rows.find((x) => x.year === y && x.flow === k);
                  return r ? toNumber(r.amount) : null;
                }),
              }))} height={240} />
          </div>
        );
      })}
    </div>
  );
}
