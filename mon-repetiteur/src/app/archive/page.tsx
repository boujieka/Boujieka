import Link from "next/link";
import { redirect } from "next/navigation";
import { getCurrentProfile } from "@/services/profiles";
import { getPrograms, getSubjects } from "@/services/curriculum";
import { getExams } from "@/services/exam-archive";

const DEFAULT_PROGRAM_CODE = "terminale_c";

const RIGHTS_LABELS: Record<string, string> = {
  verified: "Vérifié",
  permission_required: "Permission requise",
  publicly_reusable: "Réutilisable publiquement",
  restricted: "Restreint",
  unknown: "Droits non résolus",
};

export default async function ArchivePage({
  searchParams,
}: {
  searchParams: Promise<{ program?: string }>;
}) {
  const profile = await getCurrentProfile();
  if (!profile) {
    redirect("/login");
  }

  const { program: requestedProgramCode } = await searchParams;

  const programs = await getPrograms();
  if (programs.length === 0) {
    return <Empty message="Aucun programme disponible pour le moment." />;
  }
  const program =
    programs.find((p) => p.code === (requestedProgramCode ?? DEFAULT_PROGRAM_CODE)) ??
    programs[0];

  const subjects = await getSubjects(program.id);
  const subject = subjects[0];
  if (!subject) {
    return <Empty message="Programme non encore configuré." />;
  }

  const exams = await getExams(subject.id);

  return (
    <main className="mx-auto flex min-h-screen max-w-2xl flex-col gap-6 px-6 py-12">
      <div className="flex flex-col gap-2">
        {programs.length > 1 ? (
          <nav className="flex gap-3 text-xs">
            {programs.map((p) => (
              <Link
                key={p.id}
                href={`/archive?program=${p.code}`}
                className={
                  p.id === program.id
                    ? "font-semibold underline"
                    : "text-zinc-500 underline dark:text-zinc-400"
                }
              >
                {p.name}
              </Link>
            ))}
          </nav>
        ) : null}
        <h1 className="text-2xl font-semibold text-black dark:text-zinc-50">
          Archive des épreuves — {subject.name}
        </h1>
      </div>

      {exams.length === 0 ? (
        <Empty message="Aucune épreuve archivée pour le moment." />
      ) : (
        <ul className="flex flex-col gap-2">
          {exams.map((exam) => (
            <li
              key={exam.id}
              className="flex items-center justify-between gap-3 rounded border border-zinc-200 p-3 text-sm dark:border-zinc-800"
            >
              <div>
                <p className="font-medium text-black dark:text-zinc-50">{exam.title}</p>
                <p className="text-xs text-zinc-500">
                  {exam.year}
                  {exam.session ? ` — ${exam.session}` : ""}
                </p>
              </div>
              {exam.accessUrl ? (
                <a
                  href={exam.accessUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="shrink-0 text-xs underline"
                >
                  Voir le sujet
                </a>
              ) : (
                <span className="shrink-0 rounded bg-zinc-100 px-2 py-1 text-xs text-zinc-600 dark:bg-zinc-800 dark:text-zinc-400">
                  {RIGHTS_LABELS[exam.rights_status] ?? exam.rights_status}
                </span>
              )}
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}

function Empty({ message }: { message: string }) {
  return (
    <main className="mx-auto flex min-h-screen max-w-2xl flex-col items-center justify-center px-6 text-center">
      <p className="text-zinc-500">{message}</p>
    </main>
  );
}
