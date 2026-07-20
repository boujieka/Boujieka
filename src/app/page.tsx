import Link from "next/link";
import { Wordmark, SolarDisc } from "@/components/logo";
import { HeroPreview } from "@/components/hero-preview";
import { getSession } from "@/lib/auth/session";

export default async function LandingPage() {
  const session = await getSession();

  // La chaîne d'origination, groupée par ses trois phases réelles.
  const phases: { phase: string; items: { t: string; d: string }[] }[] = [
    {
      phase: "Origination",
      items: [
        { t: "Profils offtakers & sites", d: "Charge horaire, criticité, coût des coupures, pipeline." },
        { t: "Profils développeurs", d: "Zones, technologies, taille de projet, track record." },
      ],
    },
    {
      phase: "Analyse",
      items: [
        { t: "Pré-faisabilité", d: "Productible NASA POWER, simulation 8760 h, dimensionnement à fiabilité cible." },
        { t: "Technico-économique", d: "CAPEX, tarif PPA, TRI, payback, économies." },
        { t: "Décarbonisation", d: "tCO₂ évitées via le facteur d'émission par pays." },
        { t: "Bancabilité", d: "Score financier, technique et de résilience." },
      ],
    },
    {
      phase: "Mise en relation",
      items: [
        { t: "Matching pondéré", d: "Géographie, taille, hybride et score, avec filtres durs." },
        { t: "Intérêt & messagerie", d: "Échanges intermédiés entre les deux faces." },
        { t: "Assistance IA", d: "Qualification, notes de concept chiffrées, explications." },
      ],
    },
  ];

  return (
    <div className="min-h-screen bg-white text-navy-800">
      {/* Barre */}
      <header className="sticky top-0 z-20 border-b border-navy-100 bg-white/85 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <Wordmark />
          <nav className="flex items-center gap-4 text-sm">
            <Link href="#pour-qui" className="hidden text-navy-500 hover:text-navy-800 sm:inline">Pour qui</Link>
            <Link href="#methode" className="hidden text-navy-500 hover:text-navy-800 sm:inline">Méthode</Link>
            {session ? (
              <Link href="/dashboard" className="btn-primary">Tableau de bord</Link>
            ) : (
              <>
                <Link href="/login" className="text-navy-600 hover:text-navy-900">Connexion</Link>
                <Link href="/register" className="btn-primary">Créer un compte</Link>
              </>
            )}
          </nav>
        </div>
      </header>

      {/* Hero — orienté résultat */}
      <section className="relative overflow-hidden bg-navy-700 text-white">
        <div className="pointer-events-none absolute inset-0 -z-10" style={{ background: "linear-gradient(180deg, #0a1e3f 0%, #0b2148 100%)" }} />
        <SolarDisc className="pointer-events-none absolute -right-24 top-10 -z-10 h-72 w-72 opacity-20" />
        <div className="mx-auto grid max-w-6xl items-center gap-12 px-6 py-20 lg:grid-cols-[1.15fr,0.85fr]">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-gold-200">
              Pré-faisabilité &amp; origination · solaire + stockage C&amp;I
            </p>
            <h1 className="mt-4 text-balance text-4xl font-semibold leading-[1.08] tracking-tight sm:text-5xl">
              Moins de coupures, une facture maîtrisée, chaque tonne de CO₂ prouvée.
            </h1>
            <p className="mt-4 text-lg font-medium text-gold-200">
              Le chiffrage de pré-faisabilité qui valorise votre résilience.
            </p>
            <p className="mt-4 max-w-[56ch] text-lg text-navy-100">
              Pour les entreprises consommatrices : ATEN chiffre un projet solaire + stockage
              <span className="font-semibold text-white"> avant d'engager</span> — taux de couverture, économies
              contre le réseau et CO₂ évité — puis met l'opportunité qualifiée en relation avec les bons développeurs.
            </p>

            {/* CTA principal — face offtaker prioritaire */}
            <div className="mt-8 flex flex-wrap items-center gap-3">
              <Link href={session ? "/sites/new" : "/register"} className="btn-gold text-base">Évaluer un site</Link>
              <Link href="/login" className="btn border border-white/25 text-white hover:bg-white/10">Connexion</Link>
            </div>
            {/* Entrée secondaire — face développeur */}
            <p className="mt-5 text-sm text-navy-200">
              Vous développez des projets ?{" "}
              <Link
                href={session ? "/opportunities" : "/register"}
                className="font-medium text-vert-300 underline decoration-vert-300/40 underline-offset-4 hover:decoration-vert-300"
              >
                Accéder aux opportunités qualifiées →
              </Link>
            </p>
          </div>
          <div className="lg:justify-self-end lg:max-w-sm">
            <HeroPreview />
          </div>
        </div>
      </section>

      {/* Bande de crédibilité — méthode, pas déclaratif */}
      <section className="border-b border-navy-100 bg-navy-800 text-white">
        <div className="mx-auto grid max-w-6xl grid-cols-2 gap-6 px-6 py-8 sm:grid-cols-4">
          <Proof k="8760 pas" v="Simulation horaire du bilan énergétique sur une année type." />
          <Proof k="NASA POWER" v="Productible solaire à partir de l'irradiation du site." />
          <Proof k="Facteur pays" v="CO₂ évité via le facteur d'émission réseau national." />
          <Proof k="Modèle intermédié" v="Mise en relation validée par l'opérateur de la plateforme." />
        </div>
      </section>

      {/* Deux objectifs mesurés */}
      <section className="border-b border-navy-100 bg-navy-50">
        <div className="mx-auto max-w-6xl px-6 py-14">
          <p className="text-xs font-semibold uppercase tracking-widest text-navy-400">Deux objectifs, mesurés — pas déclarés</p>
          <div className="mt-6 grid gap-6 md:grid-cols-2">
            <Objective
              accent="gold"
              label="Sécurité d'approvisionnement"
              headline="Taux de couverture"
              body="Issu d'une simulation horaire sur 8760 pas, avec déficit résiduel et coût de la fiabilité chiffrés."
            />
            <Objective
              accent="vert"
              label="Décarbonisation"
              headline="tCO₂ évitées"
              body="Calculées via le facteur d'émission réseau du pays, auditables et agrégées au portefeuille."
            />
          </div>
        </div>
      </section>

      {/* Pour qui — valeur par face */}
      <section id="pour-qui" className="mx-auto max-w-6xl px-6 py-16">
        <h2 className="text-balance text-2xl font-semibold sm:text-3xl">Une plateforme, deux faces</h2>
        <div className="mt-8 grid gap-6 md:grid-cols-2">
          <AudienceCard
            accent="gold"
            title="Offtakers — entreprises consommatrices"
            points={[
              "Un chiffrage indépendant avant tout engagement contractuel",
              "La valeur de la résilience intégrée : coût des coupures et couverture cible",
              "Un dossier prêt à discuter : note de concept, économies, CO₂ évité",
            ]}
          />
          <AudienceCard
            accent="vert"
            title="Développeurs — firmes de projet"
            points={[
              "Un flux d'opportunités C&I pré-qualifiées, pas des pistes froides",
              "Un appariement pondéré sur votre zone, votre taille et vos technologies",
              "Un score de bancabilité pour prioriser vos efforts commerciaux",
            ]}
          />
        </div>
      </section>

      {/* Méthode — la chaîne d'origination */}
      <section id="methode" className="border-t border-navy-100 bg-navy-50 py-16">
        <div className="mx-auto max-w-6xl px-6">
          <h2 className="text-balance text-2xl font-semibold sm:text-3xl">De la donnée de site à la mise en relation</h2>
          <p className="mt-2 max-w-[56ch] text-navy-500">
            Chaque phase alimente la suivante&nbsp;: la qualité de l'origination détermine la pertinence des appariements.
          </p>
          <div className="mt-10 grid gap-6 lg:grid-cols-3">
            {phases.map((p, i) => (
              <div key={p.phase} className="rounded-xl border border-navy-100 bg-white p-6 shadow-card">
                <div className="flex items-baseline gap-2">
                  <span className="text-sm font-bold tabular-nums text-gold-600">0{i + 1}</span>
                  <h3 className="text-lg font-semibold text-navy-800">{p.phase}</h3>
                </div>
                <ul className="mt-4 space-y-4">
                  {p.items.map((it) => (
                    <li key={it.t} className="border-l-2 border-navy-100 pl-3">
                      <div className="font-medium text-navy-800">{it.t}</div>
                      <div className="text-sm text-navy-500">{it.d}</div>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA final */}
      <section className="border-t border-navy-100 bg-navy-700 text-white">
        <div className="mx-auto flex max-w-6xl flex-col items-start justify-between gap-6 px-6 py-14 sm:flex-row sm:items-center">
          <div>
            <h2 className="text-2xl font-semibold">Chiffrez votre premier projet</h2>
            <p className="mt-1 text-navy-100">Créez un compte offtaker ou développeur en quelques minutes.</p>
          </div>
          <Link href={session ? "/dashboard" : "/register"} className="btn-gold text-base">
            {session ? "Ouvrir le tableau de bord" : "Créer un compte"}
          </Link>
        </div>
      </section>

      <footer className="bg-navy-900 py-8">
        <div className="mx-auto max-w-6xl px-6">
          <div className="flex flex-wrap items-center justify-between gap-2 text-sm text-navy-300">
            <span className="[&_*]:!text-white">
              <Wordmark />
            </span>
            <span>Décarbonisation &amp; sécurité d'approvisionnement · méthodologie transparente</span>
          </div>
          <p className="mt-4 border-t border-white/10 pt-4 text-xs text-navy-400">
            Les chiffrages présentés (taux de couverture, économies, CO₂ évité, dimensionnement) sont des
            estimations de pré-faisabilité fondées sur des données publiques et des hypothèses paramétrables.
            Ils ne constituent pas une offre ni un engagement contractuel.
          </p>
        </div>
      </footer>
    </div>
  );
}

function Proof({ k, v }: { k: string; v: string }) {
  return (
    <div>
      <div className="text-sm font-semibold text-gold-200">{k}</div>
      <div className="mt-1 text-xs leading-relaxed text-navy-200">{v}</div>
    </div>
  );
}

function Objective({ accent, label, headline, body }: { accent: "gold" | "vert"; label: string; headline: string; body: string }) {
  return (
    <div className="rounded-xl border border-navy-100 bg-white p-6 shadow-card">
      <span className={`inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-widest ${accent === "vert" ? "text-vert-700" : "text-gold-700"}`}>
        <span className={`h-2 w-2 rounded-full ${accent === "vert" ? "bg-vert" : "bg-gold"}`} />
        {label}
      </span>
      <div className="mt-3 text-3xl font-semibold tracking-tight text-navy-800">{headline}</div>
      <p className="mt-2 max-w-[42ch] text-navy-500">{body}</p>
    </div>
  );
}

function AudienceCard({ accent, title, points }: { accent: "gold" | "vert"; title: string; points: string[] }) {
  return (
    <div className="rounded-xl border border-navy-100 bg-white p-6 shadow-card">
      <div className="flex items-center gap-2">
        <span className={`h-2.5 w-2.5 rounded-full ${accent === "vert" ? "bg-vert" : "bg-gold"}`} />
        <h3 className="text-lg font-semibold text-navy-800">{title}</h3>
      </div>
      <ul className="mt-4 space-y-2.5">
        {points.map((p) => (
          <li key={p} className="flex gap-2 text-sm text-navy-600">
            <span className={`mt-2 h-1.5 w-1.5 shrink-0 rounded-full ${accent === "vert" ? "bg-vert-300" : "bg-gold-300"}`} />
            {p}
          </li>
        ))}
      </ul>
    </div>
  );
}
