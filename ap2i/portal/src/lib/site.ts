/**
 * Commercial / legal configuration of the public portal.
 *
 * OWNER ACTION REQUIRED — publisher identity.
 * `publisher` must be filled in by the owner of the portal (legal name of the publishing entity, country of
 * establishment and a contact e-mail address) BEFORE `contactFormEnabled` is switched to `true`. While
 * `publisher` is null:
 *   - the legal pages show a visible "identity to be completed" notice wherever the publisher is needed;
 *   - the contact form is rendered disabled and never submits anything (no personal data is collected
 *     without an identified data controller).
 * Never put a placeholder or invented entity here: leave it null until the real identity is known.
 */
export interface Publisher {
  /** Legal name of the publishing entity (as registered). */
  name: string;
  /** Country of establishment. */
  country: string;
  /** Address that receives contact requests and data-protection requests. */
  email?: string;
}

export const SITE = {
  publisher: null as null | Publisher,
  /** Switch to true only once `publisher` is filled in and the Netlify form "contact" is deployed. */
  contactFormEnabled: false,
  /** How the public snapshot is refreshed. "manual" = regenerated and redeployed by hand, no fixed schedule. */
  refreshCadence: "manual" as "manual" | "daily" | "weekly" | "monthly",
};

/** True when the contact form may actually POST data. */
export function contactFormOpen(): boolean {
  return SITE.contactFormEnabled && SITE.publisher !== null;
}
