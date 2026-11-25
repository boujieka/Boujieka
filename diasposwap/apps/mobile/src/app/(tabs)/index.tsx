import { Pressable, Text, View } from 'react-native';
import { router } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { type CurrencyCode, COUNTRIES, INITIAL_CORRIDORS, crossRate } from '@diasposwap/shared-types';
import { analyseLiquidity } from '@diasposwap/liquidity';
import { Button, Card, H1, H2, ListItem, Logo, Muted, Progress, Row, Screen, StatePill } from '@/components/ui';
import { countryName, useApp, useCurrentUser, userOrders } from '@/lib/store';
import { fmt, fmtRate } from '@/lib/format';

const ACTIVE = ['PENDING_VERIFICATION', 'PENDING_FUNDING', 'FUNDED', 'QUEUED', 'PARTIALLY_MATCHED', 'MATCHED', 'SETTLEMENT_PENDING', 'REFUND_PENDING', 'DISPUTED'];

export default function Dashboard() {
  const { t } = useTranslation();
  const { sim, locale } = useApp();
  const user = useCurrentUser();
  if (!user) return null;
  const me = user.profile;
  const cur = COUNTRIES[me.country].currency;
  const orders = userOrders(sim, me.userId);
  const funded = orders.filter((o) => o.collectionRef && o.state !== 'FAILED');
  const sent = funded.reduce((s, o) => s + (o.principal - o.refundedPrincipal), 0n);
  const fees = funded.reduce((s, o) => s + (o.fee - o.refundedFee), 0n);
  const received = new Map<CurrencyCode, bigint>();
  for (const p of sim.payouts.values()) {
    const o = sim.orders.get(p.beneficiaryOrderId);
    if (o?.userId === me.userId && p.status === 'SUCCEEDED') received.set(p.currency, (received.get(p.currency) ?? 0n) + p.amount);
  }
  const active = orders.filter((o) => ACTIVE.includes(o.state));
  const done = orders.filter((o) => o.state === 'SETTLED' || o.state === 'REFUNDED');
  const myCorridors = INITIAL_CORRIDORS.filter((c) => c.a === me.country || c.b === me.country);
  const liq = analyseLiquidity({ orders: [...sim.orders.values()], rates: sim.rates(), now: new Date(), corridors: myCorridors });

  return (
    <Screen>
      <View className="flex-row items-center justify-between"><Logo height={30} /><Text onPress={() => router.push('/notifications')} accessibilityRole="button" className="text-2xl text-petrol dark:text-ivory">🔔</Text></View>
      <H1>{t('home.hello', { name: me.fullName.split(' ')[0] })}</H1>
      <Button testID="send-money" title={t('home.send')} onPress={() => router.push('/(tabs)/send')} />

      <Card>
        <Row label={t('home.sent')} value={fmt(sent, cur, locale)} strong />
        <Row label={t('home.received')} value={[...received].map(([c, v]) => fmt(v, c, locale)).join(' · ') || '—'} />
        <Row label={t('home.fees')} value={fmt(fees, cur, locale)} />
        <Row label={t('home.savings')} value="—" />
        <Muted className="text-xs">{t('home.savingsNA')}</Muted>
        <View className="flex-row gap-4 pt-1">
          <Text className="text-sm text-anthracite dark:text-ivory">{t('home.inProgress')}: <Text className="font-bold">{active.length}</Text></Text>
          <Text className="text-sm text-anthracite dark:text-ivory">{t('home.done')}: <Text className="font-bold">{done.length}</Text></Text>
        </View>
      </Card>

      {active.length > 0 && (
        <Card>
          <H2>{t('home.inProgress')}</H2>
          {active.slice(0, 4).map((o) => {
            const ratio = Number(((o.principal - o.remaining) * 1000n) / o.principal) / 1000;
            return (
              <Pressable key={o.id} accessibilityRole="button" className="gap-1.5 py-1" onPress={() => router.push(`/transfer/${o.id}`)}>
                <View className="flex-row justify-between items-center">
                  <Text className="text-sm text-anthracite dark:text-ivory">{COUNTRIES[o.fromCountry].flag} → {COUNTRIES[o.toCountry].flag}  {fmt(o.principal, o.sendCurrency, locale)}</Text>
                  <StatePill state={o.state} />
                </View>
                <Progress ratio={ratio} />
              </Pressable>
            );
          })}
        </Card>
      )}

      <Card>
        <H2>{t('home.corridors')}</H2>
        {liq.map((c) => {
          const [a, b] = c.corridorId.split('-') as [keyof typeof COUNTRIES, keyof typeof COUNTRIES];
          const status = c.observations < 5 ? t('home.unknown') : c.imbalanceBps < 3000 ? t('home.balanced') : `${t('home.waiting')} · ${c.dominantDirection?.replace('>', ' → ')}`;
          return <ListItem key={c.corridorId} title={`${COUNTRIES[a].flag} ${countryName(a, locale)} ⇄ ${COUNTRIES[b].flag} ${countryName(b, locale)}`} subtitle={`${status} · ${t(`home.uncertainty.${c.uncertainty}`)}`} />;
        })}
      </Card>

      <Card>
        <H2>{t('home.rates')}</H2>
        {[...new Set(myCorridors.map((c) => COUNTRIES[c.a === me.country ? c.b : c.a].currency))].filter((c) => c !== cur).map((c) => {
          const r = crossRate(cur, c, sim.rates());
          return <Row key={c} label={fmtRate(r, locale)} value={r.source === 'OFFICIAL_PEG' ? t('send.peg') : t('send.simulatedRate')} />;
        })}
      </Card>

      <Card>
        <H2>{t('home.recent')}</H2>
        {orders.length === 0 ? <Muted>{t('home.none')}</Muted> : orders.slice(0, 3).map((o) => (
          <ListItem key={o.id} title={`${COUNTRIES[o.toCountry].flag} ${fmt(o.principal, o.sendCurrency, locale)}`} subtitle={o.id} right={<StatePill state={o.state} />} onPress={() => router.push(`/transfer/${o.id}`)} />
        ))}
      </Card>
    </Screen>
  );
}
