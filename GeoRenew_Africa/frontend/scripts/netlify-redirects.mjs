// Génère dist/_redirects pour Netlify après le build.
// - /api/* est relayé (proxy, statut 200) vers l'API hébergée ailleurs si GEORENEW_API_ORIGIN est défini
//   (ex. https://georenew-api.exemple.org) ; le navigateur reste sur le domaine Netlify (pas de CORS).
// - Sans API configurée, /api/* renvoie 404 en JSON (réécriture documentée par Netlify) : l'interface affiche « API non configurée ».
// - Toutes les autres routes servent index.html (application monopage).
import { writeFileSync } from "node:fs";

const origin = (process.env.GEORENEW_API_ORIGIN ?? "").trim().replace(/\/+$/, "");
if (origin && !/^https:\/\/[a-z0-9.-]+(:\d+)?$/i.test(origin)) {
  console.error(`GEORENEW_API_ORIGIN invalide : ${origin} (attendu : https://hote[:port], sans chemin)`);
  process.exit(1);
}
const lines = [];
if (origin) lines.push(`/api/*  ${origin}/api/:splat  200`);
else lines.push("/api/*  /api-unconfigured.json  404");
lines.push("/*  /index.html  200");
writeFileSync("dist/_redirects", lines.join("\n") + "\n");
writeFileSync(
  "dist/api-unconfigured.json",
  JSON.stringify({ detail: { code: "api_non_configuree", message:
    "API GeoRenew non configurée pour ce déploiement : l'interface est en ligne mais le serveur d'API (FastAPI + PostGIS) n'est pas encore branché." } }) + "\n",
);
console.log(origin ? `Relais /api/* → ${origin}` : "Aucune API configurée : /api/* renvoie 404 (api_non_configuree)");
