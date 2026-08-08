type ClassValue = string | false | null | undefined;

/** Minimal className joiner — no tailwind-merge dedup logic needed here
 * since our variant maps never produce conflicting utilities for the
 * same property (CLAUDE.md §32: don't add a dependency for this). */
export function cn(...classes: ClassValue[]): string {
  return classes.filter(Boolean).join(" ");
}
