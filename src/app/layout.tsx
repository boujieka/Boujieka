import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ATEN — Le disque solaire",
  description:
    "Plateforme d'origination et de mise en relation pour projets d'énergie renouvelable C&I. Décarbonisation et sécurité d'approvisionnement, mesurées.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <body>{children}</body>
    </html>
  );
}
