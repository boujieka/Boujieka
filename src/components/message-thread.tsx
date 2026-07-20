"use client";

import { ActionForm, SubmitButton } from "@/components/action-form";
import { sendMessageAction } from "@/lib/actions/interactions";

export interface ThreadMessage {
  id: string;
  body: string;
  senderName: string;
  fromMe: boolean;
  at: string;
}

/**
 * Fil de messagerie intermédié rattaché à une opportunité.
 * `recipientUserId` est calculé côté serveur (l'autre partie du fil).
 */
export function MessageThread({
  opportunityId,
  messages,
  recipientUserId,
}: {
  opportunityId: string;
  currentUserId: string;
  ownerUserId: string | null;
  messages: ThreadMessage[];
  canCompose: boolean;
  isOwner: boolean;
  recipientUserId?: string | null;
}) {
  return (
    <div className="card">
      <h2 className="mb-4 text-lg font-semibold">Messagerie</h2>
      {messages.length === 0 ? (
        <p className="text-sm text-navy-400">Aucun message pour l'instant.</p>
      ) : (
        <ul className="mb-4 space-y-2">
          {messages.map((m) => (
            <li key={m.id} className={`flex ${m.fromMe ? "justify-end" : "justify-start"}`}>
              <div
                className={`max-w-[75%] rounded-2xl px-4 py-2 text-sm ${
                  m.fromMe ? "bg-navy text-white" : "bg-navy-50 text-navy-800"
                }`}
              >
                <div className={`mb-0.5 text-xs ${m.fromMe ? "text-navy-200" : "text-navy-400"}`}>
                  {m.senderName} · {m.at}
                </div>
                {m.body}
              </div>
            </li>
          ))}
        </ul>
      )}

      {recipientUserId ? (
        <ActionForm action={sendMessageAction} className="flex gap-2">
          <input type="hidden" name="opportunityId" value={opportunityId} />
          <input type="hidden" name="recipientUserId" value={recipientUserId} />
          <input name="body" required className="input flex-1" placeholder="Votre message…" />
          <SubmitButton variant="primary">Envoyer</SubmitButton>
        </ActionForm>
      ) : (
        <p className="text-xs text-navy-400">
          La messagerie s'ouvre lorsqu'une des deux parties a initié le contact.
        </p>
      )}
    </div>
  );
}
