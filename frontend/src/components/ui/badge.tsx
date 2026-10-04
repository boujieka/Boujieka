import { cva, type VariantProps } from "class-variance-authority";
import * as React from "react";

import { cn } from "@/lib/utils";

const badgeVariants = cva(
  "inline-flex items-center gap-1 rounded-sm border px-1.5 py-px text-[11px] font-medium leading-4 whitespace-nowrap",
  {
    variants: {
      variant: {
        neutral: "border-border-strong text-muted",
        fact: "border-[var(--nature-fact)] text-[var(--nature-fact)]",
        calc: "border-[var(--nature-calc)] text-[var(--nature-calc)]",
        estimate: "border-[var(--nature-estimate)] text-[var(--nature-estimate)]",
        ai: "border-[var(--nature-ai)] text-[var(--nature-ai)]",
        synthetic:
          "border-[var(--nature-synthetic)] text-[var(--nature-synthetic)] font-semibold",
        good: "border-good text-good",
        warning: "border-warning text-warning",
        critical: "border-critical text-critical",
      },
    },
    defaultVariants: { variant: "neutral" },
  },
);

export function Badge({
  className,
  variant,
  ...props
}: React.ComponentProps<"span"> & VariantProps<typeof badgeVariants>) {
  return <span className={cn(badgeVariants({ variant }), className)} {...props} />;
}
