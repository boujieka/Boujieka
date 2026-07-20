import Link from "next/link";
import { Wordmark } from "@/components/logo";
import { getSession } from "@/lib/auth/session";

export default async function LandingPage() {
  const session = await getSession();

  const modules = [
    { t: "Profils offtakers & sites", d: "Sites, courbe de charge horaire, criticité et coût des coupures, pipeline d'origination." },
    { t: "Profils développeurs", d: "Zones, technologies (solaire, stockage, hybride), taille de projet, track record." },
    { t: "Pré-faisabilité", d: "Productible NASA POWER, simulation horaire sur 8760 h, dimensionnement à fiabilité cible." },
    { t: "Technico-économique", d: "CAPEX, tarif PPA, TRI, payback, économies contre réseau." },
    { t: "Décarbonisation", d: "tCO₂ évitées via facteur d'émission par pays, suivi de portefeuille." },
    { t: "Bancabilité & résilience", d: "Score intégrant la dimension sécurité d'approvisionnement." },
    { t: "Matching pondéré", d: "Géographie, taille, capacité hybride et score, avec filtres durs." },
    { t: "Intérêt & messagerie", d: "Expression d'intérêt et échanges entre les deux faces, intermédiés." },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-navy-700 to-navy-800 text-white">
      <header className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
        <span className="[&_*]:!text-white">
          <Wordmark />
        </span>
        <nav className="flex items-center gap-3 text-sm">
          {session ? (
            <Link href="/dashboard" className="btn-gold">Tableau de bord</Link>
          ) : (
            <>
              <Link href="/login" className="text-navy-100 hover:text-white">Connexion</Link>
              <Link href="/register" className="btn-gold">Créer un compte</Link>
            </>
          )}
        </nav>
      </header>

      <section className="mx-auto max-w-6xl px-6 py-16">
        <div className="max-w-3xl">
          <p className="mb-3 inline-flex items-center gap-2 rounded-full bg-white/10 px-3 py-1 text-xs font-medium text-gold-200">
            Énergie renouvelable C&I · Afrique centrale
          </p>
          <h1 className="text-4xl font-bold leading-tight text-white sm:text-5xl">
            Originer et mettre en relation les projets solaire + stockage, sur deux objectifs mesurés.
          </h1>
          <p className="mt-5 text-lg text-navy-100">
            ATEN relie entreprises consommatrices et développeurs. Chaque opportunité est chiffrée
            sur la <span className="font-semibold text-vert-300">décarbonisation</span> (tCO₂ évitées)
            et la <span className="font-semibold text-gold-200">sécurité d'approvisionnement</span>
            {" "}(taux de couverture, déficit résiduel, coût de la fiabilité).
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link href={session ? "/dashboard" : "/register"} className="btn-gold text-base">
              Commencer
            </Link>
            <Link href="/login" className="btn border border-white/30 text-white hover:bg-white/10">
              J'ai déjà un compte
            </Link>
          </div>
          <p className="mt-4 text-sm text-navy-200">
            Démo : <code className="text-gold-200">offtaker@aten.demo</code> ·{" "}
            <code className="text-gold-200">developer@aten.demo</code> ·{" "}
            <code className="text-gold-200">admin@aten.demo</code> — mot de passe <code>demo1234</code>
          </p>
        </div>
      </section>

      <section className="bg-navy-50 py-16 text-navy-800">
        <div className="mx-auto max-w-6xl px-6">
          <h2 className="text-2xl font-semibold">Neuf modules, une chaîne d'origination</h2>
          <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {modules.map((m) => (
              <div key={m.t} className="card">
                <h3 className="font-semibold text-navy-800">{m.t}</h3>
                <p className="mt-1 text-sm text-navy-500">{m.d}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <footer className="bg-navy-800 py-8 text-center text-sm text-navy-300">
        ATEN — Le disque solaire · Décarbonisation & sécurité d'approvisionnement
      </footer>
    </div>
  );
}
