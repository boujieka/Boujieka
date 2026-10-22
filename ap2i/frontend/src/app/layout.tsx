import type { Metadata, Viewport } from "next";
import "./globals.css";
import { Footer } from "@/components/footer";
import { Header } from "@/components/header";
import { I18nProvider } from "@/components/i18n-provider";
import { getI18n } from "@/i18n/server";
import { canAdmin, getMe } from "@/lib/api";

export async function generateMetadata(): Promise<Metadata> {
  const { d } = await getI18n();
  return {
    title: { default: `AP²I — ${d.meta.name}`, template: "%s · AP²I" },
    description: d.meta.description,
    icons: { icon: "/ap2i-logo.png" },
  };
}

export const viewport: Viewport = { width: "device-width", initialScale: 1, themeColor: "#082B50" };

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  const { locale, d } = await getI18n();
  const me = await getMe();
  return (
    <html lang={locale}>
      <body className="flex min-h-screen flex-col">
        <I18nProvider locale={locale} d={d}>
          <Header user={me ? { name: me.full_name || me.email, isAdmin: canAdmin(me) } : null} />
          <main id="main" className="mx-auto w-full max-w-7xl flex-1 px-4 py-6">
            {children}
          </main>
          <Footer d={d} />
        </I18nProvider>
      </body>
    </html>
  );
}
