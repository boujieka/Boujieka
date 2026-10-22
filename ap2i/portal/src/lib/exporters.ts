// CSV / Excel exports of the rows behind a view. Every file starts with provenance lines.
export type Cell = string | number | null | undefined;

const csvCell = (v: Cell) => {
  if (v === null || v === undefined) return "";
  let s = String(v);
  if (/^[=+\-@\t\r]/.test(s) && typeof v === "string") s = "'" + s; // spreadsheet formula injection guard
  return /[",;\n\r]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
};

export function toCSV(header: string[], rows: Cell[][], provenance: string[]): string {
  return [...provenance.map((p) => csvCell("# " + p)), header.map(csvCell).join(","), ...rows.map((r) => r.map(csvCell).join(","))].join("\r\n");
}

export function download(name: string, content: BlobPart, type: string) {
  const url = URL.createObjectURL(new Blob([content], { type }));
  const a = document.createElement("a");
  a.href = url;
  a.download = name;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

export function downloadCSV(name: string, header: string[], rows: Cell[][], provenance: string[]) {
  download(name.endsWith(".csv") ? name : `${name}.csv`, "﻿" + toCSV(header, rows, provenance), "text/csv;charset=utf-8");
}

export async function downloadXLSX(name: string, header: string[], rows: Cell[][], provenance: string[]) {
  const { default: writeXlsxFile } = await import("write-excel-file/browser");
  const data = [
    ...provenance.map((p) => [{ value: p, fontStyle: "italic" as const }]),
    header.map((h) => ({ value: h, fontWeight: "bold" as const })),
    ...rows.map((r) => r.map((v) => (v === null || v === undefined ? null : { value: typeof v === "number" ? v : String(v) }))),
  ];
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const blob = await writeXlsxFile(data as any).toBlob();
  download(name.endsWith(".xlsx") ? name : `${name}.xlsx`, blob, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
}
