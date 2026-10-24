import { FormEvent, useState } from "react";
import { Api } from "../api";
import { Lang, t } from "../i18n";
import { Alert, errorText } from "../components/ui";

export function LoginPage({ lang, onToken }: { lang: Lang; onToken: (t: string) => void }) {
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  async function submit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const f = new FormData(e.currentTarget);
    setBusy(true);
    try {
      const r = await new Api(null).login(String(f.get("email")), String(f.get("password")));
      onToken(r.access_token);
    } catch (err) { setError(errorText(err)); } finally { setBusy(false); }
  }
  return (
    <form className="stack card" onSubmit={submit} aria-label={t("login", lang)}>
      <label className="field">{t("email", lang)}<input name="email" type="email" required autoComplete="username" /></label>
      <label className="field">{t("password", lang)}<input name="password" type="password" required minLength={12} autoComplete="current-password" /></label>
      {error && <Alert kind="critical">{error}</Alert>}
      <button className="primary" type="submit" disabled={busy}>{t("login", lang)}</button>
    </form>
  );
}

export function InvitePage({ token, lang, api, signedIn, onToken }: {
  token: string; lang: Lang; api: Api; signedIn: boolean; onToken: (t: string) => void;
}) {
  const [error, setError] = useState("");
  async function submit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const f = new FormData(e.currentTarget);
    try {
      const r = signedIn ? await api.acceptInvitation(token)
        : await api.acceptInvitation(token, String(f.get("name")), String(f.get("password")));
      onToken(r.access_token);
      window.location.hash = "#/projects";
      window.location.reload();
    } catch (err) { setError(errorText(err)); }
  }
  return (
    <section>
      <h2>{t("acceptInvitation", lang)}</h2>
      <form className="stack card" onSubmit={submit}>
        {!signedIn && <>
          <p className="small muted">{t("inviteNewAccount", lang)}</p>
          <label className="field">{t("name", lang)}<input name="name" required maxLength={200} autoComplete="name" /></label>
          <label className="field">{t("password", lang)}<input name="password" type="password" required minLength={12} autoComplete="new-password" /></label>
        </>}
        {error && <Alert kind="critical">{error}{error.startsWith("401") && <p>{t("inviteExisting", lang)}</p>}</Alert>}
        <button className="primary" type="submit">{t("acceptInvitation", lang)}</button>
      </form>
    </section>
  );
}
