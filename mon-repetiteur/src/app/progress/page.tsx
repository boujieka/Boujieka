import { redirect } from "next/navigation";
import { getCurrentProfile } from "@/services/profiles";
import { getStudentProgress } from "@/services/progress";

export default async function ProgressPage() {
  const profile = await getCurrentProfile();
  if (!profile) {
    redirect("/login");
  }

  const progress = await getStudentProgress();

  return (
    <main className="mx-auto flex min-h-screen max-w-2xl flex-col gap-6 px-6 py-12">
      <h1 className="text-2xl font-semibold text-black dark:text-zinc-50">
        Ma progression
      </h1>

      {progress.length === 0 ? (
        <p className="text-zinc-500">
          Aucune progression pour le moment — commencez par un exercice.
        </p>
      ) : (
        <ul className="flex flex-col gap-2">
          {progress.map((entry) => (
            <li
              key={entry.skillId}
              className="rounded border border-zinc-200 p-3 dark:border-zinc-800"
            >
              <div className="flex items-center justify-between gap-2">
                <div>
                  <p className="text-xs text-zinc-500">{entry.topicTitle}</p>
                  <p className="text-sm font-medium text-black dark:text-zinc-50">
                    {entry.skillTitle}
                  </p>
                </div>
                <p className="text-sm tabular-nums text-zinc-700 dark:text-zinc-300">
                  {Math.round(entry.masteryScore * 100)}%
                </p>
              </div>
              <div className="mt-2 h-1.5 w-full overflow-hidden rounded-full bg-zinc-100 dark:bg-zinc-800">
                <div
                  className="h-full rounded-full bg-black dark:bg-white"
                  style={{ width: `${Math.round(entry.masteryScore * 100)}%` }}
                />
              </div>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
