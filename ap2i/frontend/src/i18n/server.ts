import "server-only";
import { cookies } from "next/headers";
import { dictionaries, LOCALE_COOKIE, normalizeLocale } from "./index";

export async function getI18n() {
  const locale = normalizeLocale((await cookies()).get(LOCALE_COOKIE)?.value);
  return { locale, d: dictionaries[locale] };
}
