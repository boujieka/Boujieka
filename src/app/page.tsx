import Link from "next/link";
import { Wordmark, SolarDisc } from "@/components/logo";
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
            <Link href="#chaine" className="hidden text-navy-500 hover:text-navy-800 sm:inline">La plateforme</Link>
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

      {/* Hero — sobre, navy */}
      <section className="relative overflow-hidden bg-navy-700 text-white">
        <div
          className="pointer-events-none absolute inset-0 -z-10"
          style={{ background: "linear-gradient(180deg, #0a1e3f 0%, #0b2148 100%)" }}
        />
        <SolarDisc className="pointer-events-none absolute -right-24 top-10 -z-10 h-72 w-72 opacity-25" />
        <div className="mx-auto max-w-6xl px-6 py-24">
          <div className="max-w-3xl">
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-gold-200">
              Plateforme d'origination — énergie renouvelable C&amp;I
            </p>
            <h1 className="mt-4 text-balance text-4xl font-semibold leading-[1.08] tracking-tight sm:text-5xl">
              Solaire et stockage pour l'industrie, chiffrés sur deux objectifs&nbsp;: décarboner et sécuriser l'approvisionnement.
            </h1>
            <p className="mt-6 max-w-[54ch] text-lg text-navy-100">
              ATEN relie entreprises consommatrices et développeurs. Chaque opportunité est instruite,
              dimensionnée et mise en relation sur des grandeurs mesurées, non des intentions.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link href={session ? "/dashboard" : "/register"} className="btn-gold text-base">Commencer</Link>
              <Link href="/login" className="btn border border-white/25 text-white hover:bg-white/10">Connexion</Link>
            </div>
          </div>
        </div>
      </section>

      {/* Deux objectifs mesurés — le cœur du produit */}
      <section className="border-b border-navy-100 bg-navy-50">
        <div className="mx-auto grid max-w-6xl gap-6 px-6 py-14 md:grid-cols-2">
          <Objective
            accent="vert"
            label="Décarbonisation"
            headline="tCO₂ évitées"
            body="Calculées via le facteur d'émission réseau du pays, agrégées au niveau du portefeuille."
          />
          <Objective
            accent="gold"
            label="Sécurité d'approvisionnement"
            headline="Taux de couverture"
            body="Issu d'une simulation horaire sur 8760 pas, avec déficit résiduel et coût de la fiabilité."
          />
        </div>
      </section>

      {/* La chaîne d'origination — 3 phases */}
      <section id="chaine" className="mx-auto max-w-6xl px-6 py-16">
        <h2 className="text-balance text-2xl font-semibold sm:text-3xl">De la donnée de site à la mise en relation</h2>
        <p className="mt-2 max-w-[56ch] text-navy-500">
          Chaque phase alimente la suivante&nbsp;: la qualité de l'origination détermine la pertinence des
          appariements.
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
      </section>

      {/* Appel à l'action final */}
      <section className="border-t border-navy-100 bg-navy-700 text-white">
        <div className="mx-auto flex max-w-6xl flex-col items-start justify-between gap-6 px-6 py-14 sm:flex-row sm:items-center">
          <div>
            <h2 className="text-2xl font-semibold">Prêt à originer votre premier projet&nbsp;?</h2>
            <p className="mt-1 text-navy-100">Créez un compte offtaker ou développeur en quelques minutes.</p>
          </div>
          <Link href={session ? "/dashboard" : "/register"} className="btn-gold text-base">
            {session ? "Ouvrir le tableau de bord" : "Créer un compte"}
          </Link>
        </div>
      </section>

      <footer className="bg-navy-900 py-8">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-2 px-6 text-sm text-navy-300">
          <span className="[&_*]:!text-white">
            <Wordmark />
          </span>
          <span>Décarbonisation &amp; sécurité d'approvisionnement</span>
        </div>
      </footer>
    </div>
  );
}

function Objective({
  accent,
  label,
  headline,
  body,
}: {
  accent: "gold" | "vert";
  label: string;
  headline: string;
  body: string;
}) {
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
