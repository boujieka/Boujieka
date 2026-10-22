import * as React from "react";
import { cn } from "@/lib/utils";

type Variant = "primary" | "secondary" | "outline" | "ghost" | "danger";
const variants: Record<Variant, string> = {
  primary: "bg-navy text-white hover:bg-navy-700",
  secondary: "bg-emerald text-white hover:brightness-110",
  outline: "border border-line bg-white text-navy hover:bg-navy-50",
  ghost: "text-navy hover:bg-navy-50",
  danger: "bg-danger text-white hover:brightness-110",
};

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  size?: "sm" | "md";
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(function Button(
  { className, variant = "primary", size = "md", type = "button", ...props },
  ref,
) {
  return (
    <button
      ref={ref}
      type={type}
      className={cn(
        "inline-flex items-center justify-center gap-2 rounded-md font-medium transition disabled:cursor-not-allowed disabled:opacity-50",
        size === "sm" ? "px-2.5 py-1 text-sm" : "px-4 py-2 text-sm",
        variants[variant],
        className,
      )}
      {...props}
    />
  );
});

export function buttonClass(variant: Variant = "primary", size: "sm" | "md" = "md", className?: string) {
  return cn(
    "inline-flex items-center justify-center gap-2 rounded-md font-medium no-underline transition",
    size === "sm" ? "px-2.5 py-1 text-sm" : "px-4 py-2 text-sm",
    variants[variant],
    className,
  );
}
