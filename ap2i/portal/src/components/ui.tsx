import type { ReactNode } from "react";
import { useI18n } from "../lib/i18n";
import type { AlertLevel } from "../lib/types";

export function Card({ title, actions, children, note, id, className = "" }: {
  title?: ReactNode; actions?: ReactNode; children: ReactNode; note?: ReactNode; id?: string; className?: string;
}) {
  return (
    <section className={`card ${className}`} id={id} aria-label={typeof title === "string" ? title : undefined}>
      {(title || actions) && (
        <header className="card-h">
          {title && <h3>{title}</h3>}
          {actions && <div className="card-actions">{actions}</div>}
        </header>
      )}
      <div className="card-b">{children}</div>
      {note && <p className="note">{note}</p>}
    </section>
  );
}

export function Kpi({ label, value, sub, href }: { label: string; value: ReactNode; sub?: ReactNode; href?: string }) {
  const body = (
    <>
      <span className="kpi-l">{label}</span>
      <b className="kpi-v">{value}</b>
      {sub && <span className="kpi-s">{sub}</span>}
    </>
  );
  return href ? <a className="kpi" href={href}>{body}</a> : <div className="kpi">{body}</div>;
}

export function PageHead({ title, subtitle, children }: { title: string; subtitle?: ReactNode; children?: ReactNode }) {
  return (
    <div className="page-head">
      <div>
        <h1>{title}</h1>
        {subtitle && <p className="sub">{subtitle}</p>}
      </div>
      {children && <div className="page-head-r">{children}</div>}
    </div>
  );
}

const LEVEL_CLS: Record<AlertLevel, string> = { critical_attention: "lv-crit", high_attention: "lv-high", watch: "lv-watch", information: "lv-info" };

export function LevelBadge({ level }: { level: AlertLevel }) {
  const { t } = useI18n();
  return <span className={`badge ${LEVEL_CLS[level]}`}>{t(`level.${level}`)}</span>;
}

export function Badge({ children, tone = "navy" }: { children: ReactNode; tone?: "navy" | "green" | "gold" | "gray" }) {
  return <span className={`badge b-${tone}`}>{children}</span>;
}

export function Loading() {
  const { t } = useI18n();
  return <div className="state" role="status"><span className="spinner" aria-hidden /> {t("common.loading")}</div>;
}

export function ErrorState({ error, retry }: { error: string; retry?: () => void }) {
  const { t } = useI18n();
  return (
    <div className="state err" role="alert">
      <b>{t("common.error")}</b> <span className="muted">{error}</span>
      {retry && <button className="btn sm" onClick={retry}>{t("common.retry")}</button>}
    </div>
  );
}

export function Empty({ children }: { children?: ReactNode }) {
  const { t } = useI18n();
  return <div className="state empty">{children ?? t("common.none")}</div>;
}

export function NA() {
  const { t } = useI18n();
  return <span className="na">{t("common.na")}</span>;
}

export function Field({ label, children }: { label: string; children: ReactNode }) {
  return (
    <div className="field">
      <dt>{label}</dt>
      <dd>{children === null || children === undefined || children === "" ? <NA /> : children}</dd>
    </div>
  );
}

export function ExternalLink({ href, children }: { href: string | null | undefined; children: ReactNode }) {
  if (!href || !/^https?:\/\//.test(href)) return <>{children}</>;
  return <a href={href.replace(/^http:\/\//, "https://")} target="_blank" rel="noopener noreferrer">{children} ↗</a>;
}
