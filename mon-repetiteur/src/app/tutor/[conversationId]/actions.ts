"use server";

import { revalidatePath } from "next/cache";
import { AIService } from "@/services/ai/tutor";
import type { AiMessage } from "@/types/ai";

export interface SendMessageState {
  error: string | null;
  userMessage: AiMessage | null;
  assistantMessage: AiMessage | null;
  /** Bumped on every action call so the client can tell two calls with the
   * same (e.g. both-null) shape apart and know a new response arrived. */
  sequence: number;
}

export async function sendMessageAction(
  conversationId: string,
  prevState: SendMessageState,
  formData: FormData,
): Promise<SendMessageState> {
  const sequence = prevState.sequence + 1;
  const content = String(formData.get("content") ?? "").trim();
  if (!content) {
    return { error: "Écrivez un message.", userMessage: null, assistantMessage: null, sequence };
  }

  const { error, userMessage, assistantMessage } = await AIService.chat(conversationId, content);

  // Best-effort: keeps the Data Cache fresh for the next full navigation
  // to this page. The client appends userMessage/assistantMessage itself
  // (below) rather than depending on this triggering an inline re-render.
  revalidatePath(`/tutor/${conversationId}`);

  return { error, userMessage, assistantMessage, sequence };
}
