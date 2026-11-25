import { router } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { analyseLiquidity } from '@diasposwap/liquidity';
import { simulateMultilateral } from '@diasposwap/matching-engine';
import { Button, Card, H1, H2, Muted, Row, Screen } from '@/components/ui';
import { useApp, useSimVersion } from '@/lib/store';
import { fmt } from '@/lib/format';

/** Read-only liquidity view of the demo community (operator-style screen, simulation data). */
export default function Liquidity() {
  const { t } = useTranslation();
  const { sim, locale } = useApp();
  useSimVersion();
  const orders = [...sim.orders.values()];
  const liq = analyseLiquidity({ orders, rates: sim.rates(), now: new Date() });
  const multi = simulateMultilateral(orders, sim.rates(), { mode: 'simulation' });
  return (
    <Screen>
      <H1>{t('profile.liquidity')}</H1>
      <Muted>Estimations, avec incertitude. Les cycles multilatéraux sont une simulation et ne sont pas autorisés en production.</Muted>
      <Card>
        <H2>Compensation multilatérale (simulation)</H2>
        <Row label="Volume brut en attente" value={fmt(multi.grossBefore, 'EUR', locale)} />
        <Row label="Après compensation bilatérale" value={fmt(multi.grossAfterBilateral, 'EUR', locale)} />
        <Row label="Après cycles multilatéraux" value={fmt(multi.grossAfterMultilateral, 'EUR', locale)} strong />
        {multi.cycles.slice(0, 3).map((c, i) => <Muted key={i} className="text-xs">{c.path.join(' → ')} : {fmt(c.eurCents, 'EUR', locale)}</Muted>)}
      </Card>
      {liq.map((c) => (
        <Card key={c.corridorId}>
          <H2>{c.corridorId}</H2>
          <Row label="En attente A→B / B→A" value={`${fmt(c.pendingAB, 'EUR', locale)} / ${fmt(c.pendingBA, 'EUR', locale)}`} />
          <Row label="Besoin de préfinancement" value={fmt(c.prefundingNeed, 'EUR', locale)} />
          <Row label="Déséquilibre" value={`${(c.imbalanceBps / 100).toFixed(0)} %`} />
          <Row label="Résorption estimée" value={c.estimatedClearDays === null ? 'inconnue' : `~${c.estimatedClearDays} j`} />
          <Row label="Incertitude" value={`${c.uncertainty} (${c.observations} obs.)`} />
        </Card>
      ))}
      <Button variant="secondary" title={t('common.back')} onPress={() => router.back()} />
    </Screen>
  );
}
