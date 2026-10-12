"use client";
import { useId, type ReactNode } from "react";
import { Label } from "@/components/ui/label";
import { cn } from "@/lib/utils";

/** Labelled form control with an error message wired through aria-describedby. */
export function Field({
  label,
  error,
  hint,
  className,
  children,
}: {
  label: ReactNode;
  error?: string;
  hint?: ReactNode;
  className?: string;
  children: (id: string, describedBy: string | undefined, invalid: boolean) => ReactNode;
}) {
  const id = useId();
  const errId = `${id}-err`;
  const hintId = `${id}-hint`;
  const describedBy = [error ? errId : null, hint ? hintId : null].filter(Boolean).join(" ") || undefined;
  return (
    <div className={cn("flex flex-col gap-1", className)}>
      <Label htmlFor={id}>{label}</Label>
      {children(id, describedBy, !!error)}
      {hint ? (
        <p id={hintId} className="text-xs text-subtle-foreground">
          {hint}
        </p>
      ) : null}
      {error ? (
        <p id={errId} className="text-xs text-danger-700">
          {error}
        </p>
      ) : null}
    </div>
  );
}
