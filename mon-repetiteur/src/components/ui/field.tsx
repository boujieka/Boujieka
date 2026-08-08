import type { InputHTMLAttributes } from "react";
import { cn } from "@/lib/cn";

export function Field({
  label,
  className,
  ...props
}: InputHTMLAttributes<HTMLInputElement> & { label: string }) {
  return (
    <label className="flex flex-col gap-1.5 text-sm font-medium text-zinc-700 dark:text-zinc-300">
      {label}
      <input
        className={cn(
          // text-base (16px), not text-sm: Safari auto-zooms on focusing
          // any input under 16px, which is jarring on mobile.
          "rounded-lg border border-zinc-300 bg-white px-3 py-2.5 text-base text-zinc-950 placeholder:text-zinc-400",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:ring-offset-2",
          "dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-50 dark:focus-visible:ring-offset-zinc-950",
          className,
        )}
        {...props}
      />
    </label>
  );
}
