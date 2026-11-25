import { useEffect, useState } from 'react';
import { View } from 'react-native';
import { Redirect } from 'expo-router';
import { Mark } from '@/components/ui';
import { useApp } from '@/lib/store';
import { loadSession } from '@/lib/session';

/** Splash / router gate. */
export default function Index() {
  const { userId, onboarded, login } = useApp();
  const [ready, setReady] = useState(false);
  useEffect(() => {
    void loadSession().then(async (id) => { if (id && useApp.getState().sim.users.has(id)) await login(id); setReady(true); });
  }, [login]);
  if (!ready) return <View className="flex-1 items-center justify-center bg-petrol"><Mark size={120} dark /></View>;
  if (!onboarded && !userId) return <Redirect href="/onboarding" />;
  if (!userId) return <Redirect href="/login" />;
  return <Redirect href="/(tabs)" />;
}
