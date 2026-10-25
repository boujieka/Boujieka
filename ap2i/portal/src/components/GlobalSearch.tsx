import { useMemo, useRef, useState } from "react";
import { useI18n } from "../lib/i18n";
import { useNames, useSnap } from "../lib/context";
import { maxLevel } from "../lib/agg";
import { go } from "../lib/router";
import { LevelBadge } from "./ui";

const norm = (s: string) => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();

/** Search-as-you-type over project titles, identifiers (AP²I and donor) and executing agencies. */
export function GlobalSearch({ variant = "bar" }: { variant?: "bar" | "hero" }) {
  const { t, locale } = useI18n();
  const s = useSnap();
  const names = useNames(locale);
  const [q, setQ] = useState("");
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState(0);
  const box = useRef<HTMLDivElement>(null);
  const id = variant === "hero" ? "hsearch" : "gsearch";
  const index = useMemo(() => {
    const ids = new Map<number, string[]>();
    for (const a of s.agreements) ids.set(a.project, [...(ids.get(a.project) ?? []), a.source_identifier]);
    return s.projects.map((p) => ({ p, text: norm([p.title, p.ref, p.agency ?? "", ...p.partners.map((c) => `${c} ${names.partner(c)}`), ...(ids.get(p.id) ?? [])].join(" ")) }));
  }, [s, names]);
  const results = useMemo(() => {
    const words = norm(q).split(/\s+/).filter((w) => w.length >= 2);
    if (!words.length) return [];
    return index.filter((x) => words.every((w) => x.text.includes(w))).slice(0, 8).map((x) => x.p);
  }, [q, index]);
  const pick = (ref: string) => {
    setQ("");
    setOpen(false);
    go(`/project/${ref}`, {});
  };
  return (
    <div className={`gsearch${variant === "hero" ? " gsearch-hero" : ""}`} ref={box} onBlur={(e) => { if (!box.current?.contains(e.relatedTarget as Node)) setOpen(false); }}>
      <input type="search" value={q} placeholder={variant === "hero" ? t("search.heroPlaceholder") : t("search.placeholder")} aria-label={t("search.placeholder")} role="combobox"
        aria-expanded={open && results.length > 0} aria-controls={`${id}-list`} aria-autocomplete="list" data-testid={variant === "hero" ? "hero-search" : "global-search"}
        aria-activedescendant={open && results[active] ? `${id}-${results[active].id}` : undefined}
        onChange={(e) => { setQ(e.target.value); setOpen(true); setActive(0); }} onFocus={() => setOpen(true)}
        onKeyDown={(e) => {
          if (e.key === "ArrowDown") { e.preventDefault(); setActive((a) => Math.min(a + 1, results.length - 1)); }
          else if (e.key === "ArrowUp") { e.preventDefault(); setActive((a) => Math.max(a - 1, 0)); }
          else if (e.key === "Enter" && results[active]) { e.preventDefault(); pick(results[active].ref); }
          else if (e.key === "Escape") setOpen(false);
        }} />
      {open && q.trim().length >= 2 && (
        <ul id={`${id}-list`} role="listbox" className="gsearch-list">
          {results.length ? results.map((p, i) => {
            const l = maxLevel(p);
            return (
              <li key={p.id} id={`${id}-${p.id}`} role="option" aria-selected={i === active} className={i === active ? "on" : ""}
                onMouseDown={(e) => { e.preventDefault(); pick(p.ref); }} onMouseEnter={() => setActive(i)}>
                <b>{p.title}</b>
                <span className="small muted">{names.sector(p.sector)} · {t(`status.${p.status}`)} · {p.partners.map((c) => names.partner(c)).join(", ")}</span>
                {l && <LevelBadge level={l} />}
              </li>
            );
          }) : <li className="muted small">{t("common.none")}</li>}
        </ul>
      )}
    </div>
  );
}
