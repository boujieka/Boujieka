import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const badgeVariants = cva("inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-xs font-medium whitespace-nowrap [&_svg]:size-3", {
  variants: {
    variant: {
      neutral: "border-border bg-surface-muted text-muted-foreground",
      navy: "border-navy-100 bg-navy-50 text-navy-800",
      success: "border-emerald-100 bg-emerald-50 text-emerald-700",
      warning: "border-warning-100 bg-warning-100 text-warning-700",
      danger: "border-danger-100 bg-danger-100 text-danger-700",
      gold: "border-gold-100 bg-gold-50 text-gold-700",
    },
  },
  defaultVariants: { variant: "neutral" },
});

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement>, VariantProps<typeof badgeVariants> {}

export function Badge({ className, variant, ...props }: BadgeProps) {
  return <span className={cn(badgeVariants({ variant }), className)} {...props} />;
}
