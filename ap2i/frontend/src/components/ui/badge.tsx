import * as React from "react";
import { cn } from "@/lib/utils";

export type Tone = "neutral" | "navy" | "emerald" | "gold" | "danger" | "outline";
const tones: Record<Tone, string> = {
  neutral: "bg-gray-bg text-ink border-line",
  navy: "bg-navy-50 text-navy border-navy/20",
  emerald: "bg-emerald-50 text-emerald border-emerald/30",
  gold: "bg-gold-50 text-[#7a5a0c] border-gold/40",
  danger: "bg-danger-50 text-danger border-danger/30",
  outline: "bg-white text-muted border-line",
};

export function Badge({ tone = "neutral", className, ...props }: React.HTMLAttributes<HTMLSpanElement> & { tone?: Tone }) {
  return <span className={cn("inline-flex items-center whitespace-nowrap rounded-full border px-2 py-0.5 text-xs font-medium", tones[tone], className)} {...props} />;
}
