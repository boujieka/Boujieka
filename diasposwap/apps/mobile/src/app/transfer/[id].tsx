import { Text, View } from 'react-native';
import { router, useLocalSearchParams } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { COUNTRIES } from '@diasposwap/shared-types';
import { Button, Card, H1, H2, Muted, Progress, Row, Screen, StatePill } from '@/components/ui';
import { useApp, useSimVersion } from '@/lib/store';
import { fmt, fmtDate } from '@/lib/format';

export default function Tracking() {
  const { t } = useTranslation();
  const { id } = useLocalSearchParams<{ id: string }>();
  const { sim, locale, userId, simulateCounterparty, runMatching, settle, cancel } = useApp();
  useSimVersion();
  const o = sim.orders.get(id ?? '');
  if (!o || o.userId !== userId) return <Screen><Muted>—</Muted></Screen>;
  const v = sim.userView(o.id); // user-safe view: no counterparty identity or account data
  const ben = sim.beneficiaries.get(o.beneficiaryId);
  const ratio = Number((v.matched * 1000n) / o.principal) / 1000;
  const searching = o.state === 'QUEUED' || o.state === 'PARTIALLY_MATCHED';

  return (
    <Screen>
      <H1>{t('tracking.title')}</H1>
      <Card>
        <View className="flex-row justify-between items-center">
          <Text className="text-lg font-semibold text-petrol dark:text-ivory">{COUNTRIES[o.fromCountry].flag} → {COUNTRIES[o.toCountry].flag} {ben?.fullName}</Text>
          <StatePill state={o.state} />
        </View>
        <Text testID="order-state" className="text-xs text-anthracite-500 dark:text-ivory-300">{o.id} · {o.state}</Text>
        <Row label={t('send.amount')} value={fmt(o.principal, o.sendCurrency, locale)} strong />
        <Row label={t('tracking.matched')} value={`${fmt(v.matched, o.sendCurrency, locale)} · ${t('tracking.matches', { count: v.matchCount })}`} />
        <Progress ratio={ratio} />
        <Row label={t('tracking.toReceive')} value={fmt(v.beneficiaryReceived, o.receiveCurrency, locale)} strong />
        {v.beneficiaryPending > 0n ? <Row label={t('tracking.pending')} value={fmt(v.beneficiaryPending, o.receiveCurrency, locale)} /> : null}
        {v.refunded > 0n ? <Row label={t('tracking.refunded')} value={fmt(v.refunded, o.sendCurrency, locale)} /> : null}
        {o.state === 'FAILED' ? <Text className="text-sm text-danger">{t('confirm.blocked')}</Text> : null}
        {o.state === 'PENDING_VERIFICATION' ? <Text className="text-sm text-gold-700">{t('confirm.review')}</Text> : null}
        <Muted className="text-xs">{t('tracking.privacy')}</Muted>
      </Card>

      <Card className="border-dashed border-gold">
        <H2>{t('tracking.demo')}</H2>
        {searching ? <>
          <Button testID="sim-counterparty" variant="secondary" title={t('tracking.counterparty')} onPress={() => simulateCounterparty(o.id, 1)} />
          <Button testID="sim-half" variant="secondary" title={t('tracking.half')} onPress={() => simulateCounterparty(o.id, 0.5)} />
          <Button testID="run-matching" title={t('tracking.runMatching')} onPress={() => runMatching()} />
        </> : null}
        {v.beneficiaryPending > 0n || o.state === 'REFUND_PENDING'
          ? <Button testID="settle" title={t('tracking.settle')} onPress={() => settle()} /> : null}
        {o.state === 'QUEUED' && o.remaining === o.principal
          ? <Button variant="ghost" title={t('tracking.cancel')} onPress={() => cancel(o.id)} /> : null}
        {['SETTLED', 'REFUNDED'].includes(o.state) ? <Button testID="receipt" variant="secondary" title={t('tracking.receipt')} onPress={() => router.push(`/receipt/${o.id}`)} /> : null}
      </Card>

      <Card>
        <H2>{t('tracking.timeline')}</H2>
        {v.history.map((h, i) => (
          <View key={i} className="flex-row gap-3 py-1">
            <View className="items-center"><View className={`w-3 h-3 rounded-full ${i === v.history.length - 1 ? 'bg-gold' : 'bg-emerald'}`} />{i < v.history.length - 1 ? <View className="w-0.5 flex-1 bg-ivory-300" /> : null}</View>
            <View className="flex-1 pb-2">
              <Text className="text-sm font-semibold text-anthracite dark:text-ivory">{t(`states.${h.to}`)}</Text>
              <Text className="text-xs text-anthracite-500 dark:text-ivory-300">{fmtDate(h.at, locale)}</Text>
            </View>
          </View>
        ))}
      </Card>
    </Screen>
  );
}
