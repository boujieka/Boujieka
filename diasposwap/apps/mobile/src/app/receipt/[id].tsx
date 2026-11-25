import { View } from 'react-native';
import { useLocalSearchParams } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { Card, H1, Mark, Muted, Row, Screen } from '@/components/ui';
import { countryName, useApp } from '@/lib/store';
import { fmt, fmtDate, fmtRate } from '@/lib/format';

export default function Receipt() {
  const { t } = useTranslation();
  const { id } = useLocalSearchParams<{ id: string }>();
  const { sim, locale, userId } = useApp();
  const o = sim.orders.get(id ?? '');
  if (!o || o.userId !== userId) return <Screen><Muted>—</Muted></Screen>;
  const v = sim.userView(o.id);
  const q = sim.quotes.get(o.quoteId);
  const ben = sim.beneficiaries.get(o.beneficiaryId);
  return (
    <Screen>
      <View className="items-center"><Mark size={56} /></View>
      <H1>{t('receipt.title')}</H1>
      <Card>
        <Row label={t('receipt.order')} value={o.id} />
        <Row label={t('receipt.date')} value={fmtDate(o.createdAt, locale)} />
        <Row label={t('send.from')} value={countryName(o.fromCountry, locale)} />
        <Row label={t('send.beneficiary')} value={`${ben?.fullName ?? ''} (${countryName(o.toCountry, locale)})`} />
        <Row label={t('send.amount')} value={fmt(o.principal, o.sendCurrency, locale)} />
        <Row label={t('send.fee')} value={fmt(o.fee - o.refundedFee, o.sendCurrency, locale)} />
        {q ? <Row label={t('send.rate')} value={fmtRate(q.rate, locale)} /> : null}
        <Row label={t('tracking.toReceive')} value={fmt(v.beneficiaryReceived, o.receiveCurrency, locale)} strong />
        {v.refunded > 0n ? <Row label={t('tracking.refunded')} value={fmt(v.refunded, o.sendCurrency, locale)} /> : null}
        <Row label={t('receipt.status')} value={t(`states.${o.state}`)} />
      </Card>
      <Muted className="text-xs">{t('receipt.disclaimer')}</Muted>
    </Screen>
  );
}
