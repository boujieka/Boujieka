import { useMemo, useState } from 'react';
import { Switch, Text, TextInput, View } from 'react-native';
import { router } from 'expo-router';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import {
  type CountryCode, COUNTRIES, INITIAL_CORRIDORS, MoneyError, convertFloor, crossRate, divCeil, parseMajor,
} from '@diasposwap/shared-types';
import { Button, Card, Chip, H1, Muted, Row, Screen } from '@/components/ui';
import { countryName, useApp, useCurrentUser, useSimVersion } from '@/lib/store';
import { fmt, fmtRate } from '@/lib/format';

export default function Send() {
  const { t } = useTranslation();
  const { sim, locale } = useApp();
  useSimVersion();
  const user = useCurrentUser();
  const from = user?.profile.country ?? 'FR';
  const destinations = INITIAL_CORRIDORS.filter((c) => c.a === from || c.b === from).map((c) => (c.a === from ? c.b : c.a));
  const [to, setTo] = useState<CountryCode>(destinations[0] ?? 'CM');
  const [amount, setAmount] = useState('');
  const [partial, setPartial] = useState(true);
  const sendCur = COUNTRIES[from].currency;
  const recvCur = COUNTRIES[to].currency;
  const bens = [...sim.beneficiaries.values()].filter((b) => b.ownerId === user?.profile.userId && b.country === to);
  const [benId, setBenId] = useState<string | null>(null);
  const beneficiary = bens.find((b) => b.id === benId) ?? bens[0];

  // Reference rates are served through TanStack Query so a real API can replace the local simulator later.
  const rates = useQuery({ queryKey: ['rates'], queryFn: () => sim.rates(), staleTime: 60_000 });

  const preview = useMemo(() => {
    if (!rates.data || !amount) return null;
    try {
      const principal = parseMajor(amount, sendCur);
      if (principal <= 0n) return { error: t('send.invalid') };
      const rate = crossRate(sendCur, recvCur, rates.data);
      const fee = divCeil(principal * 75n, 10_000n);
      return { principal, fee, total: principal + fee, rate, receive: convertFloor(principal, rate) };
    } catch (e) {
      return { error: e instanceof MoneyError ? t('send.invalid') : String(e) };
    }
  }, [amount, rates.data, sendCur, recvCur, t]);

  const canReview = preview && !('error' in preview) && beneficiary;
  const review = () => {
    if (!user || !preview || 'error' in preview || !beneficiary) return;
    const q = sim.quote(user.profile.userId, from, to, preview.principal);
    router.push({ pathname: '/transfer/confirm', params: { quoteId: q.id, beneficiaryId: beneficiary.id, partial: partial ? '1' : '0' } });
  };

  return (
    <Screen>
      <H1>{t('send.title')}</H1>
      <Card>
        <Row label={t('send.from')} value={`${COUNTRIES[from].flag} ${countryName(from, locale)} (${sendCur})`} />
        <Text className="text-sm text-anthracite-500 dark:text-ivory-300">{t('send.to')}</Text>
        <View className="flex-row flex-wrap gap-2">
          {destinations.map((d) => <Chip key={d} label={`${COUNTRIES[d].flag} ${countryName(d, locale)}`} selected={d === to} onPress={() => { setTo(d); setBenId(null); }} />)}
        </View>
      </Card>

      <Card>
        <Text className="text-sm text-anthracite-500 dark:text-ivory-300">{t('send.amount')} ({sendCur})</Text>
        <TextInput testID="amount" value={amount} onChangeText={setAmount} keyboardType="decimal-pad" placeholder="0" placeholderTextColor="#6B7878"
          accessibilityLabel={t('send.amount')} className="text-4xl font-bold text-petrol dark:text-ivory py-2" />
        {preview && 'error' in preview ? <Text className="text-sm text-danger">{preview.error}</Text> : null}
        {preview && !('error' in preview) ? (
          <View className="gap-2 pt-2 border-t border-ivory-200 dark:border-petrol-600">
            <Row label={t('send.fee')} value={fmt(preview.fee, sendCur, locale)} />
            <Row label={t('send.total')} value={fmt(preview.total, sendCur, locale)} strong />
            <Row label={t('send.rate')} value={fmtRate(preview.rate, locale)} />
            <Muted className="text-xs">{preview.rate.source === 'OFFICIAL_PEG' ? t('send.peg') : t('send.simulatedRate')}</Muted>
            <Row label={t('send.receive')} value={fmt(preview.receive, recvCur, locale)} strong />
          </View>
        ) : null}
      </Card>

      <Card>
        <Text className="text-sm text-anthracite-500 dark:text-ivory-300">{t('send.beneficiary')}</Text>
        {bens.length === 0 ? <Muted>{t('send.noBeneficiary')}</Muted> : (
          <View className="flex-row flex-wrap gap-2">
            {bens.map((b) => <Chip key={b.id} label={b.fullName} selected={b.id === beneficiary?.id} onPress={() => setBenId(b.id)} />)}
          </View>
        )}
        <Button variant="ghost" title={`+ ${t('send.addBeneficiary')}`} onPress={() => router.push('/beneficiaries')} />
      </Card>

      <Card>
        <View className="flex-row items-center justify-between">
          <Text className="text-base text-anthracite dark:text-ivory flex-1">{t('send.partial')}</Text>
          <Switch value={partial} onValueChange={setPartial} accessibilityLabel={t('send.partial')} trackColor={{ true: '#087F6D', false: '#E2DCCB' }} />
        </View>
        <Muted className="text-xs">{t('send.partialHelp')}</Muted>
      </Card>

      <Button testID="review" title={t('send.review')} disabled={!canReview} onPress={review} />
    </Screen>
  );
}
