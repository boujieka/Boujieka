"use client";

import { useActionState, useEffect, useRef, useState } from "react";
import { sendMessageAction, type SendMessageState } from "./actions";
import type { AiMessage } from "@/types/ai";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/cn";

const initialState: SendMessageState = {
  error: null,
  userMessage: null,
  assistantMessage: null,
  sequence: 0,
};

/**
 * Owns the message list as client state, seeded from the server-rendered
 * history and appended to directly from the action's return value —
 * rather than depending on the parent Server Component re-fetching after
 * a mutation. Simpler and more standard for a chat UI, and sidesteps
 * needing every message-send to force a fresh server render just to see
 * its own result.
 */
export function TutorChat({
  conversationId,
  initialMessages,
}: {
  conversationId: string;
  initialMessages: AiMessage[];
}) {
  const [messages, setMessages] = useState(initialMessages);
  const [handledSequence, setHandledSequence] = useState(0);
  const boundAction = sendMessageAction.bind(null, conversationId);
  const [state, formAction, pending] = useActionState(boundAction, initialState);
  const formRef = useRef<HTMLFormElement>(null);

  // Adjusting state in response to a prop/value change during render
  // (not in an Effect) is the React-recommended pattern here — see
  // "You Might Not Need an Effect" / react-hooks/set-state-in-effect.
  if (state.sequence !== handledSequence) {
    setHandledSequence(state.sequence);
    if (state.userMessage || state.assistantMessage) {
      setMessages((prev) => [
        ...prev,
        ...(state.userMessage ? [state.userMessage] : []),
        ...(state.assistantMessage ? [state.assistantMessage] : []),
      ]);
    }
  }

  // Resetting the actual <form> DOM element is a real side effect, so it
  // does belong in an Effect (unlike the setMessages above).
  useEffect(() => {
    if (!state.error) {
      formRef.current?.reset();
    }
  }, [handledSequence, state.error]);

  return (
    <>
      <div className="flex flex-col gap-3">
        {messages.length === 0 ? (
          <p className="text-sm text-zinc-500 dark:text-zinc-400">
            Commence la conversation ci-dessous.
          </p>
        ) : (
          messages
            .filter((message) => message.role !== "system")
            .map((message) => (
              <div
                key={message.id}
                className={cn(
                  "max-w-[85%] whitespace-pre-wrap rounded-2xl px-4 py-2.5 text-sm leading-relaxed",
                  message.role === "user"
                    ? "self-end rounded-br-sm bg-indigo-600 text-white"
                    : "self-start rounded-bl-sm bg-zinc-100 text-zinc-950 dark:bg-zinc-800 dark:text-zinc-50",
                )}
              >
                {message.content}
              </div>
            ))
        )}
      </div>

      <form ref={formRef} action={formAction} className="flex flex-col gap-2">
        <textarea
          name="content"
          required
          rows={2}
          placeholder="Pose ta question…"
          className="rounded-lg border border-zinc-300 px-3 py-2.5 text-base focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:ring-offset-2 dark:border-zinc-700 dark:bg-zinc-900 dark:focus-visible:ring-offset-zinc-950"
        />
        {state.error ? (
          <p role="alert" className="text-sm text-rose-600 dark:text-rose-400">
            {state.error}
          </p>
        ) : null}
        <Button type="submit" disabled={pending} className="w-fit">
          {pending ? "Envoi…" : "Envoyer"}
        </Button>
      </form>
    </>
  );
}
