import type { Metadata } from "next";

import { Nav } from "@/components/nav";
import { SyntheticBanner } from "@/components/provenance";
import { api } from "@/lib/api";

import "./globals.css";

export const metadata: Metadata = {
  title: "Cartouche · African Bond Intelligence",
  description: "Africa's Sovereign Debt Opportunity Engine — source-first sovereign debt market intelligence.",
};

export const dynamic = "force-dynamic";

async function hasSyntheticData(): Promise<boolean> {
  try {
    return (await api.summary()).synthetic_records_present;
  } catch {
    return false;
  }
}

export default async function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  const synthetic = await hasSyntheticData();
  return (
    <html lang="en">
      <body className="min-h-screen antialiased">
        <a href="#main" className="sr-only focus:not-sr-only focus:absolute focus:p-2">
          Skip to content
        </a>
        {synthetic && <SyntheticBanner />}
        <Nav />
        <main id="main" className="mx-auto max-w-[1400px] px-4 py-5">
          {children}
        </main>
        <footer className="mx-auto max-w-[1400px] border-t border-border px-4 py-4 text-xs text-muted">
          Information and analytics only. Not investment advice, not a recommendation, and no guarantee of
          returns or of access to any market. Values are labelled{" "}
          <strong>FACT</strong> (as published), <strong>CALC</strong> (derived), <strong>ESTIMATE</strong>,{" "}
          <strong>AI</strong> or <strong>SYNTHETIC</strong>.
        </footer>
      </body>
    </html>
  );
}
