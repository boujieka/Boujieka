import type { ReactNode } from "react";
import { label } from "../i18n";
import { natureLabel } from "../lib/format";

export function Field({ label: l, children, hint }: { label: string; children: ReactNode; hint?: string }) {
  return (
    <label className="field">
      <span className="field-label">{l}</span>
      {children}
      {hint && <span className="field-hint">{hint}</span>}
    </label>
  );
}

export function Select({ name, values, defaultValue, value, onChange, required }: {
  name?: string; values: readonly string[]; defaultValue?: string; value?: string;
  onChange?: (v: string) => void; required?: boolean;
}) {
  return (
    <select name={name} defaultValue={defaultValue} value={value} required={required}
      onChange={onChange ? (e) => onChange(e.target.value) : undefined}>
      {values.map((v) => <option key={v} value={v}>{label(v)}</option>)}
    </select>
  );
}

/** Étiquette de nature d'une valeur : renseigné / calculé / hypothétique / inconnu. */
export function NatureBadge({ nature }: { nature: string }) {
  return <span className={`badge nature-${nature}`}>{natureLabel(nature)}</span>;
}

export function FictionalBadge() {
  return <span className="badge fictional">FICTIF</span>;
}

export function ErrorBox({ error }: { error: unknown }) {
  if (!error) return null;
  const msg = error instanceof Error ? error.message : String(error);
  return <div className="error" role="alert">{msg}</div>;
}

export function Warnings({ items }: { items?: string[] }) {
  if (!items || items.length === 0) return null;
  return <ul className="warnings">{items.map((w, i) => <li key={i}>{w}</li>)}</ul>;
}
