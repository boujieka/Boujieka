import '../global.css';
import '../i18n';
import { useEffect } from 'react';
import { useColorScheme } from 'react-native';
import { DarkTheme, DefaultTheme, Stack, ThemeProvider } from 'expo-router';
import * as SplashScreen from 'expo-splash-screen';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { StatusBar } from 'expo-status-bar';

void SplashScreen.preventAutoHideAsync();
const queryClient = new QueryClient({ defaultOptions: { queries: { retry: 0 } } });

const light = { ...DefaultTheme, colors: { ...DefaultTheme.colors, background: '#FAF8F2', card: '#FAF8F2', primary: '#087F6D', text: '#182525', border: '#EFEBDF' } };
const dark = { ...DarkTheme, colors: { ...DarkTheme.colors, background: '#082F35', card: '#082F35', primary: '#C9A44C', text: '#FAF8F2', border: '#14505A' } };

export default function RootLayout() {
  const scheme = useColorScheme();
  useEffect(() => { void SplashScreen.hideAsync(); }, []);
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider value={scheme === 'dark' ? dark : light}>
        <StatusBar style="auto" />
        <Stack screenOptions={{ headerShown: false }}>
          <Stack.Screen name="index" />
          <Stack.Screen name="onboarding" />
          <Stack.Screen name="login" />
          <Stack.Screen name="(tabs)" />
          <Stack.Screen name="transfer/confirm" options={{ presentation: 'card' }} />
          <Stack.Screen name="transfer/[id]" />
          <Stack.Screen name="receipt/[id]" />
          <Stack.Screen name="beneficiaries" />
          <Stack.Screen name="notifications" />
          <Stack.Screen name="liquidity" />
        </Stack>
      </ThemeProvider>
    </QueryClientProvider>
  );
}
