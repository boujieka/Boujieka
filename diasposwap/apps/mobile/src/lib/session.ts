import { Platform } from 'react-native';
import * as SecureStore from 'expo-secure-store';

/** Session persistence: SecureStore on device (Keychain / Keystore). On web, memory only (no localStorage for secrets). */
const memory = new Map<string, string>();
const KEY = 'diasposwap.session';

export async function saveSession(userId: string): Promise<void> {
  if (Platform.OS === 'web') { memory.set(KEY, userId); return; }
  await SecureStore.setItemAsync(KEY, userId);
}
export async function loadSession(): Promise<string | null> {
  if (Platform.OS === 'web') return memory.get(KEY) ?? null;
  return SecureStore.getItemAsync(KEY);
}
export async function clearSession(): Promise<void> {
  if (Platform.OS === 'web') { memory.delete(KEY); return; }
  await SecureStore.deleteItemAsync(KEY);
}
