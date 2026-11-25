import { type ColorValue, Text } from 'react-native';
import { Redirect } from 'expo-router';
import { Tabs } from 'expo-router/tabs';
import { useTranslation } from 'react-i18next';
import { useApp } from '@/lib/store';

const icon = (glyph: string) => ({ color }: { color: ColorValue }) => <Text style={{ color, fontSize: 18 }}>{glyph}</Text>;

export default function TabsLayout() {
  const { t } = useTranslation();
  const userId = useApp((s) => s.userId);
  if (!userId) return <Redirect href="/login" />;
  return (
    <Tabs screenOptions={{ headerShown: false, tabBarActiveTintColor: '#087F6D', tabBarInactiveTintColor: '#6B7878' }}>
      <Tabs.Screen name="index" options={{ title: t('tabs.home'), tabBarIcon: icon('⌂') }} />
      <Tabs.Screen name="send" options={{ title: t('tabs.send'), tabBarIcon: icon('⇄'), tabBarButtonTestID: 'tab-send' }} />
      <Tabs.Screen name="history" options={{ title: t('tabs.history'), tabBarIcon: icon('☰') }} />
      <Tabs.Screen name="profile" options={{ title: t('tabs.profile'), tabBarIcon: icon('◉') }} />
    </Tabs>
  );
}
