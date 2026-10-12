"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState, type ReactNode } from "react";
import { Building2, ChevronDown, LogOut, Menu, User, X } from "lucide-react";
import { Brand } from "@/components/brand";
import { DemoBadge } from "@/components/badges";
import { LangToggle } from "@/components/lang-toggle";
import { Loading, ErrorBox } from "@/components/page";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuRadioGroup,
  DropdownMenuRadioItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { useI18n, type DictKey } from "@/lib/i18n";
import { useSession } from "@/lib/session";
import { cn } from "@/lib/utils";

const NAV: { href: string; key: DictKey; exact?: boolean }[] = [
  { href: "/app", key: "nav.dashboard", exact: true },
  { href: "/app/explore", key: "nav.explore" },
  { href: "/app/projects", key: "nav.projects" },
  { href: "/app/optimizer", key: "nav.optimizer" },
  { href: "/app/finance", key: "nav.finance" },
  { href: "/app/portfolio", key: "nav.portfolio" },
  { href: "/app/investors", key: "nav.investors" },
  { href: "/app/delivery", key: "nav.delivery" },
  { href: "/app/academy", key: "nav.academy" },
  { href: "/app/reports", key: "nav.reports" },
  { href: "/app/admin", key: "nav.admin" },
];

function OrgSwitcher() {
  const { me, org, setOrgId } = useSession();
  const { t } = useI18n();
  if (!me || !org) return null;
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <button
          type="button"
          className="flex max-w-[14rem] items-center gap-2 rounded-md border border-white/20 px-2.5 py-1.5 text-left text-xs text-white hover:bg-white/10"
          aria-label={t("nav.organisation")}
          data-testid="org-switcher"
        >
          <Building2 className="size-3.5 shrink-0 text-gold-500" aria-hidden />
          <span className="truncate">{org.name}</span>
          <ChevronDown className="size-3.5 shrink-0 opacity-70" aria-hidden />
        </button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-72">
        <DropdownMenuLabel>{t("nav.organisation")}</DropdownMenuLabel>
        <DropdownMenuRadioGroup value={org.id} onValueChange={setOrgId}>
          {me.organizations.map((o) => (
            <DropdownMenuRadioItem key={o.id} value={o.id}>
              <span className="flex min-w-0 flex-col">
                <span className="truncate">{o.name}</span>
                <span className="text-xs text-subtle-foreground">
                  {o.role}
                  {o.plan ? ` · ${o.plan}` : ""}
                  {o.is_demo ? ` · ${t("common.demoBadge")}` : ""}
                </span>
              </span>
            </DropdownMenuRadioItem>
          ))}
        </DropdownMenuRadioGroup>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

function UserMenu() {
  const { me, logout } = useSession();
  const { t } = useI18n();
  const router = useRouter();
  if (!me) return null;
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <button type="button" className="flex size-8 items-center justify-center rounded-full bg-white/10 text-white hover:bg-white/20" aria-label={me.full_name} data-testid="user-menu">
          <User className="size-4" aria-hidden />
        </button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuLabel>
          {t("nav.signedInAs")}
          <span className="block truncate font-medium text-foreground">{me.full_name}</span>
          <span className="block truncate">{me.email}</span>
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuItem
          onSelect={async () => {
            await logout();
            router.push("/login");
          }}
          data-testid="logout"
        >
          <LogOut className="size-4" aria-hidden /> {t("nav.logout")}
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

export function AppShell({ children }: { children: ReactNode }) {
  const { me, loading, error, org, refresh } = useSession();
  const { t } = useI18n();
  const pathname = usePathname();
  const router = useRouter();
  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (!loading && !me && !error) router.replace(`/login?next=${encodeURIComponent(pathname)}`);
  }, [loading, me, error, router, pathname]);

  const active = (href: string, exact?: boolean) => (exact ? pathname === href : pathname === href || pathname.startsWith(`${href}/`));

  return (
    <div className="flex min-h-screen flex-col">
      <header className="sticky top-0 z-40">
        <div className="bg-navy-950">
          <div className="mx-auto flex max-w-7xl items-center justify-between gap-3 px-4 py-2.5 sm:px-6">
            <div className="flex min-w-0 items-center gap-3">
              <button
                type="button"
                className="rounded p-1 text-white lg:hidden"
                aria-label={t("nav.menu")}
                aria-expanded={open}
                aria-controls="main-nav-mobile"
                onClick={() => setOpen((v) => !v)}
              >
                {open ? <X className="size-5" aria-hidden /> : <Menu className="size-5" aria-hidden />}
              </button>
              <Brand href="/app" inverted />
            </div>
            <div className="flex min-w-0 items-center gap-2 sm:gap-3">
              <div className="hidden sm:block">
                <OrgSwitcher />
              </div>
              <LangToggle inverted />
              <UserMenu />
            </div>
          </div>
        </div>
        <nav aria-label="Main" className="hidden border-b border-border bg-surface lg:block">
          <ul className="mx-auto flex max-w-7xl gap-0.5 overflow-x-auto px-4 sm:px-6" data-testid="main-nav">
            {NAV.map((n) => (
              <li key={n.href}>
                <Link
                  href={n.href}
                  aria-current={active(n.href, n.exact) ? "page" : undefined}
                  className={cn(
                    "block whitespace-nowrap border-b-2 px-2.5 py-2.5 text-[13px] font-medium transition-colors",
                    active(n.href, n.exact) ? "border-emerald-600 text-navy-900" : "border-transparent text-muted-foreground hover:text-navy-900",
                  )}
                >
                  {t(n.key)}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
        {open ? (
          <nav id="main-nav-mobile" aria-label="Main" className="border-b border-border bg-surface lg:hidden">
            <div className="px-4 pt-3 sm:hidden">
              <div className="rounded-md bg-navy-950 p-2">
                <OrgSwitcher />
              </div>
            </div>
            <ul className="grid grid-cols-2 gap-1 p-3 sm:grid-cols-3">
              {NAV.map((n) => (
                <li key={n.href}>
                  <Link
                    href={n.href}
                    onClick={() => setOpen(false)}
                    aria-current={active(n.href, n.exact) ? "page" : undefined}
                    className={cn("block rounded px-3 py-2 text-sm", active(n.href, n.exact) ? "bg-navy-50 font-medium text-navy-900" : "text-muted-foreground")}
                  >
                    {t(n.key)}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>
        ) : null}
      </header>

      <main className="mx-auto w-full max-w-7xl flex-1 px-4 py-6 sm:px-6 sm:py-8">
        {org?.is_demo ? (
          <div className="mb-4">
            <DemoBadge />
          </div>
        ) : null}
        {loading ? <Loading /> : error ? <ErrorBox error={error} onRetry={() => void refresh()} /> : !me ? <Loading /> : !org ? <ErrorBox error="No organisation" /> : children}
      </main>
      <footer className="border-t border-border bg-surface">
        <div className="mx-auto max-w-7xl px-4 py-4 text-xs text-subtle-foreground sm:px-6">{t("home.footer")}</div>
      </footer>
    </div>
  );
}

export function PlainButtonLink({ href, children }: { href: string; children: ReactNode }) {
  return (
    <Button asChild variant="outline" size="sm">
      <Link href={href}>{children}</Link>
    </Button>
  );
}
