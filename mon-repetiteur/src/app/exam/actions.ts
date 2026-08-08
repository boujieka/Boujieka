"use server";

import { redirect } from "next/navigation";
import { createClient } from "@/lib/supabase/server";
import { createMockExam } from "@/services/mock-exam";

/**
 * Starts a mock exam for the first vertical (Terminale C -> Mathématiques
 * — PRD.md §5). Program/subject picking is later work, same scope call
 * as /learn and /tutor's entry points.
 */
export async function startMockExamAction() {
  const supabase = await createClient();

  const { data: program } = await supabase
    .from("programs")
    .select("id")
    .eq("code", "terminale_c")
    .single();
  const { data: subject } = await supabase
    .from("subjects")
    .select("id")
    .eq("program_id", program!.id)
    .eq("slug", "mathematiques")
    .single();
  const { data: cls } = await supabase
    .from("classes")
    .select("id")
    .eq("program_id", program!.id)
    .eq("code", "terminale")
    .single();

  const { error, mockExam } = await createMockExam(subject!.id, cls!.id);
  if (error || !mockExam) {
    redirect("/learn");
  }

  redirect(`/exam/${mockExam.id}`);
}
