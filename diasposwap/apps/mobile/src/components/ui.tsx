import type { ReactNode } from 'react';
import { ActivityIndicator, Pressable, ScrollView, Text, View, useColorScheme } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { SvgXml } from 'react-native-svg';
import { useTranslation } from 'react-i18next';
import type { TransferState } from '@diasposwap/shared-types';
import { logoDark, logoLight, markDark, markLight } from './brand-svg';

export function Mark({ size = 48, dark }: { size?: number; dark?: boolean }) {
  const scheme = useColorScheme();
  const useDark = dark ?? scheme === 'dark';
  return <SvgXml xml={useDark ? markDark : markLight} width={size} height={size} />;
}

export function Logo({ height = 36, dark }: { height?: number; dark?: boolean }) {
  const scheme = useColorScheme();
  const useDark = dark ?? scheme === 'dark';
  return <SvgXml xml={useDark ? logoDark : logoLight} width={(height * 520) / 128} height={height} />;
}

/** Permanent, non-dismissable notice required by the brief. */
export function SimulationBanner() {
  const { t } = useTranslation();
  return (
    <View accessibilityRole="alert" className="bg-gold-100 dark:bg-petrol-700 border-b border-gold px-4 py-1.5">
      <Text className="text-center text-xs font-semibold text-petrol dark:text-gold">⚠︎ {t('sim')}</Text>
    </View>
  );
}

export function Screen({ children, scroll = true }: { children: ReactNode; scroll?: boolean }) {
  return (
    <SafeAreaView edges={['top']} className="flex-1 bg-ivory dark:bg-petrol">
      <SimulationBanner />
      {scroll ? (
        <ScrollView contentContainerClassName="px-4 pb-10 pt-4 gap-4" keyboardShouldPersistTaps="handled">{children}</ScrollView>
      ) : (
        <View className="flex-1 px-4 pt-4">{children}</View>
      )}
    </SafeAreaView>
  );
}

export function H1({ children }: { children: ReactNode }) {
  return <Text accessibilityRole="header" className="text-2xl font-bold text-petrol dark:text-ivory">{children}</Text>;
}
export function H2({ children }: { children: ReactNode }) {
  return <Text accessibilityRole="header" className="text-base font-semibold text-petrol dark:text-ivory">{children}</Text>;
}
export function Muted({ children, className = '' }: { children: ReactNode; className?: string }) {
  return <Text className={`text-sm text-anthracite-500 dark:text-ivory-300 ${className}`}>{children}</Text>;
}
export function Body({ children, className = '' }: { children: ReactNode; className?: string }) {
  return <Text className={`text-base text-anthracite dark:text-ivory ${className}`}>{children}</Text>;
}

export function Card({ children, className = '' }: { children: ReactNode; className?: string }) {
  return <View className={`rounded-2xl bg-white dark:bg-petrol-700 border border-ivory-200 dark:border-petrol-600 p-4 gap-2 ${className}`}>{children}</View>;
}

export function Button({ title, onPress, variant = 'primary', disabled, loading, testID }: {
  title: string; onPress: () => void; variant?: 'primary' | 'secondary' | 'ghost' | 'danger'; disabled?: boolean; loading?: boolean; testID?: string;
}) {
  const base = 'rounded-xl px-4 py-3.5 items-center justify-center min-h-[48px]';
  const styles: Record<string, string> = {
    primary: 'bg-emerald',
    secondary: 'bg-transparent border border-petrol dark:border-ivory',
    ghost: 'bg-transparent',
    danger: 'bg-danger',
  };
  const text: Record<string, string> = {
    primary: 'text-white', secondary: 'text-petrol dark:text-ivory', ghost: 'text-emerald dark:text-emerald-300', danger: 'text-white',
  };
  return (
    <Pressable testID={testID} accessibilityRole="button" accessibilityState={{ disabled: !!disabled }} disabled={disabled || loading} onPress={onPress}
      className={`${base} ${styles[variant]} ${disabled ? 'opacity-40' : 'active:opacity-80'}`}>
      {loading ? <ActivityIndicator color="#fff" /> : <Text className={`text-base font-semibold ${text[variant]}`}>{title}</Text>}
    </Pressable>
  );
}

export function Row({ label, value, strong }: { label: string; value: string; strong?: boolean }) {
  return (
    <View className="flex-row justify-between items-center gap-3">
      <Text className="text-sm text-anthracite-500 dark:text-ivory-300 flex-shrink">{label}</Text>
      <Text className={`text-sm text-right ${strong ? 'font-bold text-petrol dark:text-ivory text-base' : 'text-anthracite dark:text-ivory'}`}>{value}</Text>
    </View>
  );
}

const STATE_TONE: Partial<Record<TransferState, string>> = {
  SETTLED: 'bg-emerald-100 text-emerald', REFUNDED: 'bg-ivory-200 text-anthracite', FAILED: 'bg-danger-100 text-danger',
  DISPUTED: 'bg-danger-100 text-danger', CANCELLED: 'bg-ivory-200 text-anthracite-500', EXPIRED: 'bg-ivory-200 text-anthracite-500',
};

export function StatePill({ state }: { state: TransferState }) {
  const { t } = useTranslation();
  const tone = STATE_TONE[state] ?? 'bg-gold-100 text-petrol';
  const [bg, fg] = tone.split(' ');
  return (
    <View className={`self-start rounded-full px-2.5 py-1 ${bg}`}>
      <Text className={`text-xs font-semibold ${fg}`}>{t(`states.${state}`)}</Text>
    </View>
  );
}

export function Progress({ ratio }: { ratio: number }) {
  const pct = Math.max(0, Math.min(1, ratio)) * 100;
  return (
    <View accessibilityRole="progressbar" accessibilityValue={{ min: 0, max: 100, now: Math.round(pct) }} className="h-2 rounded-full bg-ivory-200 dark:bg-petrol-600 overflow-hidden">
      <View className="h-2 rounded-full bg-emerald" style={{ width: `${pct}%` }} />
    </View>
  );
}

export function Chip({ label, selected, onPress }: { label: string; selected?: boolean; onPress: () => void }) {
  return (
    <Pressable accessibilityRole="button" accessibilityState={{ selected: !!selected }} onPress={onPress}
      className={`rounded-full px-3.5 py-2 border ${selected ? 'bg-petrol border-petrol dark:bg-gold dark:border-gold' : 'border-ivory-300 dark:border-petrol-600'}`}>
      <Text className={`text-sm ${selected ? 'text-ivory dark:text-petrol font-semibold' : 'text-anthracite dark:text-ivory'}`}>{label}</Text>
    </Pressable>
  );
}

export function ListItem({ title, subtitle, right, onPress }: { title: string; subtitle?: string; right?: ReactNode; onPress?: () => void }) {
  return (
    <Pressable accessibilityRole={onPress ? 'button' : undefined} onPress={onPress} className="flex-row items-center justify-between py-3 gap-3 border-b border-ivory-200 dark:border-petrol-600">
      <View className="flex-1 gap-0.5">
        <Text className="text-base text-anthracite dark:text-ivory">{title}</Text>
        {subtitle ? <Text className="text-xs text-anthracite-500 dark:text-ivory-300">{subtitle}</Text> : null}
      </View>
      {right}
    </Pressable>
  );
}
