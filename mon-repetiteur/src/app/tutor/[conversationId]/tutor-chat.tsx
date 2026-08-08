"use client";

import { useActionState, useEffect, useRef, useState } from "react";
import { sendMessageAction, type SendMessageState } from "./actions";
import type { AiMessage } from "@/types/ai";

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
          <p className="text-sm text-zinc-500">Commence la conversation ci-dessous.</p>
        ) : (
          messages
            .filter((message) => message.role !== "system")
            .map((message) => (
              <div
                key={message.id}
                className={`max-w-[85%] rounded p-3 text-sm ${
                  message.role === "user"
                    ? "self-end bg-black text-white dark:bg-white dark:text-black"
                    : "self-start bg-zinc-100 text-black dark:bg-zinc-800 dark:text-zinc-50"
                }`}
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
          className="rounded border border-zinc-300 px-3 py-2 text-sm dark:border-zinc-700 dark:bg-zinc-900"
        />
        {state.error ? (
          <p role="alert" className="text-sm text-red-600 dark:text-red-400">
            {state.error}
          </p>
        ) : null}
        <button
          type="submit"
          disabled={pending}
          className="w-fit rounded bg-black px-4 py-2 text-sm text-white disabled:opacity-50 dark:bg-white dark:text-black"
        >
          {pending ? "Envoi…" : "Envoyer"}
        </button>
      </form>
    </>
  );
}
