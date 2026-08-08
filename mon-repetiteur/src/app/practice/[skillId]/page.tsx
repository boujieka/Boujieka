import { redirect } from "next/navigation";
import { getCurrentProfile } from "@/services/profiles";
import { getExercises } from "@/services/exercises";
import { ExerciseCard } from "./exercise-card";

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
    <main className="mx-auto flex min-h-screen max-w-2xl flex-col gap-4 px-6 py-12">
      <h1 className="text-2xl font-semibold text-black dark:text-zinc-50">
        S&apos;entraîner
      </h1>
      {exercises.length === 0 ? (
        <p className="text-zinc-500">Aucun exercice disponible pour le moment.</p>
      ) : (
        exercises.map((exercise) => <ExerciseCard key={exercise.id} exercise={exercise} />)
      )}
    </main>
  );
}
