import { ImageResponse } from "next/og";

/**
 * Image de partage Open Graph (1200×630), générée à la volée par next/og.
 * Aucune ressource externe — charte navy/or/vert, identité « disque solaire ».
 */
export const runtime = "edge";
export const alt = "ATEN — chiffrer un projet solaire + stockage C&I avant d'engager";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default function OpengraphImage() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          padding: "72px",
          background: "linear-gradient(135deg, #0a1e3f 0%, #0b2148 100%)",
          color: "#ffffff",
          fontFamily: "sans-serif",
        }}
      >
        {/* Marque */}
        <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
          <div
            style={{
              width: 56,
              height: 56,
              borderRadius: 999,
              background: "#0a1e3f",
              border: "3px solid #16305c",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <div style={{ width: 28, height: 28, borderRadius: 999, background: "#c9a227" }} />
          </div>
          <div style={{ display: "flex", alignItems: "baseline", gap: 10, fontSize: 30, fontWeight: 700, letterSpacing: -1 }}>
            <span>ATEN</span>
            <span style={{ color: "#93a6c6", fontWeight: 400 }}>· Le disque solaire</span>
          </div>
        </div>

        {/* Accroche */}
        <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
          <div style={{ fontSize: 30, color: "#e9d084", fontWeight: 600 }}>
            Pré-faisabilité &amp; origination · solaire + stockage C&amp;I
          </div>
          <div style={{ fontSize: 60, fontWeight: 700, lineHeight: 1.05, letterSpacing: -1.5, maxWidth: 1000 }}>
            Moins de coupures, une facture maîtrisée, chaque tonne de CO2 prouvée.
          </div>
        </div>

        {/* Deux objectifs mesurés */}
        <div style={{ display: "flex", gap: 16 }}>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 12,
              padding: "12px 22px",
              borderRadius: 999,
              background: "rgba(201,162,39,0.14)",
              color: "#e9d084",
              fontSize: 26,
              fontWeight: 600,
            }}
          >
            <div style={{ width: 14, height: 14, borderRadius: 999, background: "#c9a227" }} />
            Sécurité d'approvisionnement
          </div>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 12,
              padding: "12px 22px",
              borderRadius: 999,
              background: "rgba(31,163,106,0.16)",
              color: "#52c78e",
              fontSize: 26,
              fontWeight: 600,
            }}
          >
            <div style={{ width: 14, height: 14, borderRadius: 999, background: "#1fa36a" }} />
            Décarbonisation
          </div>
        </div>
      </div>
    ),
    { ...size },
  );
}
