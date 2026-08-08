import { notFound, redirect } from "next/navigation";
import { getCurrentProfile } from "@/services/profiles";
import { getConversationWithMessages } from "@/services/ai/tutor";
import { TutorChat } from "./tutor-chat";

export default async function TutorPage({
  params,
}: {
  params: Promise<{ conversationId: string }>;
}) {
  const profile = await getCurrentProfile();
  if (!profile) {
    redirect("/login");
  }

  const { conversationId } = await params;
  const { conversation, messages } = await getConversationWithMessages(conversationId);

  // RLS already scopes this to the caller's own conversations — a null
  // result here means "not found", never "someone else's".
  if (!conversation) {
    notFound();
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-2xl flex-col gap-4 px-6 py-12">
      <h1 className="text-2xl font-semibold text-black dark:text-zinc-50">Tuteur IA</h1>

      {!process.env.ANTHROPIC_API_KEY ? (
        <p className="rounded border border-amber-300 bg-amber-50 p-3 text-sm text-amber-800 dark:border-amber-800 dark:bg-amber-950 dark:text-amber-200">
          Le tuteur IA n&apos;est pas encore configuré sur cet environnement
          (ANTHROPIC_API_KEY manquant).
        </p>
      ) : null}

      <TutorChat conversationId={conversationId} initialMessages={messages} />
    </main>
  );
}
