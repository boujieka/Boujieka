import { router } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { COUNTRIES } from '@diasposwap/shared-types';
import { Card, H1, ListItem, Muted, Screen, StatePill } from '@/components/ui';
import { useApp, useSimVersion, userOrders } from '@/lib/store';
import { fmt, fmtDate } from '@/lib/format';

export default function History() {
  const { t } = useTranslation();
  const { sim, userId, locale } = useApp();
  useSimVersion();
  const orders = userId ? userOrders(sim, userId) : [];
  return (
    <Screen>
      <H1>{t('history.title')}</H1>
      <Card>
        {orders.length === 0 ? <Muted>{t('history.empty')}</Muted> : orders.map((o) => (
          <ListItem key={o.id} title={`${COUNTRIES[o.fromCountry].flag} → ${COUNTRIES[o.toCountry].flag}  ${fmt(o.principal, o.sendCurrency, locale)}`}
            subtitle={`${fmtDate(o.createdAt, locale)} · ${o.id}`} right={<StatePill state={o.state} />} onPress={() => router.push(`/transfer/${o.id}`)} />
        ))}
      </Card>
    </Screen>
  );
}
