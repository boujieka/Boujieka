import * as React from "react";
import { cn } from "@/lib/utils";

type Tone = "info" | "warning" | "danger" | "success";
const tones: Record<Tone, string> = {
  info: "border-navy/30 bg-navy-50 text-navy",
  warning: "border-gold/50 bg-gold-50 text-[#5c4409]",
  danger: "border-danger/30 bg-danger-50 text-danger",
  success: "border-emerald/30 bg-emerald-50 text-emerald",
};

export function Alert({ tone = "info", title, children, className, role }: { tone?: Tone; title?: React.ReactNode; children?: React.ReactNode; className?: string; role?: string }) {
  return (
    <div role={role ?? (tone === "danger" ? "alert" : "note")} className={cn("rounded-md border px-4 py-3 text-sm", tones[tone], className)}>
      {title ? <p className="font-semibold">{title}</p> : null}
      {children ? <div className={title ? "mt-1" : ""}>{children}</div> : null}
    </div>
  );
}
