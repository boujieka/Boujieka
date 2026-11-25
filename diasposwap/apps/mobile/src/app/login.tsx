import { useState } from 'react';
import { Pressable, Text, TextInput, View } from 'react-native';
import { router } from 'expo-router';
import { Controller, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useTranslation } from 'react-i18next';
import { COUNTRIES } from '@diasposwap/shared-types';
import { Button, Card, H1, Mark, Muted, Screen } from '@/components/ui';
import { DEMO_PROFILES, countryName, useApp } from '@/lib/store';

const schema = z.object({ pin: z.string().regex(/^\d{4}$/) });

/** Demo sign-in. Real authentication (password + MFA, device binding) is backend work, see docs/SECURITY.md. */
export default function Login() {
  const { t } = useTranslation();
  const { login, locale } = useApp();
  const [selected, setSelected] = useState(DEMO_PROFILES[0]?.userId ?? '');
  const { control, handleSubmit, formState: { errors } } = useForm<z.infer<typeof schema>>({ resolver: zodResolver(schema), defaultValues: { pin: '' } });
  const submit = handleSubmit(async () => { await login(selected); router.replace('/(tabs)'); });
  return (
    <Screen>
      <View className="items-center pt-4"><Mark size={72} /></View>
      <H1>{t('login.title')}</H1>
      <Muted>{t('login.subtitle')}</Muted>
      <View className="gap-2">
        {DEMO_PROFILES.map((p) => (
          <Pressable key={p.userId} testID={`profile-${p.userId}`} accessibilityRole="radio" accessibilityState={{ checked: selected === p.userId }} onPress={() => setSelected(p.userId)}>
            <Card className={selected === p.userId ? 'border-emerald border-2' : ''}>
              <Text className="text-base font-semibold text-petrol dark:text-ivory">{COUNTRIES[p.country].flag} {p.name}</Text>
              <Muted>{t('login.residence')} {countryName(p.country, locale)} · {p.note} · KYC {p.kyc}</Muted>
            </Card>
          </Pressable>
        ))}
      </View>
      <Text className="text-sm font-semibold text-petrol dark:text-ivory">{t('login.pin')}</Text>
      <Controller control={control} name="pin" render={({ field }) => (
        <TextInput testID="pin" value={field.value} onChangeText={field.onChange} keyboardType="number-pad" maxLength={4} secureTextEntry
          accessibilityLabel={t('login.pin')} placeholder="••••" placeholderTextColor="#6B7878"
          className="rounded-xl border border-ivory-300 dark:border-petrol-600 bg-white dark:bg-petrol-700 px-4 py-3 text-lg text-anthracite dark:text-ivory" />
      )} />
      {errors.pin ? <Text className="text-sm text-danger">{t('login.pinError')}</Text> : null}
      <Button testID="login" title={t('login.submit')} onPress={() => void submit()} />
    </Screen>
  );
}
