"use client";
import { PlannedPage } from "@/components/planned";

export default function DeliveryPage() {
  return <PlannedPage title="planned.delivery.title" phase="planned.delivery.phase" text="planned.delivery.text" links={[{ href: "/app/projects", key: "nav.projects" }]} />;
}
