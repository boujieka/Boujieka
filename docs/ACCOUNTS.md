# Free accounts (Supabase Auth)

Browsing the site stays open. A **free account is required to download**:

- report PDFs (`/rapports/**.pdf`);
- data CSVs (`/donnees/*.csv`);
- the CSV export of the market table.

Sign-in uses an e-mail link (magic link) and no password. Every registered user is recorded in Supabase Auth with:

- e-mail, sign-up date and last sign-in;
- the metadata entered on the form: `profil`, `organisation`, `pays`, `langue`, `consent_at`, `news`.

## How it works

1. **Sign-in form (`#compte`).** The form calls `POST {SUPABASE_URL}/auth/v1/otp` with `create_user: true` and the metadata. Supabase sends the link.
2. **Return from the link.** The link brings the user back to the site with `#access_token=…&refresh_token=…`. The page then:
   - stores the access token in the cookie `cartouche_at` (`Secure`, `SameSite=Lax`, lifetime of the token);
   - stores the refresh token in `localStorage`, which keeps the session alive across visits.
3. **Server-side check.** The Netlify Edge Function `site/edge/gate.js` runs on `/rapports/*.pdf` and `/donnees/*.csv`. It calls `GET {SUPABASE_URL}/auth/v1/user` with the cookie's token. If the token is accepted, the file is served. Otherwise, or if Supabase is unreachable, the visitor is redirected to `/?next=<file>#compte`.
4. **Limit of the CSV gate.** The market-table CSV is generated in the browser from data already embedded in the page. Its gate is therefore only a client-side prompt, not a protection.
5. **Account deletion.** The user requests it from the account panel, which uses the Netlify form `suppression-compte`. The owner then deletes the user in Supabase (Authentication → Users).

**Activation.** `site/build.py` enables all of this only when `SUPABASE_URL` and `SUPABASE_PUBLISHABLE_KEY` (or `SUPABASE_ANON_KEY`) are set in the build environment. Without them, nothing is gated and the account button is hidden.

## Setup (owner)

1. **Create the project.** On supabase.com, create a project. Choose a region close to your users and compatible with your data-protection obligations.
2. **Enable e-mail sign-in.** In Authentication → Sign In / Providers: Email enabled, new sign-ups allowed.
3. **Set the URLs.** In Authentication → URL Configuration:
   - Site URL: `https://cartouche-africa.netlify.app`;
   - Redirect URLs: `https://cartouche-africa.netlify.app/**`.
4. **Configure custom SMTP.** In Authentication → SMTP (or Emails), set up your own SMTP. Supabase's built-in e-mail service is rate-limited and meant for testing, so real sign-ups need your own provider.
5. **Set the environment variables.** In the **cloud environment settings** (never in chat or in the repository), set:
   - `SUPABASE_URL`: the Project URL, `https://<ref>.supabase.co`;
   - `SUPABASE_PUBLISHABLE_KEY`: the publishable key, `sb_publishable_…`, or the legacy `anon` key as `SUPABASE_ANON_KEY`. This key is public by design.
   - **Never use the `service_role` / `sb_secret_…` key.** The build refuses a `sb_secret_` key.
6. **Rebuild and deploy.** The daily job does this automatically.

## Listing registered users

- **Dashboard:** Supabase → Authentication → Users.
- **SQL editor:**

```sql
select email, created_at, last_sign_in_at, raw_user_meta_data
from auth.users order by created_at desc;
```

## Before Supabase is configured: free registration

The « Compte » tab (navigation and header button) is always visible. Until `SUPABASE_URL` and the public key are set, it shows a free registration form instead of the e-mail sign-in.

- **What the form records** (Netlify form `inscription-client`): name, e-mail, profile, organisation, country, consent, a news opt-in and an unsubscribe box.
- **What happens on submission:**
  - the browser remembers the registration and shows « Mon compte »;
  - nothing is gated, since there is no authentication service yet.
- **Owner access:** registrations are listed in Netlify → Forms → `inscription-client`, with CSV export.
- **When Supabase is configured:** the same tab switches to the e-mail-link account, and downloads and the investor journey require it.
