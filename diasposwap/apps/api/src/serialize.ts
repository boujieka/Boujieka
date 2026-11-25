/** JSON-safe conversion: bigint amounts are sent as decimal strings of MINOR units, never as floats. */
export function toJson(value: unknown): unknown {
  if (typeof value === 'bigint') return value.toString();
  if (Array.isArray(value)) return value.map(toJson);
  if (value && typeof value === 'object') {
    if (value instanceof Map) return Object.fromEntries([...value].map(([k, v]) => [String(k), toJson(v)]));
    return Object.fromEntries(Object.entries(value).map(([k, v]) => [k, toJson(v)]));
  }
  return value;
}
