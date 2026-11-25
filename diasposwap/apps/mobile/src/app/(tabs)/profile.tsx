import { router } from 'expo-router';
import { View } from 'react-native';
import { useTranslation } from 'react-i18next';
import i18n from '@/i18n';
import { COUNTRIES } from '@diasposwap/shared-types';
import { Button, Card, Chip, H1, H2, ListItem, Muted, Row, Screen } from '@/components/ui';
import { countryName, useApp, useCurrentUser } from '@/lib/store';

export default function Profile() {
  const { t } = useTranslation();
  const { locale, setLocale, logout } = useApp();
  const user = useCurrentUser();
  if (!user) return null;
  const p = user.profile;
  const soon = <Muted className="text-xs">{t('common.soon')}</Muted>;
  return (
    <Screen>
      <H1>{t('profile.title')}</H1>
      <Card>
        <H2>{COUNTRIES[p.country].flag} {p.fullName}</H2>
        <Row label={t('login.residence')} value={countryName(p.country, locale)} />
        <Row label={t('profile.kyc')} value={`${p.kycLevel} (${t('profile.simulated')})`} />
        <Row label="PEP" value={p.pep ? t('profile.pepYes') : t('profile.pepNo')} />
      </Card>
      <Card>
        <H2>{t('profile.language')}</H2>
        <View className="flex-row gap-2">
          {(['fr', 'en'] as const).map((l) => <Chip key={l} label={l === 'fr' ? 'Français' : 'English'} selected={locale === l} onPress={() => { setLocale(l); void i18n.changeLanguage(l); }} />)}
        </View>
      </Card>
      <Card>
        <ListItem title={t('profile.beneficiaries')} onPress={() => router.push('/beneficiaries')} right={<Muted>›</Muted>} />
        <ListItem title={t('profile.notifications')} onPress={() => router.push('/notifications')} right={<Muted>›</Muted>} />
        <ListItem title={t('profile.liquidity')} onPress={() => router.push('/liquidity')} right={<Muted>›</Muted>} />
        <ListItem title={t('profile.security')} subtitle={t('profile.securityBody')} />
        <ListItem title={t('profile.communities')} right={soon} />
        <ListItem title={t('profile.referral')} right={soon} />
        <ListItem title={t('profile.disputes')} right={soon} />
        <ListItem title={t('profile.help')} right={soon} />
      </Card>
      <Button variant="secondary" title={t('profile.logout')} onPress={() => { void logout().then(() => router.replace('/login')); }} />
    </Screen>
  );
}
