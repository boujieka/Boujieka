import { redirect } from "next/navigation";
import { getCurrentProfile } from "@/services/profiles";
import { getExercises } from "@/services/exercises";
import { ExerciseCard } from "./exercise-card";
import { AppShell } from "@/components/app-shell";
import { PageHeader } from "@/components/ui/page-header";
import { EmptyState } from "@/components/ui/empty-state";

export default async function PracticePage({
  params,
}: {
  params: Promise<{ skillId: string }>;
}) {
  const profile = await getCurrentProfile();
  if (!profile) {
    redirect("/login");
  }

  const { skillId } = await params;
  const exercises = await getExercises(skillId);

  return (
    <AppShell>
      <main className="mx-auto flex max-w-2xl flex-col gap-6 px-6 py-8 sm:py-12">
        <PageHeader title="S'entraîner" />
        {exercises.length === 0 ? (
          <EmptyState message="Aucun exercice disponible pour le moment." />
        ) : (
          <ul className="flex flex-col gap-4">
            {exercises.map((exercise) => (
              <li key={exercise.id}>
                <ExerciseCard exercise={exercise} />
              </li>
            ))}
          </ul>
        )}
      </main>
    </AppShell>
  );
}
