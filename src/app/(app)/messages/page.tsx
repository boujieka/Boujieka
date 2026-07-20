import Link from "next/link";
import { requireUser } from "@/lib/auth/guards";
import { prisma } from "@/lib/db";
import { Card, EmptyState, Badge } from "@/components/ui";

export default async function MessagesPage() {
  const session = await requireUser();

  const messages = await prisma.message.findMany({
    where: { OR: [{ senderUserId: session.userId }, { recipientUserId: session.userId }] },
    orderBy: { createdAt: "desc" },
    include: { opportunity: { include: { site: true } }, sender: true, recipient: true },
  });

  // Regroupe par opportunité (fil de discussion).
  const threads = new Map<string, { title: string; country: string; last: (typeof messages)[number]; unread: number }>();
  for (const m of messages) {
    const key = m.opportunityId;
    const existing = threads.get(key);
    const unread = m.recipientUserId === session.userId && !m.readAt ? 1 : 0;
    if (!existing) {
      threads.set(key, {
        title: m.opportunity.title,
        country: m.opportunity.site.country,
        last: m,
        unread,
      });
    } else {
      existing.unread += unread;
    }
  }

  const list = Array.from(threads.entries());

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Messagerie</h1>
      {list.length === 0 ? (
        <EmptyState title="Aucune conversation">
          Les échanges se font depuis la page d'une opportunité.
        </EmptyState>
      ) : (
        <Card>
          <ul className="divide-y divide-navy-50">
            {list.map(([oppId, t]) => (
              <li key={oppId} className="flex items-center justify-between py-3">
                <div>
                  <Link href={`/opportunities/${oppId}`} className="font-medium hover:text-gold-600">
                    {t.title}
                  </Link>
                  <div className="text-xs text-navy-400">
                    {t.country} · {t.last.sender.fullName} : {t.last.body.slice(0, 60)}
                    {t.last.body.length > 60 ? "…" : ""}
                  </div>
                </div>
                {t.unread > 0 && <Badge tone="gold">{t.unread} non lu</Badge>}
              </li>
            ))}
          </ul>
        </Card>
      )}
    </div>
  );
}
