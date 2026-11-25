import { useState } from 'react';
import { Text, View } from 'react-native';
import { router } from 'expo-router';
import { useTranslation } from 'react-i18next';
import i18n from '@/i18n';
import { Button, Chip, Logo, Screen } from '@/components/ui';
import { useApp } from '@/lib/store';

export default function Onboarding() {
  const { t } = useTranslation();
  const [step, setStep] = useState(0);
  const { setOnboarded, setLocale, locale } = useApp();
  const slides = [['s1t', 's1b'], ['s2t', 's2b'], ['s3t', 's3b']] as const;
  const [title, body] = slides[step] ?? slides[0];
  const changeLang = (l: 'fr' | 'en') => { setLocale(l); void i18n.changeLanguage(l); };
  return (
    <Screen>
      <View className="items-center py-6"><Logo height={44} /></View>
      <Text className="text-center text-sm italic text-anthracite-500 dark:text-ivory-300">{t('slogan')}</Text>
      <View className="rounded-2xl bg-petrol p-6 gap-3 min-h-[200px] justify-center">
        <Text className="text-2xl font-bold text-ivory">{t(`onboarding.${title}`)}</Text>
        <Text className="text-base text-ivory-200 leading-6">{t(`onboarding.${body}`)}</Text>
      </View>
      <View className="flex-row justify-center gap-2" accessibilityLabel={`${step + 1}/3`}>
        {slides.map((_, i) => <View key={i} className={`h-2 rounded-full ${i === step ? 'w-6 bg-gold' : 'w-2 bg-ivory-300'}`} />)}
      </View>
      <View className="gap-2">
        <Text className="text-sm font-semibold text-petrol dark:text-ivory">{t('onboarding.language')}</Text>
        <View className="flex-row gap-2">
          <Chip label="Français" selected={locale === 'fr'} onPress={() => changeLang('fr')} />
          <Chip label="English" selected={locale === 'en'} onPress={() => changeLang('en')} />
        </View>
      </View>
      {step < 2
        ? <Button title={t('common.continue')} onPress={() => setStep(step + 1)} />
        : <Button testID="start" title={t('onboarding.start')} onPress={() => { setOnboarded(); router.replace('/login'); }} />}
    </Screen>
  );
}
