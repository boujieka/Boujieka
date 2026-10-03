import Link from "next/link";

const LINKS = [
  { href: "/", label: "Home" },
  { href: "/auctions", label: "Auction calendar" },
  { href: "/countries", label: "Countries" },
  { href: "/admin/data-quality", label: "Data quality" },
];

export function Nav() {
  return (
    <header className="border-b border-border bg-surface">
      <div className="mx-auto flex max-w-[1400px] flex-wrap items-center gap-x-6 gap-y-2 px-4 py-2.5">
        <Link href="/" className="flex items-baseline gap-2">
          <span className="text-sm font-bold tracking-wider">AFRICAN BOND INTELLIGENCE</span>
          <span className="hidden text-xs text-muted md:inline">Africa&apos;s Sovereign Debt Opportunity Engine</span>
        </Link>
        <nav aria-label="Main" className="flex flex-wrap gap-x-4 gap-y-1 text-sm">
          {LINKS.map((l) => (
            <Link key={l.href} href={l.href} className="text-muted hover:text-foreground focus-visible:text-foreground">
              {l.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
