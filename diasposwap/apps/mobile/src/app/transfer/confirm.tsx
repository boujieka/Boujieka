import { useRef, useState } from 'react';
import { Text } from 'react-native';
import { router, useLocalSearchParams } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { COUNTRIES } from '@diasposwap/shared-types';
import { SimulationError } from '@diasposwap/settlement-engine';
import { Button, Card, H1, Muted, Row, Screen } from '@/components/ui';
import { countryName, useApp } from '@/lib/store';
import { fmt, fmtDate, fmtRate } from '@/lib/format';

export default function Confirm() {
  const { t } = useTranslation();
  const { quoteId, beneficiaryId, partial } = useLocalSearchParams<{ quoteId: string; beneficiaryId: string; partial: string }>();
  const { sim, locale, placeOrder } = useApp();
  const [error, setError] = useState<string | null>(null);
  // one idempotency key per confirmation screen: a double tap cannot create two orders
  const idem = useRef(`ui:${quoteId}:${Date.now()}`).current;
  const q = sim.quotes.get(quoteId ?? '');
  const ben = sim.beneficiaries.get(beneficiaryId ?? '');
  if (!q || !ben) return <Screen><Muted>—</Muted></Screen>;

  const pay = () => {
    try {
      const o = placeOrder(q, ben.id, partial === '1', idem);
      router.replace(`/transfer/${o.id}`);
    } catch (e) {
      setError(e instanceof SimulationError ? e.message : String(e));
    }
  };

  return (
    <Screen>
      <H1>{t('confirm.title')}</H1>
      <Card>
        <Row label={t('send.from')} value={`${COUNTRIES[q.from].flag} ${countryName(q.from, locale)}`} />
        <Row label={t('send.to')} value={`${COUNTRIES[q.to].flag} ${ben.fullName}`} />
        <Row label={t('send.amount')} value={fmt(q.principal, q.sendCurrency, locale)} />
        <Row label={t('send.fee')} value={fmt(q.fee, q.sendCurrency, locale)} />
        <Row label={t('send.total')} value={fmt(q.total, q.sendCurrency, locale)} strong />
        <Row label={t('send.rate')} value={fmtRate(q.rate, locale)} />
        <Row label={t('send.receive')} value={fmt(q.estimatedReceive, q.receiveCurrency, locale)} strong />
        <Row label={t('send.partial')} value={partial === '1' ? '✓' : '✗'} />
      </Card>
      <Muted>{t('confirm.validity', { time: fmtDate(q.expiresAt, locale) })}</Muted>
      <Muted>{t('confirm.delay')}</Muted>
      {error ? <Text className="text-sm text-danger">{error}</Text> : null}
      <Button testID="pay" title={t('confirm.pay', { amount: fmt(q.total, q.sendCurrency, locale) })} onPress={pay} />
      <Button variant="secondary" title={t('common.back')} onPress={() => router.back()} />
    </Screen>
  );
}
