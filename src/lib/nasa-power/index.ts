/**
 * Productible solaire via NASA POWER.
 *
 * Récupère l'irradiation horaire (GHI, W/m²) sur une année type pour un point
 * (latitude, longitude), puis la convertit en productible photovoltaïque
 * y[h] (kWh par kWc et par pas) par un ratio de performance.
 *
 * Modèle simple « plan horizontal » : 1 kWc produit `PR × GHI/1000` kWh sous
 * GHI (W/m²). Ce modèle est volontairement transparent au stade de la
 * pré-faisabilité ; il pourra être raffiné (inclinaison, température) sans
 * changer l'interface.
 */

import { HOURS_PER_YEAR } from "../config";

export interface ProductibleResult {
  /** y[h] : productible par kWc (kWh/kWc) sur 8760 pas. */
  yieldPerKwp: number[];
  /** Productible spécifique annuel (kWh/kWc/an) = Σ y[h]. */
  specificYield: number;
  /** Année de données utilisée. */
  year: number;
  source: "nasa_power" | "synthetic";
}

const BASE_URL =
  process.env.NASA_POWER_BASE_URL ||
  "https://power.larc.nasa.gov/api/temporal/hourly/point";

/**
 * Convertit une série horaire d'irradiation globale horizontale (W/m²) en
 * productible par kWc (kWh/kWc) via le ratio de performance.
 */
export function irradianceToYield(ghiWm2: number[], performanceRatio: number): number[] {
  // 1 kWc = 1 kW sous 1000 W/m². Énergie sur 1 h = puissance × 1 h.
  return ghiWm2.map((ghi) => (Math.max(0, ghi) / 1000) * performanceRatio);
}

interface NasaPowerResponse {
  properties?: { parameter?: Record<string, Record<string, number>> };
}

/**
 * Récupère le productible horaire depuis NASA POWER pour un point donné.
 * Aucune clé requise (API publique). En cas d'échec réseau, l'appelant peut
 * se rabattre sur `syntheticProductible`.
 *
 * @param year Année météo à interroger (par défaut la dernière année complète
 *   disponible fournie par l'appelant).
 */
export async function fetchProductible(
  latitude: number,
  longitude: number,
  performanceRatio: number,
  year: number,
): Promise<ProductibleResult> {
  const params = new URLSearchParams({
    parameters: "ALLSKY_SFC_SW_DWN",
    community: "RE",
    longitude: String(longitude),
    latitude: String(latitude),
    start: `${year}0101`,
    end: `${year}1231`,
    format: "JSON",
    "time-standard": "LST",
  });

  const url = `${BASE_URL}?${params.toString()}`;
  const res = await fetch(url, { headers: { Accept: "application/json" } });
  if (!res.ok) {
    throw new Error(`NASA POWER a répondu ${res.status}`);
  }
  const data = (await res.json()) as NasaPowerResponse;
  const series = data.properties?.parameter?.ALLSKY_SFC_SW_DWN;
  if (!series) throw new Error("Réponse NASA POWER sans série ALLSKY_SFC_SW_DWN");

  // NASA POWER fournit l'irradiation en Wh/m² sur le pas horaire (≡ W/m² moyen).
  // Les clés sont AAAAMMJJHH ordonnées chronologiquement.
  const keys = Object.keys(series).sort();
  const ghi = keys.map((k) => {
    const v = series[k];
    return v === -999 || v == null ? 0 : v; // -999 = valeur manquante
  });

  // Normalise à 8760 pas (les années bissextiles en comptent 8784).
  const trimmed = ghi.slice(0, HOURS_PER_YEAR);
  while (trimmed.length < HOURS_PER_YEAR) trimmed.push(0);

  const yieldPerKwp = irradianceToYield(trimmed, performanceRatio);
  return {
    yieldPerKwp,
    specificYield: yieldPerKwp.reduce((a, b) => a + b, 0),
    year,
    source: "nasa_power",
  };
}

/**
 * Productible synthétique de repli (climat tropical) — cloche diurne calée sur
 * un productible spécifique annuel cible. Utilisé lorsque NASA POWER est
 * indisponible, pour ne pas bloquer la pré-faisabilité.
 */
export function syntheticProductible(
  performanceRatio: number,
  targetSpecificYield = 1750,
): ProductibleResult {
  const raw = new Array<number>(HOURS_PER_YEAR);
  let sum = 0;
  for (let h = 0; h < HOURS_PER_YEAR; h++) {
    const hod = h % 24;
    const x = (hod - 6) / 12; // journée solaire 6h→18h
    const v = x > 0 && x < 1 ? Math.sin(Math.PI * x) : 0;
    raw[h] = v;
    sum += v;
  }
  // Calibre pour que Σ y = targetSpecificYield × PR / PR ... on applique le PR
  // via l'échelle finale afin de refléter les pertes système.
  const scale = sum > 0 ? (targetSpecificYield / performanceRatio / sum) : 0;
  const yieldPerKwp = raw.map((v) => v * scale * performanceRatio);
  return {
    yieldPerKwp,
    specificYield: yieldPerKwp.reduce((a, b) => a + b, 0),
    year: 0,
    source: "synthetic",
  };
}
