import * as React from "react";
import { cn } from "@/lib/utils";

export function Card({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("min-w-0 rounded-lg border border-line bg-white shadow-sm", className)} {...props} />;
}

export function CardHeader({ title, description, actions, className, as: As = "h2" }: { title: React.ReactNode; description?: React.ReactNode; actions?: React.ReactNode; className?: string; as?: "h1" | "h2" | "h3" }) {
  return (
    <div className={cn("flex flex-wrap items-start justify-between gap-2 border-b border-line px-4 py-3", className)}>
      <div className="min-w-0">
        <As className="text-base font-semibold text-navy">{title}</As>
        {description ? <p className="mt-0.5 text-sm text-muted">{description}</p> : null}
      </div>
      {actions ? <div className="flex flex-wrap gap-2">{actions}</div> : null}
    </div>
  );
}

export function CardBody({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("p-4", className)} {...props} />;
}
