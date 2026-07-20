import Link from "next/link";
import type { ReactNode } from "react";

export function Card({
  children,
  className = "",
}: {
  children: ReactNode;
  className?: string;
}) {
  return <div className={`card ${className}`}>{children}</div>;
}

export function SectionTitle({ children, action }: { children: ReactNode; action?: ReactNode }) {
  return (
    <div className="mb-4 flex items-center justify-between">
      <h2 className="text-lg font-semibold text-navy-800">{children}</h2>
      {action}
    </div>
  );
}

/** Tuile de statistique — accent gold/vert/navy. */
export function Stat({
  label,
  value,
  hint,
  accent = "navy",
}: {
  label: string;
  value: ReactNode;
  hint?: string;
  accent?: "navy" | "gold" | "vert";
}) {
  const ring =
    accent === "gold"
      ? "border-l-gold"
      : accent === "vert"
        ? "border-l-vert"
        : "border-l-navy";
  return (
    <div className={`card border-l-4 ${ring}`}>
      <div className="text-xs font-medium uppercase tracking-wide text-navy-400">{label}</div>
      <div className="mt-1 text-2xl font-semibold text-navy-800">{value}</div>
      {hint && <div className="mt-1 text-xs text-navy-400">{hint}</div>}
    </div>
  );
}

export function RatingBadge({ rating }: { rating: "A" | "B" | "C" | "D" | string }) {
  const cls =
    rating === "A" ? "rating-A" : rating === "B" ? "rating-B" : rating === "C" ? "rating-C" : "rating-D";
  return <span className={cls}>Bancabilité {rating}</span>;
}

export function Badge({
  children,
  tone = "navy",
}: {
  children: ReactNode;
  tone?: "navy" | "gold" | "vert" | "muted";
}) {
  const cls =
    tone === "gold" ? "badge-gold" : tone === "vert" ? "badge-vert" : tone === "muted" ? "badge-muted" : "badge-navy";
  return <span className={cls}>{children}</span>;
}

export function LinkButton({
  href,
  children,
  variant = "primary",
}: {
  href: string;
  children: ReactNode;
  variant?: "primary" | "gold" | "vert" | "ghost";
}) {
  const cls =
    variant === "gold"
      ? "btn-gold"
      : variant === "vert"
        ? "btn-vert"
        : variant === "ghost"
          ? "btn-ghost"
          : "btn-primary";
  return (
    <Link href={href} className={cls}>
      {children}
    </Link>
  );
}

export function EmptyState({ title, children }: { title: string; children?: ReactNode }) {
  return (
    <div className="rounded-xl border border-dashed border-navy-200 bg-white/60 p-8 text-center">
      <p className="font-medium text-navy-700">{title}</p>
      {children && <div className="mt-2 text-sm text-navy-500">{children}</div>}
    </div>
  );
}

export function Field({
  label,
  name,
  type = "text",
  required,
  defaultValue,
  placeholder,
  step,
  min,
  max,
  hint,
}: {
  label: string;
  name: string;
  type?: string;
  required?: boolean;
  defaultValue?: string | number;
  placeholder?: string;
  step?: string;
  min?: string;
  max?: string;
  hint?: string;
}) {
  return (
    <div>
      <label className="label" htmlFor={name}>
        {label} {required && <span className="text-gold-600">*</span>}
      </label>
      <input
        id={name}
        name={name}
        type={type}
        required={required}
        defaultValue={defaultValue}
        placeholder={placeholder}
        step={step}
        min={min}
        max={max}
        className="input"
      />
      {hint && <p className="mt-1 text-xs text-navy-400">{hint}</p>}
    </div>
  );
}
