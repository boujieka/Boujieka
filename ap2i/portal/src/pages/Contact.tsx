import { useId, useMemo, useRef, useState, type FormEvent } from "react";
import { useI18n } from "../lib/i18n";
import { ct } from "../lib/i18n-commercial";
import { contactFormOpen, SITE } from "../lib/site";
import type { Route } from "../lib/router";
import { Card, PageHead } from "../components/ui";
import { planName } from "./Plans";

const SEGMENTS = ["government", "donor", "consultancy", "media", "other"] as const;
type Segment = (typeof SEGMENTS)[number];
const MAX_MESSAGE = 1000;
// Pragmatic check; the browser's type=email validation is not relied on (noValidate) so messages stay localised.
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

interface Values { name: string; organisation: string; email: string; segment: Segment | ""; message: string; consent: boolean; botField: string }
type FieldKey = "name" | "organisation" | "email" | "segment" | "message" | "consent";
type Errors = Partial<Record<FieldKey, string>>;

const EMPTY: Values = { name: "", organisation: "", email: "", segment: "", message: "", consent: false, botField: "" };

function validate(v: Values): Errors {
  const e: Errors = {};
  if (!v.name.trim()) e.name = "com.err.name";
  if (!v.organisation.trim()) e.organisation = "com.err.org";
  if (!EMAIL_RE.test(v.email.trim())) e.email = "com.err.email";
  if (!v.segment) e.segment = "com.err.segment";
  if (v.message.length > MAX_MESSAGE) e.message = "com.err.message";
  if (!v.consent) e.consent = "com.err.consent";
  return e;
}

export function Contact({ route }: { route: Route }) {
  const { locale } = useI18n();
  const c = (k: string, vars?: Record<string, string | number>) => ct(locale, k, vars);
  const open = contactFormOpen();
  const planCode = route.qs.get("plan") ?? "";
  const plan = useMemo(() => (planCode ? planName(planCode, locale) : null), [planCode, locale]);

  const [v, setV] = useState<Values>(EMPTY);
  const [errors, setErrors] = useState<Errors>({});
  const [touched, setTouched] = useState(false);
  const [state, setState] = useState<"idle" | "sending" | "ok" | "fail">("idle");
  const summaryRef = useRef<HTMLDivElement>(null);
  const uid = useId();
  const id = (k: string) => `${uid}-${k}`;

  const set = <K extends keyof Values>(k: K, val: Values[K]) => {
    const next = { ...v, [k]: val };
    setV(next);
    if (touched) setErrors(validate(next));
  };

  async function submit(ev: FormEvent<HTMLFormElement>) {
    ev.preventDefault();
    if (!open || state === "sending") return;
    const e = validate(v);
    setErrors(e);
    setTouched(true);
    if (Object.keys(e).length) {
      requestAnimationFrame(() => summaryRef.current?.focus());
      return;
    }
    setState("sending");
    const body = new URLSearchParams({
      "form-name": "contact",
      "bot-field": v.botField,
      name: v.name.trim(),
      organisation: v.organisation.trim(),
      email: v.email.trim(),
      segment: v.segment,
      message: v.message.trim(),
      consent: "yes",
      plan: plan ? planCode : "",
    });
    try {
      const res = await fetch("/", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: body.toString() });
      if (!res.ok) throw new Error(String(res.status));
      setState("ok");
      setV(EMPTY);
      setTouched(false);
    } catch {
      setState("fail");
    }
  }

  const errCount = Object.keys(errors).length;
  const fieldProps = (k: FieldKey) => ({
    id: id(k),
    "aria-invalid": errors[k] ? (true as const) : undefined,
    "aria-describedby": errors[k] ? id(`${k}-err`) : undefined,
  });
  const Err = ({ k }: { k: FieldKey }) => (errors[k] ? <span id={id(`${k}-err`)} className="field-err" style={{ color: "var(--red)", fontSize: ".8rem" }}>{c(errors[k] as string)}</span> : null);
  const Req = () => <span className="muted small"> ({c("com.f.required")})</span>;
  const labelStyle = { display: "flex", flexDirection: "column" as const, gap: 4, fontSize: ".88rem" };
  const inputStyle = { width: "100%" };
  const publisherText = SITE.publisher ? SITE.publisher.name : c("com.publisher.todo");

  return (
    <div>
      <PageHead title={c("com.contact.title")} subtitle={c("com.contact.subtitle")} />
      {plan && <p><span className="badge b-gold">{c("com.contact.plan", { plan })}</span></p>}

      {!open && (
        <div className="state empty" role="note" data-testid="contact-closed" style={{ flexDirection: "column", alignItems: "flex-start", marginBottom: 12 }}>
          <b>{c("com.contact.closed.title")}</b>
          <span>{c("com.contact.closed.body")}</span>
          {!SITE.publisher && <span className="small">{c("com.publisher.todo")}</span>}
        </div>
      )}

      <div className="grid-2-1">
        <Card title={c("com.contact.formTitle")}>
          {state === "ok" ? (
            <div className="state form-ok" role="status" data-testid="contact-ok" style={{ flexDirection: "column", alignItems: "flex-start" }}>
              <b>{c("com.ok.title")}</b>
              <span>{c("com.ok.body")}</span>
              <button type="button" className="btn sm ghost" onClick={() => setState("idle")}>{c("com.ok.again")}</button>
            </div>
          ) : (
            <form name="contact" method="POST" data-netlify="true" netlify-honeypot="bot-field" noValidate onSubmit={submit}
              aria-disabled={!open || undefined} data-testid="contact-form" className="contact-form">
              <input type="hidden" name="form-name" value="contact" />
              <fieldset disabled={!open || state === "sending"} style={{ border: 0, padding: 0, margin: 0, minWidth: 0, display: "grid", gap: 12 }}>
                {errCount > 0 && (
                  <div ref={summaryRef} tabIndex={-1} role="alert" className="state err" style={{ padding: "8px 0" }}>
                    {c("com.err.summary", { n: errCount })}
                  </div>
                )}
                {/* Honeypot: hidden from people and assistive technologies; bots fill it and Netlify discards the entry. */}
                <p hidden aria-hidden="true">
                  <label>{c("com.f.honeypot")} <input name="bot-field" tabIndex={-1} autoComplete="off" value={v.botField} onChange={(e) => set("botField", e.target.value)} /></label>
                </p>

                <label htmlFor={id("name")} style={labelStyle}>
                  <span>{c("com.f.name")}<Req /></span>
                  <input {...fieldProps("name")} name="name" type="text" autoComplete="name" required maxLength={200} style={inputStyle}
                    value={v.name} onChange={(e) => set("name", e.target.value)} />
                  <Err k="name" />
                </label>

                <label htmlFor={id("organisation")} style={labelStyle}>
                  <span>{c("com.f.org")}<Req /></span>
                  <input {...fieldProps("organisation")} name="organisation" type="text" autoComplete="organization" required maxLength={200} style={inputStyle}
                    value={v.organisation} onChange={(e) => set("organisation", e.target.value)} />
                  <Err k="organisation" />
                </label>

                <label htmlFor={id("email")} style={labelStyle}>
                  <span>{c("com.f.email")}<Req /></span>
                  <input {...fieldProps("email")} name="email" type="email" autoComplete="email" inputMode="email" required maxLength={254} style={inputStyle}
                    value={v.email} onChange={(e) => set("email", e.target.value)} />
                  <Err k="email" />
                </label>

                <label htmlFor={id("segment")} style={labelStyle}>
                  <span>{c("com.f.segment")}<Req /></span>
                  <select {...fieldProps("segment")} name="segment" required style={inputStyle}
                    value={v.segment} onChange={(e) => set("segment", e.target.value as Segment | "")}>
                    <option value="">{c("com.f.segment.choose")}</option>
                    {SEGMENTS.map((sg) => <option key={sg} value={sg}>{c(`com.seg.${sg}`)}</option>)}
                  </select>
                  <Err k="segment" />
                </label>

                <label htmlFor={id("message")} style={labelStyle}>
                  <span>{c("com.f.message")} <span className="muted small">({c("com.f.optional")})</span></span>
                  <textarea {...fieldProps("message")} name="message" rows={5} maxLength={MAX_MESSAGE} style={{ ...inputStyle, resize: "vertical" }}
                    aria-describedby={[id("message-count"), errors.message ? id("message-err") : ""].filter(Boolean).join(" ")}
                    value={v.message} onChange={(e) => set("message", e.target.value)} />
                  <span id={id("message-count")} className="small muted">{c("com.f.messageHint", { n: v.message.length })}</span>
                  <Err k="message" />
                </label>

                <div>
                  <label htmlFor={id("consent")} className="inline" style={{ alignItems: "flex-start", fontSize: ".88rem", color: "inherit" }}>
                    <input {...fieldProps("consent")} name="consent" type="checkbox" value="yes" required style={{ marginTop: 3 }}
                      checked={v.consent} onChange={(e) => set("consent", e.target.checked)} />
                    <span>{c("com.f.consent")} <a href="#/legal/privacy">{c("com.f.consentLink")}</a>.<Req /></span>
                  </label>
                  <Err k="consent" />
                </div>

                <input type="hidden" name="plan" value={plan ? planCode : ""} />

                {state === "fail" && <div className="state err" role="alert" style={{ padding: "4px 0" }} data-testid="contact-fail">{c("com.fail")}</div>}

                <div>
                  <button type="submit" className="btn gold" data-testid="contact-submit">
                    {state === "sending" ? c("com.f.sending") : c("com.f.submit")}
                  </button>
                </div>
              </fieldset>
            </form>
          )}
        </Card>

        <Card title={c("com.data.title")}>
          <dl className="dl">
            <div><dt>{c("com.data.who")}</dt><dd>{publisherText}</dd></div>
            <div><dt>{c("com.data.processor")}</dt><dd>{c("com.data.processor.value")}</dd></div>
            <div><dt>{c("com.data.purpose")}</dt><dd>{c("com.data.purpose.value")}</dd></div>
            <div><dt>{c("com.data.marketing")}</dt><dd>{c("com.data.marketing.value")}</dd></div>
            <div><dt>{c("com.data.retention")}</dt><dd>{c("com.data.retention.value")}</dd></div>
          </dl>
          <p className="small"><a href="#/legal/privacy">{c("com.data.more")}</a></p>
        </Card>
      </div>
    </div>
  );
}
