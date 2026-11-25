import { router } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { Button, Card, H1, ListItem, Muted, Screen } from '@/components/ui';
import { useApp, useSimVersion } from '@/lib/store';
import { fmtDate } from '@/lib/format';

/** In-app notification centre, derived from the audit log. Push notifications need an EAS project (not configured). */
export default function Notifications() {
  const { t } = useTranslation();
  const { sim, userId, locale } = useApp();
  useSimVersion();
  const mine = new Set([...sim.orders.values()].filter((o) => o.userId === userId).map((o) => o.id));
  const items = sim.audit.filter((a) => mine.has(a.orderId)).slice(-40).reverse();
  return (
    <Screen>
      <H1>{t('notifications.title')}</H1>
      <Card>
        {items.length === 0 ? <Muted>{t('notifications.empty')}</Muted> : items.map((a, i) => (
          <ListItem key={i} title={`${a.orderId} · ${t(`states.${a.to}`)}`} subtitle={fmtDate(a.at, locale)} onPress={() => router.push(`/transfer/${a.orderId}`)} />
        ))}
      </Card>
      <Button variant="secondary" title={t('common.back')} onPress={() => router.back()} />
    </Screen>
  );
}
