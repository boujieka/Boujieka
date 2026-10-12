"use client";
import { PlannedPage } from "@/components/planned";

export default function InvestorsPage() {
  return <PlannedPage title="planned.investors.title" phase="planned.investors.phase" text="planned.investors.text" links={[{ href: "/app/projects", key: "nav.projects" }, { href: "/app/reports", key: "nav.reports" }]} />;
}
