/** Only same-site relative paths are accepted as post-login redirect targets (no open redirect). */
export function safeNext(v: string | null | undefined): string {
  if (!v || !v.startsWith("/") || v.startsWith("//") || v.startsWith("/\\") || v.includes("://")) return "/";
  return v;
}
