import type { ReactNode } from "react";
import { Nav } from "@/components/nav";

/** Wraps every authenticated page: nav + bottom padding so content never
 * sits behind the fixed mobile tab bar (see Nav's comment). */
export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-screen flex-col bg-zinc-50 dark:bg-zinc-950">
      <Nav />
      <div className="flex-1 pb-20 sm:pb-0">{children}</div>
    </div>
  );
}
