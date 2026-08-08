import Link from "next/link";
import { buttonVariants } from "@/components/ui/button";
import { BookIcon, ChartIcon, ChatIcon, CheckIcon } from "@/components/ui/icons";

const FEATURES = [
  {
    icon: BookIcon,
    title: "Cours et exercices",
    description: "Un programme structuré, avec des exercices corrigés automatiquement.",
  },
  {
    icon: ChatIcon,
    title: "Tuteur IA",
    description: "Un indice, une méthode, une solution guidée — jamais juste la réponse.",
  },
  {
    icon: ChartIcon,
    title: "Suivi de progression",
    description: "Voyez vos points forts et vos points faibles, matière par matière.",
  },
  {
    icon: CheckIcon,
    title: "Examens blancs",
    description: "Entraînez-vous en conditions réelles avant le jour J.",
  },
];

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col bg-zinc-50 dark:bg-zinc-950">
      <main className="mx-auto flex w-full max-w-2xl flex-1 flex-col gap-12 px-6 py-16 sm:py-24">
        <div className="flex flex-col items-center gap-5 text-center">
          <span className="inline-flex items-center rounded-full bg-indigo-100 px-3 py-1 text-xs font-medium text-indigo-800 dark:bg-indigo-950 dark:text-indigo-300">
            Terminale C · GCE A-Level
          </span>
          <h1 className="text-4xl font-semibold tracking-tight text-zinc-950 sm:text-5xl dark:text-zinc-50">
            Mon Répétiteur
          </h1>
          <p className="max-w-md text-lg leading-8 text-zinc-600 dark:text-zinc-400">
            La préparation aux examens, du cours jusqu&apos;à l&apos;examen blanc — avec un
            tuteur IA qui vous aide à progresser, pas seulement à trouver la réponse.
          </p>
          <div className="flex flex-col gap-3 sm:flex-row">
            <Link href="/signup" className={buttonVariants({ size: "md" })}>
              Créer un compte
            </Link>
            <Link href="/login" className={buttonVariants({ variant: "secondary", size: "md" })}>
              Se connecter
            </Link>
          </div>
        </div>

        <dl className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          {FEATURES.map(({ icon: Icon, title, description }) => (
            <div
              key={title}
              className="flex flex-col gap-2 rounded-xl border border-zinc-200 bg-white p-4 dark:border-zinc-800 dark:bg-zinc-900"
            >
              <Icon className="h-6 w-6 text-indigo-600 dark:text-indigo-400" />
              <dt className="font-medium text-zinc-950 dark:text-zinc-50">{title}</dt>
              <dd className="text-sm text-zinc-600 dark:text-zinc-400">{description}</dd>
            </div>
          ))}
        </dl>
      </main>
    </div>
  );
}
