"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/cn";
import { ArchiveIcon, BookIcon, ChartIcon, HomeIcon } from "@/components/ui/icons";

const NAV_ITEMS = [
  { href: "/account", label: "Accueil", icon: HomeIcon },
  { href: "/learn", label: "Apprendre", icon: BookIcon },
  { href: "/progress", label: "Progression", icon: ChartIcon },
  { href: "/archive", label: "Archives", icon: ArchiveIcon },
];

/**
 * Bottom tab bar on mobile (thumb-reachable — CLAUDE.md §25 mobile-first),
 * becomes a sticky top bar at the sm breakpoint and up.
 */
export function Nav() {
  const pathname = usePathname();

  return (
    <nav
      aria-label="Navigation principale"
      className="fixed inset-x-0 bottom-0 z-40 border-t border-zinc-200 bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/80 sm:sticky sm:top-0 sm:border-t-0 sm:border-b dark:border-zinc-800 dark:bg-zinc-950/95 dark:supports-[backdrop-filter]:bg-zinc-950/80"
    >
      <ul className="mx-auto flex max-w-2xl items-stretch justify-around px-2 sm:justify-start sm:gap-1 sm:px-6">
        {NAV_ITEMS.map((item) => {
          const active = pathname === item.href || pathname.startsWith(`${item.href}/`);
          const Icon = item.icon;
          return (
            <li key={item.href} className="flex-1 sm:flex-none">
              <Link
                href={item.href}
                aria-current={active ? "page" : undefined}
                className={cn(
                  "flex flex-col items-center gap-0.5 px-2 py-2.5 text-xs font-medium transition-colors sm:flex-row sm:gap-2 sm:px-3 sm:py-4 sm:text-sm",
                  active
                    ? "text-indigo-600 dark:text-indigo-400"
                    : "text-zinc-500 hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-zinc-100",
                )}
              >
                <Icon className="h-5 w-5" />
                {item.label}
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
