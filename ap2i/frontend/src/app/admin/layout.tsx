import Link from "next/link";
import { Forbidden, LoginRequired } from "@/components/states";
import { getI18n } from "@/i18n/server";
import { canAdmin, getMe, hasPermission } from "@/lib/api";

export const metadata = { title: "Admin" };

export default async function AdminLayout({ children }: { children: React.ReactNode }) {
  const { d } = await getI18n();
  const me = await getMe();
  if (!me) return <LoginRequired d={d} next="/admin" />;
  if (!canAdmin(me)) return <Forbidden d={d} />;
  const all = hasPermission(me, "admin:all");
  const org = hasPermission(me, "admin:organization");
  const items: [string, string, boolean][] = [
    ["/admin/connectors", d.admin.connectors, true], ["/admin/sync-runs", d.admin.syncRuns, true], ["/admin/review", d.admin.review, true],
    ["/admin/matches", d.admin.matches, true], ["/admin/uploads", d.admin.uploads, hasPermission(me, "data:contribute")], ["/admin/users", d.admin.users, org],
    ["/admin/organizations", d.admin.organizations, all], ["/admin/subscriptions", d.admin.subscriptions, all], ["/admin/audit", d.admin.audit, all],
    ["/admin/system", d.admin.system, all], ["/admin/settings", d.admin.settings, all],
  ];
  return (
    <div className="grid gap-6 lg:grid-cols-[220px_minmax(0,1fr)]">
      <nav aria-label={d.admin.title} className="min-w-0">
        <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-muted">{d.admin.title}</p>
        <ul className="flex flex-wrap gap-1 lg:flex-col">
          {items.filter(([, , ok]) => ok).map(([href, t]) => <li key={href}><Link href={href} className="block rounded px-2 py-1.5 text-sm text-navy hover:bg-navy-50">{t}</Link></li>)}
        </ul>
      </nav>
      <div className="min-w-0">{children}</div>
    </div>
  );
}
