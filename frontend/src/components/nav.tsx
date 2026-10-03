import Link from "next/link";

const LINKS = [
  { href: "/", label: "Home" },
  { href: "/radar", label: "Opportunity Radar" },
  { href: "/auctions", label: "Auction calendar" },
  { href: "/countries", label: "Countries" },
  { href: "/admin/data-quality", label: "Data quality" },
];

export function Nav() {
  return (
    <header className="border-b border-border bg-surface">
      <div className="mx-auto flex max-w-[1400px] flex-wrap items-center gap-x-6 gap-y-2 px-4 py-2.5">
        <Link href="/" className="flex items-center gap-2.5" aria-label="Cartouche, African Bond Intelligence">
          {/* Cartouche mark: see brand/BRAND.md */}
          <svg viewBox="0 0 64 96" className="h-8 w-auto" aria-hidden="true">
            <rect x="8" y="4" width="48" height="78" rx="24" fill="#13306b" stroke="#c9a24a" strokeWidth="4" />
            <rect x="5" y="86" width="54" height="6" rx="2" fill="#c9a24a" />
            <circle cx="32" cy="23" r="7" fill="#c9a24a" />
            <path d="M17 72V60l3.5-4 3.5 4v12zM28.5 72V51l3.5-4 3.5 4v21zM40 72V42l3.5-4 3.5 4v30z" fill="#3fb2a6" />
          </svg>
          <span className="leading-tight">
            <span className="block text-sm font-bold tracking-[0.18em]">CARTOUCHE</span>
            <span className="block text-[10px] font-semibold tracking-[0.2em] text-muted">AFRICAN BOND INTELLIGENCE</span>
          </span>
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
