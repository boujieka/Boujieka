import { useMemo, useState, type ReactNode } from "react";
import { useI18n } from "../lib/i18n";
import { downloadCSV, downloadXLSX, type Cell } from "../lib/exporters";

export interface Column<T> {
  key: string;
  label: string;
  value: (row: T) => Cell; // raw value (sorting, exports)
  render?: (row: T) => ReactNode;
  align?: "right";
  width?: string;
  minWidth?: string; // e.g. "26ch" for titles: avoids letter-by-letter wrapping
  exportValue?: (row: T) => Cell; // human-readable value in CSV/Excel (default: value)
  exportable?: boolean; // false for UI-only columns (checkboxes)
}

/** Sortable, paginated table with CSV / Excel export of ALL rows of the current selection. */
export function DataTable<T>({ rows, columns, pageSize = 25, exportName, provenance, rowKey, initialSort, caption, testId }: {
  rows: T[]; columns: Column<T>[]; pageSize?: number; exportName?: string; provenance?: string[]; rowKey: (r: T) => string | number;
  initialSort?: { key: string; dir: 1 | -1 }; caption?: string; testId?: string;
}) {
  const { t } = useI18n();
  const [sort, setSort] = useState(initialSort);
  const [page, setPage] = useState(0);
  const sorted = useMemo(() => {
    if (!sort) return rows;
    const col = columns.find((c) => c.key === sort.key);
    if (!col) return rows;
    return [...rows].sort((a, b) => {
      const va = col.value(a), vb = col.value(b);
      if (va === null || va === undefined || va === "") return 1; // missing values always last
      if (vb === null || vb === undefined || vb === "") return -1;
      return (typeof va === "number" && typeof vb === "number" ? va - vb : String(va).localeCompare(String(vb))) * sort.dir;
    });
  }, [rows, sort, columns]);
  const pages = Math.max(1, Math.ceil(sorted.length / pageSize));
  const p = Math.min(page, pages - 1);
  const visible = sorted.slice(p * pageSize, (p + 1) * pageSize);
  const exp = (kind: "csv" | "xlsx") => {
    const cols = columns.filter((c) => c.exportable !== false);
    const header = cols.map((c) => c.label);
    const data = sorted.map((r) => cols.map((c) => (c.exportValue ?? c.value)(r)));
    if (kind === "csv") downloadCSV(exportName ?? "ap2i", header, data, provenance ?? []);
    else void downloadXLSX(exportName ?? "ap2i", header, data, provenance ?? []);
  };
  return (
    <div className="dt" data-testid={testId}>
      {exportName && (
        <div className="dt-tools">
          <span className="muted small">{sorted.length} {caption ?? ""}</span>
          <button className="btn xs ghost" onClick={() => exp("csv")} data-testid={testId ? `${testId}-csv` : undefined}>{t("common.exportCsv")}</button>
          <button className="btn xs ghost" onClick={() => exp("xlsx")}>{t("common.exportXlsx")}</button>
        </div>
      )}
      <div className="table-wrap">
        <table className="dt-table">
          <thead>
            <tr>
              {columns.map((c) => (
                <th key={c.key} scope="col" style={{ width: c.width, minWidth: c.minWidth }} className={c.align === "right" ? "r" : undefined}
                  aria-sort={sort?.key === c.key ? (sort.dir === 1 ? "ascending" : "descending") : "none"}>
                  <button className="th-btn" onClick={() => { setSort({ key: c.key, dir: sort?.key === c.key ? (-sort.dir as 1 | -1) : 1 }); setPage(0); }}>
                    {c.label}{sort?.key === c.key ? (sort.dir === 1 ? " ▲" : " ▼") : ""}
                  </button>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {visible.map((r) => (
              <tr key={rowKey(r)}>
                {columns.map((c) => {
                  const v = c.render ? c.render(r) : c.value(r);
                  return <td key={c.key} data-label={c.label} style={{ minWidth: c.minWidth }} className={c.align === "right" ? "r" : undefined}>{v === null || v === undefined || v === "" ? <span className="na">—</span> : v}</td>;
                })}
              </tr>
            ))}
            {!visible.length && <tr><td colSpan={columns.length} className="muted">{t("common.none")}</td></tr>}
          </tbody>
        </table>
      </div>
      {pages > 1 && (
        <div className="pager">
          <button className="btn xs ghost" disabled={p === 0} onClick={() => setPage(p - 1)}>{t("common.prev")}</button>
          <span className="small">{t("common.page")} {p + 1} {t("common.of")} {pages}</span>
          <button className="btn xs ghost" disabled={p >= pages - 1} onClick={() => setPage(p + 1)}>{t("common.next")}</button>
        </div>
      )}
    </div>
  );
}
