import { Text, TextInput, View } from 'react-native';
import { Controller, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { router } from 'expo-router';
import { useTranslation } from 'react-i18next';
import { type CountryCode, COUNTRIES, INITIAL_CORRIDORS } from '@diasposwap/shared-types';
import { Button, Card, Chip, H1, H2, ListItem, Muted, Screen } from '@/components/ui';
import { countryName, useApp, useCurrentUser } from '@/lib/store';

const schema = z.object({
  fullName: z.string().trim().min(3),
  country: z.string().length(2),
  accountRef: z.string().trim().min(4).max(40),
});
type Form = z.infer<typeof schema>;

export default function Beneficiaries() {
  const { t } = useTranslation();
  const { sim, locale, addBeneficiary } = useApp();
  const user = useCurrentUser();
  const from = user?.profile.country ?? 'FR';
  const countries = INITIAL_CORRIDORS.filter((c) => c.a === from || c.b === from).map((c) => (c.a === from ? c.b : c.a));
  const { control, handleSubmit, reset, formState: { errors } } = useForm<Form>({ resolver: zodResolver(schema), defaultValues: { fullName: '', country: countries[0] ?? 'CM', accountRef: '' } });
  const mine = [...sim.beneficiaries.values()].filter((b) => b.ownerId === user?.profile.userId);
  const input = 'rounded-xl border border-ivory-300 dark:border-petrol-600 bg-white dark:bg-petrol-700 px-4 py-3 text-base text-anthracite dark:text-ivory';
  const submit = handleSubmit((f) => { addBeneficiary({ fullName: f.fullName, country: f.country as CountryCode, accountRef: f.accountRef }); reset(); });
  return (
    <Screen>
      <H1>{t('beneficiaries.title')}</H1>
      <Card>
        {mine.map((b) => <ListItem key={b.id} title={`${COUNTRIES[b.country].flag} ${b.fullName}`} subtitle={`${b.accountRef}${b.relationship ? ` · ${b.relationship}` : ''}`} />)}
      </Card>
      <Card>
        <H2>{t('beneficiaries.add')}</H2>
        <Controller control={control} name="fullName" render={({ field }) => <TextInput className={input} placeholder={t('beneficiaries.name')} placeholderTextColor="#6B7878" accessibilityLabel={t('beneficiaries.name')} value={field.value} onChangeText={field.onChange} />} />
        {errors.fullName ? <Text className="text-sm text-danger">{t('beneficiaries.nameError')}</Text> : null}
        <Text className="text-sm text-anthracite-500 dark:text-ivory-300">{t('beneficiaries.country')}</Text>
        <Controller control={control} name="country" render={({ field }) => (
          <View className="flex-row flex-wrap gap-2">{countries.map((c) => <Chip key={c} label={`${COUNTRIES[c].flag} ${countryName(c, locale)}`} selected={field.value === c} onPress={() => field.onChange(c)} />)}</View>
        )} />
        <Controller control={control} name="accountRef" render={({ field }) => <TextInput className={input} placeholder={t('beneficiaries.account')} placeholderTextColor="#6B7878" accessibilityLabel={t('beneficiaries.account')} value={field.value} onChangeText={field.onChange} />} />
        {errors.accountRef ? <Text className="text-sm text-danger">{t('beneficiaries.accountError')}</Text> : null}
        <Muted className="text-xs">{t('beneficiaries.verifiedNote')}</Muted>
        <Button title={t('beneficiaries.add')} onPress={() => void submit()} />
      </Card>
      <Button variant="secondary" title={t('common.back')} onPress={() => router.back()} />
    </Screen>
  );
}
