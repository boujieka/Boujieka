"use client";

import Link from "next/link";
import { useParams, usePathname, useRouter, useSearchParams } from "next/navigation";
import { Suspense, useCallback } from "react";
import { ArrowLeft } from "lucide-react";
import { DemoBadge, StatusBadge } from "@/components/badges";
import { ErrorBox, Loading, PageHeader } from "@/components/page";
import { ExportsTab } from "@/components/project/exports";
import { InputsTab } from "@/components/project/inputs-form";
import { MilestonesTab } from "@/components/project/milestones";
import { OverviewTab } from "@/components/project/overview";
import { ResultsTab } from "@/components/project/results";
import { ScoreTab } from "@/components/project/score";
import { SensitivityTab } from "@/components/project/sensitivity";
import { SubsidyTab } from "@/components/project/subsidy";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { orgPath } from "@/lib/api";
import { useApi } from "@/lib/hooks";
import { useI18n, type DictKey } from "@/lib/i18n";
import { useSession } from "@/lib/session";
import type { Project } from "@/lib/types";

const TABS = ["overview", "inputs", "results", "sensitivity", "subsidy", "score", "milestones", "exports"] as const;
type Tab = (typeof TABS)[number];

function ProjectDetail() {
  const { id } = useParams<{ id: string }>();
  const { org } = useSession();
  const { t } = useI18n();
  const router = useRouter();
  const pathname = usePathname();
  const params = useSearchParams();
  const tabParam = params.get("tab");
  const tab: Tab = (TABS as readonly string[]).includes(tabParam ?? "") ? (tabParam as Tab) : "overview";
  const project = useApi<Project>(org ? orgPath(org.id, `/projects/${id}`) : null);

  const setTab = useCallback(
    (v: string) => {
      const q = new URLSearchParams(params.toString());
      q.set("tab", v);
      router.replace(`${pathname}?${q.toString()}`, { scroll: false });
    },
    [params, pathname, router],
  );

  if (!org) return null;
  if (project.loading && !project.data) return <Loading />;
  if (project.error) return <ErrorBox error={project.error} onRetry={project.reload} />;
  const p = project.data;
  if (!p) return null;

  return (
    <>
      <Link href="/app/projects" className="mb-3 inline-flex items-center gap-1 text-xs text-muted-foreground hover:text-navy-900">
        <ArrowLeft className="size-3.5" aria-hidden /> {t("projects.title")}
      </Link>
      <PageHeader
        title={p.name}
        lead={`${p.country} · ${t(`stage.${p.stage}` as DictKey)}`}
        badges={
          <>
            <StatusBadge status={p.latest_run?.status} />
            <DemoBadge show={p.is_demo || !!p.latest_run?.is_demo} />
          </>
        }
      />
      <Tabs value={tab} onValueChange={setTab}>
        <TabsList aria-label={p.name}>
          {TABS.map((k) => (
            <TabsTrigger key={k} value={k} data-testid={`tab-${k}`}>
              {t(`tab.${k}` as DictKey)}
            </TabsTrigger>
          ))}
        </TabsList>
        <TabsContent value="overview">
          <OverviewTab project={p} onChanged={project.reload} />
        </TabsContent>
        <TabsContent value="inputs">
          <InputsTab project={p} onSaved={project.reload} />
        </TabsContent>
        <TabsContent value="results">
          <ResultsTab project={p} onRun={project.reload} />
        </TabsContent>
        <TabsContent value="sensitivity">
          <SensitivityTab project={p} />
        </TabsContent>
        <TabsContent value="subsidy">
          <SubsidyTab project={p} />
        </TabsContent>
        <TabsContent value="score">
          <ScoreTab key={p.latest_run?.id ?? "none"} project={p} />
        </TabsContent>
        <TabsContent value="milestones">
          <MilestonesTab project={p} />
        </TabsContent>
        <TabsContent value="exports">
          <ExportsTab project={p} />
        </TabsContent>
      </Tabs>
    </>
  );
}

export default function ProjectPage() {
  return (
    <Suspense fallback={<Loading />}>
      <ProjectDetail />
    </Suspense>
  );
}
