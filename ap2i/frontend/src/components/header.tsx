"use client";

import Image from "next/image";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { cn } from "@/lib/utils";
import type { Locale } from "@/lib/format";
import { useI18n } from "./i18n-provider";

export interface HeaderUser { name: string; isAdmin: boolean }

export function Header({ user }: { user: HeaderUser | null }) {
  const { d, locale } = useI18n();
  const pathname = usePathname();
  const router = useRouter();
  const [open, setOpen] = useState(false);
  useEffect(() => setOpen(false), [pathname]);

  const items: [string, string][] = [
    ["/", d.nav.home], ["/africa", d.nav.africa], ["/countries", d.nav.countries], ["/projects", d.nav.projects],
    ["/sectors", d.nav.sectors], ["/financing", d.nav.financing], ["/performance", d.nav.performance], ["/rescue", d.nav.rescue],
    ["/intelligence", d.nav.intelligence], ["/reports", d.nav.reports], ["/explorer", d.nav.explorer], ["/pricing", d.nav.pricing],
    ["/about", d.nav.about],
  ];
  if (user?.isAdmin) items.push(["/admin", d.nav.admin]);
  const isActive = (href: string) => (href === "/" ? pathname === "/" : pathname === href || pathname.startsWith(`${href}/`));

  async function switchLocale(l: Locale) {
    await fetch("/api/session/locale", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ locale: l }) });
    router.refresh();
  }
  async function logout() {
    await fetch("/api/session/logout", { method: "POST" });
    router.push("/login?logged_out=1");
    router.refresh();
  }

  const authLinks = user ? (
    <>
      <Link href="/account" className="rounded px-2 py-1 text-sm text-white/90 hover:bg-white/10">{d.nav.account}</Link>
      <button type="button" onClick={logout} className="rounded px-2 py-1 text-sm text-white/90 hover:bg-white/10">{d.nav.logout}</button>
    </>
  ) : (
    <>
      <Link href="/login" className="rounded px-2 py-1 text-sm text-white/90 hover:bg-white/10">{d.nav.login}</Link>
      <Link href="/register" className="rounded bg-gold px-2.5 py-1 text-sm font-semibold text-navy hover:brightness-105">{d.nav.register}</Link>
    </>
  );

  return (
    <header className="bg-navy text-white">
      <a href="#main" className="sr-only focus:not-sr-only focus:absolute focus:left-2 focus:top-2 focus:z-50 focus:rounded focus:bg-white focus:px-3 focus:py-2 focus:text-navy">{d.nav.skip}</a>
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-3 px-4 py-2">
        <Link href="/" className="flex min-w-0 items-center gap-2 no-underline" aria-label="AP²I">
          <Image src="/ap2i-logo.png" alt="" width={40} height={40} className="h-10 w-10 rounded bg-white object-contain" priority />
          <span className="min-w-0">
            <span className="block text-lg font-bold leading-tight">AP²I</span>
            <span className="hidden text-xs leading-tight text-white/75 sm:block">{d.meta.name}</span>
          </span>
        </Link>
        <div className="flex items-center gap-1">
          <div role="group" aria-label={d.nav.language} className="flex overflow-hidden rounded border border-white/30 text-xs">
            {(["fr", "en"] as const).map((l) => (
              <button key={l} type="button" onClick={() => switchLocale(l)} aria-pressed={locale === l}
                className={cn("px-2 py-1 uppercase", locale === l ? "bg-white text-navy font-bold" : "text-white/85 hover:bg-white/10")}>
                {l}
              </button>
            ))}
          </div>
          {user ? <span className="ml-2 hidden max-w-40 truncate text-xs text-white/70 lg:inline" title={user.name}>{user.name}</span> : null}
          <div className="hidden items-center gap-1 md:flex">{authLinks}</div>
          <button type="button" className="ml-1 rounded border border-white/30 px-2 py-1 text-sm md:hidden" aria-expanded={open} aria-controls="main-nav" onClick={() => setOpen((v) => !v)}>
            {d.nav.menu}
          </button>
        </div>
      </div>
      <nav id="main-nav" aria-label="Main" className={cn("border-t border-white/10 bg-navy-700", open ? "block" : "hidden md:block")}>
        <ul className="mx-auto flex max-w-7xl flex-col px-2 py-1 md:flex-row md:flex-wrap md:px-4">
          {items.map(([href, text]) => (
            <li key={href}>
              <Link href={href} aria-current={isActive(href) ? "page" : undefined}
                className={cn("block rounded px-2.5 py-2 text-sm no-underline md:py-1.5", isActive(href) ? "bg-white/15 font-semibold text-white" : "text-white/85 hover:bg-white/10")}>
                {text}
              </Link>
            </li>
          ))}
          <li className="flex gap-1 border-t border-white/10 py-2 md:hidden">{authLinks}</li>
        </ul>
      </nav>
    </header>
  );
}
