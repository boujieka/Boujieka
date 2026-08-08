"use server";

import { redirect } from "next/navigation";
import { startTutorConversation } from "@/services/ai/tutor";
import type { TutorContext } from "@/types/ai";

export async function startTutorConversationAction(formData: FormData) {
  const context: TutorContext = {
    skillId: formData.get("skillId")?.toString() || undefined,
    topicId: formData.get("topicId")?.toString() || undefined,
    subjectId: formData.get("subjectId")?.toString() || undefined,
  };

  const { error, conversation } = await startTutorConversation(context);
  if (error || !conversation) {
    redirect("/learn");
  }

  redirect(`/tutor/${conversation.id}`);
}
