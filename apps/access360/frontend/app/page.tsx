"use client";

import Link from "next/link";
import { ArrowRight, BarChart3, BookOpen, Building2, Compass, Handshake, HardHat, Landmark, Map, ShieldCheck, Users } from "lucide-react";
import { Brand } from "@/components/brand";
import { LangToggle } from "@/components/lang-toggle";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useI18n, type DictKey } from "@/lib/i18n";
import { useSession } from "@/lib/session";

const MODULES: { name: string; text: DictKey; available: boolean; icon: typeof Map }[] = [
  { name: "ACCESS MAP", text: "home.mod.map", available: true, icon: Map },
  { name: "ACCESS OPTIMIZER", text: "home.mod.optimizer", available: true, icon: Compass },
  { name: "ACCESS FINANCE", text: "home.mod.finance", available: true, icon: BarChart3 },
  { name: "ACCESS MARKETPLACE", text: "home.mod.marketplace", available: false, icon: Handshake },
  { name: "ACCESS DELIVERY", text: "home.mod.delivery", available: false, icon: HardHat },
  { name: "ACCESS VERIFY", text: "home.mod.verify", available: false, icon: ShieldCheck },
  { name: "ACCESS ACADEMY", text: "home.mod.academy", available: false, icon: BookOpen },
];

const AUDIENCES: { title: DictKey; text: DictKey; icon: typeof Map }[] = [
  { title: "home.who.developers", text: "home.who.developersText", icon: Building2 },
  { title: "home.who.investors", text: "home.who.investorsText", icon: Landmark },
  { title: "home.who.government", text: "home.who.governmentText", icon: Users },
  { title: "home.who.advisors", text: "home.who.advisorsText", icon: BarChart3 },
];

const PLANS = ["Free Explorer", "Professional", "Developer Pro", "Portfolio", "Institutional", "Enterprise"];

export default function HomePage() {
  const { t } = useI18n();
  const { me } = useSession();

  return (
    <div className="min-h-screen bg-background">
      <header className="bg-navy-950 text-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between gap-3 px-4 py-4 sm:px-6">
          <Brand inverted />
          <nav className="flex items-center gap-2 sm:gap-3">
            <LangToggle inverted />
            {me ? (
              <Button asChild size="sm" variant="gold">
                <Link href="/app">{t("nav.dashboard")}</Link>
              </Button>
            ) : (
              <Button asChild size="sm" variant="ghost" className="text-white hover:bg-white/10">
                <Link href="/login">{t("home.login")}</Link>
              </Button>
            )}
          </nav>
        </div>

        <section className="mx-auto max-w-6xl px-4 pb-16 pt-10 sm:px-6 sm:pb-24 sm:pt-16">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-gold-500">{t("home.kicker")}</p>
          <h1 className="mt-4 max-w-4xl text-3xl font-semibold leading-tight tracking-tight sm:text-5xl" data-testid="tagline">
            {t("brand.tagline")}
          </h1>
          <p className="mt-6 max-w-2xl text-base leading-relaxed text-white/80">{t("home.lead")}</p>
          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <Button asChild size="lg" variant="accent">
              <Link href="/register">
                {t("home.register")} <ArrowRight aria-hidden />
              </Link>
            </Button>
            <Button asChild size="lg" variant="outline" className="border-white/30 bg-transparent text-white hover:bg-white/10">
              <Link href="/login?demo=1">{t("home.demo")}</Link>
            </Button>
          </div>
        </section>
      </header>

      <main>
        <section className="mx-auto max-w-6xl px-4 py-14 sm:px-6">
          <h2 className="text-2xl font-semibold tracking-tight text-navy-900">{t("home.modules")}</h2>
          <p className="mt-2 text-sm text-muted-foreground">{t("home.modulesLead")}</p>
          <ul className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {MODULES.map((m) => (
              <li key={m.name} className="flex flex-col gap-3 rounded-lg border border-border bg-surface p-5">
                <div className="flex items-center justify-between gap-2">
                  <span className="flex items-center gap-2 text-sm font-semibold tracking-wide text-navy-900">
                    <m.icon className="size-4 text-emerald-700" aria-hidden /> {m.name}
                  </span>
                  {m.available ? <Badge variant="success">{t("common.availableNow")}</Badge> : <Badge variant="neutral">{t("common.planned")}</Badge>}
                </div>
                <p className="text-sm leading-relaxed text-muted-foreground">{t(m.text)}</p>
              </li>
            ))}
          </ul>
          <p className="mt-6 text-sm text-muted-foreground">{t("home.alsoNow")}</p>
        </section>

        <section className="border-y border-border bg-surface">
          <div className="mx-auto max-w-6xl px-4 py-14 sm:px-6">
            <h2 className="text-2xl font-semibold tracking-tight text-navy-900">{t("home.who")}</h2>
            <ul className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
              {AUDIENCES.map((a) => (
                <li key={a.title}>
                  <a.icon className="size-5 text-gold-700" aria-hidden />
                  <h3 className="mt-3 text-sm font-semibold text-navy-900">{t(a.title)}</h3>
                  <p className="mt-1 text-sm leading-relaxed text-muted-foreground">{t(a.text)}</p>
                </li>
              ))}
            </ul>
          </div>
        </section>

        <section className="mx-auto max-w-6xl px-4 py-14 sm:px-6">
          <h2 className="text-2xl font-semibold tracking-tight text-navy-900">{t("home.plans")}</h2>
          <p className="mt-2 text-sm text-muted-foreground">{t("home.plansLead")}</p>
          <ul className="mt-8 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {PLANS.map((p) => (
              <li key={p} className="flex items-center justify-between rounded-lg border border-border bg-surface px-5 py-4">
                <span className="font-semibold text-navy-900">{p}</span>
                <span className="text-xs text-muted-foreground">{t("home.pricingOnRequest")}</span>
              </li>
            ))}
          </ul>
          <div className="mt-10 flex flex-col gap-3 sm:flex-row">
            <Button asChild variant="default">
              <Link href="/register">{t("home.register")}</Link>
            </Button>
            <Button asChild variant="outline">
              <Link href="/login?demo=1">{t("home.demo")}</Link>
            </Button>
          </div>
        </section>
      </main>

      <footer className="border-t border-border bg-navy-950 text-white/70">
        <div className="mx-auto flex max-w-6xl flex-col gap-3 px-4 py-8 text-xs sm:flex-row sm:items-center sm:justify-between sm:px-6">
          <Brand inverted />
          <p>{t("home.footer")}</p>
        </div>
      </footer>
    </div>
  );
}
