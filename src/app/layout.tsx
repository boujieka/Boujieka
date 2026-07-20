import type { Metadata } from "next";
import "./globals.css";

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000";
const TITLE = "ATEN — Le disque solaire";
const DESCRIPTION =
  "Chiffrez un projet solaire + stockage C&I avant d'engager : taux de couverture, économies contre le réseau et CO₂ évité — puis mise en relation avec les bons développeurs.";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: { default: TITLE, template: "%s · ATEN" },
  description: DESCRIPTION,
  applicationName: "ATEN",
  keywords: [
    "énergie renouvelable",
    "solaire",
    "stockage",
    "C&I",
    "PPA",
    "décarbonisation",
    "sécurité d'approvisionnement",
    "origination",
    "Afrique centrale",
  ],
  openGraph: {
    type: "website",
    locale: "fr_FR",
    url: SITE_URL,
    siteName: TITLE,
    title: TITLE,
    description: DESCRIPTION,
  },
  twitter: {
    card: "summary_large_image",
    title: TITLE,
    description: DESCRIPTION,
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <body>{children}</body>
    </html>
  );
}
