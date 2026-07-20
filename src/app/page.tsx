import Link from "next/link";
import { Wordmark, SolarDisc } from "@/components/logo";
import { getSession } from "@/lib/auth/session";

export default async function LandingPage() {
  const session = await getSession();

  // Les neuf modules — séquence réelle de la chaîne d'origination.
  const modules: { t: string; d: string; accent: "gold" | "vert" }[] = [
    { t: "Profils offtakers & sites", d: "Sites, courbe de charge horaire, criticité de la charge et coût des coupures, étapes de pipeline.", accent: "gold" },
    { t: "Profils développeurs", d: "Zones, technologies (solaire, stockage, hybride), taille de projet, track record.", accent: "gold" },
    { t: "Pré-faisabilité", d: "Productible NASA POWER, simulation horaire sur 8760 h, dimensionnement à fiabilité cible.", accent: "vert" },
    { t: "Technico-économique", d: "CAPEX, tarif PPA, TRI, payback, économie annuelle contre le réseau.", accent: "gold" },
    { t: "Décarbonisation", d: "tCO₂ évitées via le facteur d'émission par pays, suivi de portefeuille.", accent: "vert" },
    { t: "Bancabilité & résilience", d: "Score intégrant explicitement la dimension sécurité d'approvisionnement.", accent: "vert" },
    { t: "Moteur de matching", d: "Pondération géographie, taille, capacité hybride et score, avec filtres durs.", accent: "gold" },
    { t: "Intérêt & messagerie", d: "Expression d'intérêt et échanges intermédiés entre les deux faces.", accent: "gold" },
    { t: "API Claude (serveur)", d: "Qualification, notes de concept chiffrées et explication des recommandations de matching.", accent: "vert" },
  ];

  return (
    <div className="min-h-screen bg-navy-700 text-white">
      {/* Barre */}
      <header className="sticky top-0 z-20 border-b border-white/10 bg-navy-800/80 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-3.5">
          <span className="[&_*]:!text-white">
            <Wordmark />
          </span>
          <nav className="flex items-center gap-3 text-sm">
            {session ? (
              <Link href="/dashboard" className="btn-gold">Tableau de bord</Link>
            ) : (
              <>
                <Link href="#modules" className="hidden text-navy-100 hover:text-white sm:inline">Modules</Link>
                <Link href="/login" className="text-navy-100 hover:text-white">Connexion</Link>
                <Link href="/register" className="btn-gold">Créer un compte</Link>
              </>
            )}
          </nav>
        </div>
      </header>

      {/* Hero */}
      <section className="relative overflow-hidden">
        <div
          className="pointer-events-none absolute inset-0 -z-10"
          style={{
            background:
              "radial-gradient(120% 80% at 82% -10%, rgba(201,162,39,.20), transparent 55%)," +
              "radial-gradient(90% 70% at 8% 110%, rgba(31,163,106,.16), transparent 55%)," +
              "linear-gradient(180deg, #0a1e3f, #07162f)",
          }}
        />
        <SolarDisc className="pointer-events-none absolute -right-40 -top-28 -z-10 h-[560px] w-[560px] opacity-90 max-lg:opacity-40" />

        <div className="mx-auto grid max-w-6xl items-center gap-12 px-6 py-20 lg:grid-cols-[1.35fr,1fr] lg:py-24">
          <div>
            <p className="mb-3 inline-flex items-center gap-2 rounded-full bg-white/10 px-3 py-1 text-xs font-medium uppercase tracking-widest text-gold-200">
              Énergie renouvelable C&amp;I · Afrique centrale
            </p>
            <h1 className="text-balance text-4xl font-semibold leading-[1.05] tracking-tight sm:text-5xl">
              Originer et mettre en relation les projets solaire&nbsp;+&nbsp;stockage, sur deux objectifs mesurés.
            </h1>
            <p className="mt-5 max-w-[42ch] text-lg text-navy-100">
              ATEN relie entreprises consommatrices et développeurs. Chaque opportunité est chiffrée sur la{" "}
              <span className="font-semibold text-vert-300">décarbonisation</span> — tCO₂ évitées — et la{" "}
              <span className="font-semibold text-gold-200">sécurité d'approvisionnement</span> : taux de couverture,
              déficit résiduel, coût de la fiabilité.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link href={session ? "/dashboard" : "/register"} className="btn-gold text-base">Commencer</Link>
              <Link href="/login" className="btn border border-white/25 text-white hover:bg-white/10">
                J'ai déjà un compte
              </Link>
            </div>
            <p className="mt-6 text-sm text-navy-200">
              Démo : <code className="rounded bg-gold-500/10 px-1.5 py-0.5 text-gold-200">offtaker@aten.demo</code> ·{" "}
              <code className="rounded bg-gold-500/10 px-1.5 py-0.5 text-gold-200">developer@aten.demo</code> ·{" "}
              <code className="rounded bg-gold-500/10 px-1.5 py-0.5 text-gold-200">admin@aten.demo</code> — mot de passe <code>demo1234</code>
            </p>
          </div>

          {/* Les deux objectifs mesurés */}
          <div className="grid gap-4">
            <ObjectiveCard
              accent="vert"
              tag="Décarbonisation"
              metric="tCO₂ évitées / an"
              sub="Facteur d'émission réseau par pays · suivi de portefeuille"
            />
            <ObjectiveCard
              accent="gold"
              tag="Sécurité d'approvisionnement"
              metric="Taux de couverture cible"
              sub="Simulation horaire 8760 pas · déficit résiduel · coût de la fiabilité"
            />
          </div>
        </div>
      </section>

      {/* Au cœur d'ATEN — les deux algorithmes */}
      <section className="border-y border-white/10 bg-navy-800">
        <div className="mx-auto grid max-w-6xl gap-10 px-6 py-12 lg:grid-cols-2">
          <AlgoBlock
            eyebrow="Au cœur d'ATEN — algorithme 1"
            title="Dimensionnement à fiabilité cible"
            body="Simulation horaire pure du bilan énergétique sur une année type ; la puissance solaire est fixée par un facteur de surdimensionnement, la capacité batterie ajustée par dichotomie jusqu'au taux de couverture imposé. Sorties : couverture atteinte, déficit résiduel, appoint, coût de la fiabilité."
          />
          <AlgoBlock
            eyebrow="Au cœur d'ATEN — algorithme 2"
            title="Score de compatibilité du matching"
            body="Quatre dimensions pondérées — géographie, technologie, taille, bancabilité — avec filtres durs appliqués avant tout calcul : hors zone géographique, ou hybride requis sans capacité de stockage, la compatibilité est nulle. Les développeurs sont classés par score décroissant."
          />
        </div>
      </section>

      {/* Neuf modules */}
      <section id="modules" className="bg-navy-50 py-20 text-navy-800">
        <div className="mx-auto max-w-6xl px-6">
          <h2 className="text-balance text-2xl font-semibold sm:text-3xl">Neuf modules, une chaîne d'origination</h2>
          <p className="mt-2 max-w-[52ch] text-navy-500">
            De la donnée de site à la mise en relation validée — chaque étape alimente la suivante, et la qualité de
            l'origination détermine la pertinence des appariements.
          </p>
          <div className="mt-9 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {modules.map((m, i) => (
              <article
                key={m.t}
                className="group rounded-xl border border-navy-100 bg-white p-5 transition hover:-translate-y-0.5 hover:border-navy-200 hover:shadow-card"
              >
                <span className={`block h-[3px] w-7 rounded ${m.accent === "vert" ? "bg-vert" : "bg-gold"}`} />
                <div className={`mt-3 text-xs font-bold tracking-wider ${m.accent === "vert" ? "text-vert-600" : "text-gold-600"}`}>
                  0{i + 1}
                </div>
                <h3 className="mt-1 font-semibold text-navy-800">{m.t}</h3>
                <p className="mt-1 text-sm text-navy-500">{m.d}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <footer className="bg-navy-900 py-8">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-2 px-6 text-sm text-navy-300">
          <span>ATEN — Le disque solaire</span>
          <span>Décarbonisation &amp; sécurité d'approvisionnement · Charte navy / or / vert</span>
        </div>
      </footer>
    </div>
  );
}

function ObjectiveCard({
  accent,
  tag,
  metric,
  sub,
}: {
  accent: "gold" | "vert";
  tag: string;
  metric: string;
  sub: string;
}) {
  return (
    <div className="rounded-2xl border border-white/10 bg-gradient-to-b from-white/[0.06] to-white/[0.015] p-5">
      <span className={`inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-widest ${accent === "vert" ? "text-vert-300" : "text-gold-200"}`}>
        <span className={`h-2 w-2 rounded-full ${accent === "vert" ? "bg-vert" : "bg-gold"}`} />
        {tag}
      </span>
      <div className="mt-2.5 text-2xl font-semibold tracking-tight tabular-nums">{metric}</div>
      <div className="mt-1 text-sm text-navy-200">{sub}</div>
    </div>
  );
}

function AlgoBlock({ eyebrow, title, body }: { eyebrow: string; title: string; body: string }) {
  return (
    <div>
      <div className="text-xs font-medium uppercase tracking-widest text-navy-200">{eyebrow}</div>
      <h3 className="mt-2 text-lg font-semibold text-gold-200">{title}</h3>
      <p className="mt-2.5 max-w-[46ch] text-navy-200">{body}</p>
    </div>
  );
}
