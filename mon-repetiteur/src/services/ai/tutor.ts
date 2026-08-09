import "server-only";
import { createClient } from "@/lib/supabase/server";
import { AnthropicProvider } from "./anthropic-provider";
import type { AIProvider } from "./provider";
import { buildSystemPrompt } from "./prompt";
import { resolveTutorContext } from "./context";
import { isExamModeActive } from "./exam-mode";
import { generateStudyPlan } from "@/services/study-plan";
import type { AiConversation, AiMessage, TutorContext } from "@/types/ai";
import type { Json } from "@/lib/supabase/database.types";

function getProvider(): AIProvider | null {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) return null;
  return new AnthropicProvider(apiKey);
}

export interface StartConversationResult {
  error: string | null;
  conversation: AiConversation | null;
}

export async function startTutorConversation(
  context: TutorContext,
): Promise<StartConversationResult> {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) {
    return { error: "Vous devez être connecté.", conversation: null };
  }

  const { data, error } = await supabase
    .from("ai_conversations")
    .insert({ profile_id: user.id, context: context as Json })
    .select()
    .single();

  if (error) {
    return { error: error.message, conversation: null };
  }
  return { error: null, conversation: data };
}

export async function getConversationWithMessages(conversationId: string): Promise<{
  conversation: AiConversation | null;
  messages: AiMessage[];
}> {
  const supabase = await createClient();

  const { data: conversation } = await supabase
    .from("ai_conversations")
    .select("*")
    .eq("id", conversationId)
    .maybeSingle();

  if (!conversation) {
    return { conversation: null, messages: [] };
  }

  const { data: messages } = await supabase
    .from("ai_messages")
    .select("*")
    .eq("conversation_id", conversationId)
    .order("created_at");

  return { conversation, messages: messages ?? [] };
}

export interface SendTutorMessageResult {
  error: string | null;
  userMessage: AiMessage | null;
  assistantMessage: AiMessage | null;
}

/**
 * Core primitive every AIService method funnels through: persists the
 * user's turn, enforces exam mode server-side (CLAUDE.md §22), calls the
 * provider with the pedagogical system prompt + resolved context, then
 * persists and returns the reply.
 */
async function sendTutorMessage(input: {
  conversationId: string;
  content: string;
}): Promise<SendTutorMessageResult> {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) {
    return { error: "Vous devez être connecté.", userMessage: null, assistantMessage: null };
  }

  if (await isExamModeActive(user.id)) {
    return {
      error: "Le tuteur IA est désactivé pendant un examen.",
      userMessage: null,
      assistantMessage: null,
    };
  }

  const { data: conversation, error: convError } = await supabase
    .from("ai_conversations")
    .select("*")
    .eq("id", input.conversationId)
    .maybeSingle();
  if (convError || !conversation) {
    return { error: "Conversation introuvable.", userMessage: null, assistantMessage: null };
  }

  const { data: userMessage, error: userMsgError } = await supabase
    .from("ai_messages")
    .insert({ conversation_id: input.conversationId, role: "user", content: input.content })
    .select()
    .single();
  if (userMsgError || !userMessage) {
    return {
      error: userMsgError?.message ?? "Échec de l'enregistrement du message.",
      userMessage: null,
      assistantMessage: null,
    };
  }

  const provider = getProvider();
  if (!provider) {
    return {
      error: "Le tuteur IA n'est pas encore configuré (ANTHROPIC_API_KEY manquant).",
      userMessage,
      assistantMessage: null,
    };
  }

  const { data: history } = await supabase
    .from("ai_messages")
    .select("*")
    .eq("conversation_id", input.conversationId)
    .order("created_at");

  const resolvedContext = await resolveTutorContext(
    (conversation.context ?? {}) as TutorContext,
  );
  const system = buildSystemPrompt(resolvedContext);

  let assistantText: string;
  try {
    assistantText = await provider.complete({
      system,
      messages: (history ?? [])
        .filter((m) => m.role === "user" || m.role === "assistant")
        .map((m) => ({ role: m.role as "user" | "assistant", content: m.content })),
    });
  } catch (err) {
    console.error("AI provider error:", err);
    return {
      error: "Le tuteur IA est temporairement indisponible.",
      userMessage,
      assistantMessage: null,
    };
  }

  const { data: assistantMessage, error: assistantError } = await supabase
    .from("ai_messages")
    .insert({ conversation_id: input.conversationId, role: "assistant", content: assistantText })
    .select()
    .single();

  if (assistantError) {
    return { error: assistantError.message, userMessage, assistantMessage: null };
  }

  return { error: null, userMessage, assistantMessage };
}

/**
 * AIService (CLAUDE.md §7). chat() is the shared primitive; explain/
 * generateHint/guidedSolution are pedagogical modes of the same
 * conversation, not separate LLM-calling code paths (CLAUDE.md §6: avoid
 * duplicated logic). generateSimilarExercise/diagnoseStudent/
 * generateStudyPlan belong to later phases (Exercises variety, richer
 * Progress diagnostics, Study Plans) — stubbed with an honest "not yet"
 * error, not a faked response.
 */
export const AIService = {
  chat: (conversationId: string, content: string) =>
    sendTutorMessage({ conversationId, content }),

  explain: (conversationId: string, topic: string) =>
    sendTutorMessage({ conversationId, content: `Explique-moi ce concept : ${topic}` }),

  generateHint: (conversationId: string, question: string) =>
    sendTutorMessage({
      conversationId,
      content: `Donne-moi seulement un indice (pas la solution) pour : ${question}`,
    }),

  guidedSolution: (conversationId: string, question: string) =>
    sendTutorMessage({
      conversationId,
      content: `Guide-moi étape par étape pour résoudre : ${question}`,
    }),

  generateSimilarExercise: async (): Promise<{ error: string }> => ({
    error: "Pas encore implémenté — prévu avec l'enrichissement de la banque d'exercices.",
  }),

  diagnoseStudent: async (): Promise<{ error: string }> => ({
    error: "Pas encore implémenté — prévu avec l'enrichissement du suivi de progression.",
  }),

  generateStudyPlan: () => generateStudyPlan(),
};
