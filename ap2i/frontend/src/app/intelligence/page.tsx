import { Assistant } from "@/components/assistant";
import { CoverageNotice } from "@/components/coverage";
import { PageHeader } from "@/components/page-header";
import { Forbidden, LoginRequired } from "@/components/states";
import { getI18n } from "@/i18n/server";
import { getMe, hasPermission } from "@/lib/api";

export const metadata = { title: "Intelligence" };

export default async function IntelligencePage() {
  const { d } = await getI18n();
  const me = await getMe();
  return (
    <div className="space-y-4">
      <PageHeader title={d.intelligence.title} subtitle={d.intelligence.subtitle} />
      <CoverageNotice d={d} />
      {!me ? <LoginRequired d={d} next="/intelligence" /> : !hasPermission(me, "assistant:use") ? <Forbidden d={d} /> : <Assistant />}
    </div>
  );
}
