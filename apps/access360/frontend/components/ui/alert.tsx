import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const alertVariants = cva("flex gap-2 rounded-md border px-3 py-2 text-sm [&_svg]:mt-0.5 [&_svg]:size-4 [&_svg]:shrink-0", {
  variants: {
    variant: {
      info: "border-navy-100 bg-navy-50 text-navy-900",
      success: "border-emerald-100 bg-emerald-50 text-emerald-700",
      warning: "border-gold-100 bg-gold-50 text-gold-700",
      danger: "border-danger-100 bg-danger-100 text-danger-700",
    },
  },
  defaultVariants: { variant: "info" },
});

export interface AlertProps extends React.HTMLAttributes<HTMLDivElement>, VariantProps<typeof alertVariants> {}

export function Alert({ className, variant, role, ...p }: AlertProps) {
  return <div role={role ?? (variant === "danger" ? "alert" : "status")} className={cn(alertVariants({ variant }), className)} {...p} />;
}
