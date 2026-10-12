"use client";
import { PlannedPage } from "@/components/planned";

export default function PortfolioPage() {
  return <PlannedPage title="planned.portfolio.title" phase="planned.portfolio.phase" text="planned.portfolio.text" links={[{ href: "/app", key: "nav.dashboard" }, { href: "/app/finance", key: "nav.finance" }]} />;
}
