"use client";

import { useState, type FormEvent } from "react";
import { Plus } from "lucide-react";
import { Field } from "@/components/field";
import { ErrorBox, Loading } from "@/components/page";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input, Select } from "@/components/ui/input";
import { Table, TableWrap, Td, Th } from "@/components/ui/table";
import { api, ApiError, orgPath } from "@/lib/api";
import { MILESTONE_STATUSES } from "@/lib/constants";
import { date } from "@/lib/format";
import { useApi } from "@/lib/hooks";
import { useI18n, type DictKey } from "@/lib/i18n";
import { useSession } from "@/lib/session";
import type { Milestone, Project } from "@/lib/types";

const CATEGORIES = ["permitting", "technical", "financing", "procurement", "construction", "commercial", "other"];

export function MilestonesTab({ project }: { project: Project }) {
  const { org, canEdit } = useSession();
  const { t, locale } = useI18n();
  const path = org ? orgPath(org.id, `/projects/${project.id}/milestones`) : null;
  const list = useApi<Milestone[]>(path);
  const [f, setF] = useState({ title: "", category: "other", due_date: "", owner_name: "", status: "open" });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function add(e: FormEvent) {
    e.preventDefault();
    if (!path) return;
    setBusy(true);
    setError(null);
    setErrors({});
    try {
      await api(path, { method: "POST", body: { ...f, due_date: f.due_date || null, owner_name: f.owner_name || null } });
      setF({ title: "", category: "other", due_date: "", owner_name: "", status: "open" });
      list.reload();
    } catch (err) {
      if (err instanceof ApiError) setErrors(err.fieldErrors());
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setBusy(false);
    }
  }

  async function setStatus(m: Milestone, status: string) {
    if (!path) return;
    try {
      await api(`${path}/${m.id}`, { method: "PUT", body: { title: m.title, category: m.category, due_date: m.due_date, owner_name: m.owner_name, status } });
      list.reload();
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    }
  }

  return (
    <div className="grid gap-6 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)]">
      <Card>
        <CardHeader>
          <CardTitle>{t("ms.title")}</CardTitle>
        </CardHeader>
        <CardContent>
          {list.loading && !list.data ? <Loading /> : null}
          {list.error ? <ErrorBox error={list.error} onRetry={list.reload} /> : null}
          {list.data && list.data.length === 0 ? <p className="text-sm text-muted-foreground">{t("ms.empty")}</p> : null}
          {list.data && list.data.length > 0 ? (
            <TableWrap>
              <Table>
                <thead>
                  <tr>
                    <Th>{t("ms.title")}</Th>
                    <Th>{t("ms.category")}</Th>
                    <Th>{t("ms.due")}</Th>
                    <Th>{t("ms.owner")}</Th>
                    <Th>{t("common.status")}</Th>
                  </tr>
                </thead>
                <tbody>
                  {list.data.map((m) => (
                    <tr key={m.id}>
                      <Td className="font-medium">{m.title}</Td>
                      <Td className="text-muted-foreground">{m.category}</Td>
                      <Td className="whitespace-nowrap">{date(m.due_date, locale)}</Td>
                      <Td>{m.owner_name ?? "–"}</Td>
                      <Td>
                        <Select aria-label={`${t("common.status")}: ${m.title}`} className="h-8 w-36 text-xs" value={m.status} disabled={!canEdit} onChange={(e) => setStatus(m, e.target.value)}>
                          {MILESTONE_STATUSES.map((s) => (
                            <option key={s} value={s}>
                              {t(`ms.status.${s}` as DictKey)}
                            </option>
                          ))}
                        </Select>
                      </Td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </TableWrap>
          ) : null}
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>{t("ms.add")}</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={add} className="flex flex-col gap-3">
            <Field label={t("ms.title")} error={errors.title}>
              {(id, d, inv) => <Input id={id} aria-describedby={d} aria-invalid={inv} required maxLength={200} value={f.title} disabled={!canEdit} onChange={(e) => setF({ ...f, title: e.target.value })} />}
            </Field>
            <Field label={t("ms.category")} error={errors.category}>
              {(id, d) => (
                <Select id={id} aria-describedby={d} value={f.category} disabled={!canEdit} onChange={(e) => setF({ ...f, category: e.target.value })}>
                  {CATEGORIES.map((c) => (
                    <option key={c} value={c}>
                      {c}
                    </option>
                  ))}
                </Select>
              )}
            </Field>
            <Field label={t("ms.due")} error={errors.due_date}>
              {(id, d, inv) => <Input id={id} type="date" aria-describedby={d} aria-invalid={inv} value={f.due_date} disabled={!canEdit} onChange={(e) => setF({ ...f, due_date: e.target.value })} />}
            </Field>
            <Field label={`${t("ms.owner")} (${t("common.optional")})`} error={errors.owner_name}>
              {(id, d) => <Input id={id} aria-describedby={d} value={f.owner_name} disabled={!canEdit} onChange={(e) => setF({ ...f, owner_name: e.target.value })} />}
            </Field>
            <Field label={t("common.status")} error={errors.status}>
              {(id, d) => (
                <Select id={id} aria-describedby={d} value={f.status} disabled={!canEdit} onChange={(e) => setF({ ...f, status: e.target.value })}>
                  {MILESTONE_STATUSES.map((s) => (
                    <option key={s} value={s}>
                      {t(`ms.status.${s}` as DictKey)}
                    </option>
                  ))}
                </Select>
              )}
            </Field>
            {error ? <Alert variant="danger">{error}</Alert> : null}
            <Button type="submit" disabled={!canEdit || busy || !f.title}>
              <Plus aria-hidden /> {t("common.add")}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
