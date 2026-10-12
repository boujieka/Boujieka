import Link from "next/link";
import { cn } from "@/lib/utils";

/** Wordmark: ACCESS360 AFRICA. Own mark only; no third party logos. */
export function Brand({ href = "/", inverted = false, className }: { href?: string; inverted?: boolean; className?: string }) {
  return (
    <Link href={href} className={cn("flex items-center gap-2 font-semibold tracking-tight", inverted ? "text-white" : "text-navy-900", className)}>
      <svg viewBox="0 0 32 32" className="size-7 shrink-0" aria-hidden>
        <circle cx="16" cy="16" r="13" fill="none" stroke="currentColor" strokeWidth="2.5" />
        <path d="M16 3 a13 13 0 0 1 13 13" fill="none" stroke="#0f8a5f" strokeWidth="2.5" />
        <path d="M17.5 8 L11 17.5 h5 L14.5 24 L21 14.5 h-5 Z" fill="#c8962e" />
      </svg>
      <span className="text-[15px] leading-none">
        ACCESS360 <span className={inverted ? "text-gold-500" : "text-emerald-700"}>AFRICA</span>
      </span>
    </Link>
  );
}
