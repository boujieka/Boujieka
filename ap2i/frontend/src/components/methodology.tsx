import { Card, CardBody, CardHeader } from "@/components/ui/card";
import type { Dict } from "@/i18n";

export interface Methodology { data_principles: string[]; portfolio: string | null; exchange_rates: string | null; entity_resolution: string | null; early_warning: string | null; coverage: string }

export function MethodologySections({ d, m }: { d: Dict; m: Methodology }) {
  const docs: [string, string | null][] = [[d.about.portfolio, m.portfolio], [d.about.exchangeRates, m.exchange_rates], [d.about.entityResolution, m.entity_resolution], [d.about.earlyWarning, m.early_warning]];
  return (
    <div className="space-y-4">
      {docs.map(([t, txt]) => (
        <Card key={t}>
          <CardHeader title={t} as="h3" />
          <CardBody>{txt ? <pre className="whitespace-pre-wrap break-anywhere font-sans text-sm leading-relaxed">{txt.trim()}</pre> : <p className="text-sm italic text-muted">{d.common.na}</p>}</CardBody>
        </Card>
      ))}
    </div>
  );
}
