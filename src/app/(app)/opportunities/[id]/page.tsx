import { notFound } from "next/navigation";
import { requireUser } from "@/lib/auth/guards";
import { prisma } from "@/lib/db";
import { Card, SectionTitle, Stat, Badge, RatingBadge, EmptyState } from "@/components/ui";
import { ActionForm, SubmitButton } from "@/components/action-form";
import { CoverageDonut, ScoreBars } from "@/components/charts";
import {
  runPrefeasibilityAction,
  qualifyAction,
  runMatchingAction,
  generateConceptNoteAction,
} from "@/lib/actions/analysis";
import { updateStageAction } from "@/lib/actions/opportunities";
import { submitEoiAction, respondEoiAction } from "@/lib/actions/interactions";
import { updateMatchStatusAction } from "@/lib/actions/interactions";
import {
  fmtInt,
  fmtNum,
  fmtPct,
  fmtMoney,
  fmtKwhToMwh,
  STAGE_LABELS,
  CRITICALITY_LABELS,
} from "@/lib/format";
import { MessageThread } from "@/components/message-thread";

const STAGES = Object.keys(STAGE_LABELS);

export default async function OpportunityDetailPage({ params }: { params: { id: string } }) {
  const session = await requireUser();
  const opp = await prisma.opportunity.findFirst({
    where: { id: params.id, deletedAt: null },
    include: {
      site: { include: { organization: true } },
      owner: true,
      prefeasibility: { include: { technoEconomicModel: true } },
      decarbonization: { include: { gridEmissionFactor: true } },
      bankability: true,
      matches: {
        orderBy: { compatibilityScore: "desc" },
        include: { developerProfile: { include: { organization: true } } },
      },
      expressions: { include: { developerProfile: { include: { organization: true } } } },
      conceptNotes: { orderBy: { version: "desc" } },
      messages: { include: { sender: true, recipient: true }, orderBy: { createdAt: "asc" } },
    },
  });
  if (!opp) notFound();

  const isOwner = opp.site.organizationId === session.organizationId;
  const isAdmin = session.role === "admin";
  const isDeveloper = session.role === "developer";
  const canAnalyze = isOwner || isAdmin;

  // Un développeur ne voit que les opportunités qualifiées.
  if (isDeveloper && opp.qualificationStatus !== "qualifiee") notFound();
  if (!isOwner && !isAdmin && !isDeveloper) notFound();

  const pf = opp.prefeasibility;
  const te = pf?.technoEconomicModel;
  const dec = opp.decarbonization;
  const bank = opp.bankability;

  // Contexte développeur : profil + EOI existante.
  let devProfile = null;
  let existingEoi = null;
  if (isDeveloper) {
    devProfile = await prisma.developerProfile.findUnique({ where: { organizationId: session.organizationId } });
    if (devProfile) {
      existingEoi = opp.expressions.find((e) => e.developerProfileId === devProfile!.id) ?? null;
    }
  }

  // Destinataire de la messagerie (l'autre partie du fil).
  let recipientUserId: string | null = null;
  if (isDeveloper) {
    recipientUserId = opp.ownerUserId; // développeur → chargé d'origination
  } else {
    // Offtaker / admin → dernier interlocuteur développeur ayant écrit.
    const lastIncoming = [...opp.messages].reverse().find((m) => m.senderUserId !== session.userId);
    recipientUserId = lastIncoming?.senderUserId ?? null;
  }

  return (
    <div className="space-y-6">
      {/* En-tête */}
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold">{opp.title}</h1>
          <p className="text-sm text-navy-500">
            {opp.site.organization.name} · {opp.site.name} · {opp.site.country} ·{" "}
            criticité {CRITICALITY_LABELS[opp.site.loadCriticality]}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge tone="muted">{STAGE_LABELS[opp.stage]}</Badge>
          <Badge tone={opp.qualificationStatus === "qualifiee" ? "vert" : "muted"}>
            {opp.qualificationStatus === "qualifiee"
              ? "Qualifiée"
              : opp.qualificationStatus === "rejetee"
                ? "Rejetée"
                : "Non qualifiée"}
          </Badge>
          {bank && <RatingBadge rating={bank.rating} />}
        </div>
      </div>

      {/* Objectifs mesurés */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Stat label="Couverture cible" value={fmtPct(opp.targetReliabilityRate)} accent="gold" />
        <Stat label="Couverture atteinte" value={pf ? fmtPct(pf.coverageRate) : "—"} accent="gold" hint="Sécurité d'appro." />
        <Stat label="CO₂ évité / an" value={dec ? `${fmtInt(dec.annualCo2AvoidedTonnes)} t` : "—"} accent="vert" hint="Décarbonisation" />
        <Stat label="TRI" value={te?.irr != null ? fmtPct(te.irr) : "—"} accent="navy" />
      </div>

      {/* Qualification (IA) */}
      <Card>
        <SectionTitle
          action={
            canAnalyze ? (
              <ActionForm action={qualifyAction}>
                <input type="hidden" name="opportunityId" value={opp.id} />
                <SubmitButton variant="ghost">Qualifier (IA)</SubmitButton>
              </ActionForm>
            ) : undefined
          }
        >
          Qualification
        </SectionTitle>
        {opp.qualificationSummary ? (
          <p className="whitespace-pre-wrap text-sm text-navy-700">{opp.qualificationSummary}</p>
        ) : (
          <EmptyState title="Non qualifiée">
            {canAnalyze ? "Lancez la qualification IA pour une synthèse chiffrée." : "En attente de qualification."}
          </EmptyState>
        )}
      </Card>

      {/* Pré-faisabilité */}
      <Card>
        <SectionTitle
          action={
            canAnalyze ? (
              <ActionForm action={runPrefeasibilityAction} className="flex items-end gap-2">
                <input type="hidden" name="opportunityId" value={opp.id} />
                <div>
                  <label className="text-xs text-navy-400">Ratio perf.</label>
                  <input name="performanceRatio" type="number" step="0.01" min="0.5" max="0.95" placeholder="0.80" className="input w-24 py-1" />
                </div>
                <SubmitButton variant="primary">Lancer la pré-faisabilité</SubmitButton>
              </ActionForm>
            ) : undefined
          }
        >
          Pré-faisabilité — dimensionnement à fiabilité cible
        </SectionTitle>

        {!pf ? (
          <EmptyState title="Pas encore d'étude">
            {canAnalyze
              ? "Le moteur calcule le productible (NASA POWER), simule 8760 h et dimensionne PV + batterie + appoint."
              : "Analyse en attente."}
          </EmptyState>
        ) : (
          <div className="grid gap-6 lg:grid-cols-[auto,1fr]">
            <div className="flex flex-col items-center">
              <CoverageDonut coverage={pf.coverageRate} />
              <p className="mt-2 text-center text-xs text-navy-400">
                {pf.coverageRate >= opp.targetReliabilityRate ? "Cible atteinte" : "Meilleur effort (cible non atteinte)"}
              </p>
            </div>
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-3">
              <MiniStat label="PV dimensionné" value={`${fmtInt(pf.pvSizeKwp)} kWc`} />
              <MiniStat label="Batterie" value={`${fmtInt(pf.batterySizeKwh)} kWh`} />
              <MiniStat label="Appoint" value={`${fmtInt(pf.backupSizeKw)} kW`} />
              <MiniStat label="Productible annuel" value={fmtKwhToMwh(pf.annualYieldKwh)} />
              <MiniStat label="Déficit résiduel" value={fmtKwhToMwh(pf.residualDeficitKwh)} />
              <MiniStat label="Coût de la fiabilité" value={`${fmtInt(pf.reliabilityCost)} /an`} />
              <div className="col-span-2 sm:col-span-3">
                <Badge tone="muted">
                  Méthode : {pf.simulationMethod === "cible_fixee" ? "cible fixée" : "optimisation économique"}
                </Badge>{" "}
                <span className="text-xs text-navy-400">
                  {(pf.assumptions as { productibleSource?: string } | null)?.productibleSource === "nasa_power"
                    ? "Productible NASA POWER"
                    : "Productible synthétique (repli)"}
                </span>
              </div>
            </div>
          </div>
        )}
      </Card>

      {/* Technico-économique + Décarbonisation + Bancabilité */}
      <div className="grid gap-6 lg:grid-cols-3">
        <Card>
          <SectionTitle>Technico-économique</SectionTitle>
          {te ? (
            <dl className="space-y-2 text-sm">
              <Row label="CAPEX" value={fmtMoney(te.capex, te.currency)} />
              <Row label="OPEX / an" value={fmtMoney(te.opexAnnual, te.currency)} />
              <Row label="Tarif PPA" value={`${fmtNum(te.ppaTariff, 3)} ${te.currency}/kWh`} />
              <Row label="TRI" value={te.irr != null ? fmtPct(te.irr) : "n/d"} />
              <Row label="Payback" value={te.paybackYears != null ? `${fmtNum(te.paybackYears)} ans` : "n/d"} />
              <Row label="Économie / an" value={fmtMoney(te.annualSavings, te.currency)} />
            </dl>
          ) : (
            <EmptyState title="Calculé avec la pré-faisabilité" />
          )}
        </Card>

        <Card>
          <SectionTitle>Décarbonisation</SectionTitle>
          {dec ? (
            <dl className="space-y-2 text-sm">
              <Row label="CO₂ évité / an" value={`${fmtInt(dec.annualCo2AvoidedTonnes)} tCO₂`} />
              <Row label="CO₂ évité (durée de vie)" value={`${fmtInt(dec.lifetimeCo2AvoidedTonnes)} tCO₂`} />
              <Row
                label="Facteur d'émission"
                value={dec.gridEmissionFactor ? `${fmtNum(dec.gridEmissionFactor.emissionFactorTco2PerMwh, 2)} tCO₂/MWh` : "n/d"}
              />
              <Row label="Pays" value={opp.site.country} />
            </dl>
          ) : (
            <EmptyState title="Calculé avec la pré-faisabilité" />
          )}
        </Card>

        <Card>
          <SectionTitle>Bancabilité & résilience</SectionTitle>
          {bank ? (
            <>
              <div className="mb-3 flex items-center gap-3">
                <RatingBadge rating={bank.rating} />
                <span className="text-lg font-semibold">{(bank.totalScore * 100).toFixed(0)}/100</span>
              </div>
              <ScoreBars
                scores={[
                  { label: "Financier", value: bank.financialScore, tone: "navy" },
                  { label: "Technique", value: bank.technicalScore, tone: "gold" },
                  { label: "Résilience", value: bank.resilienceScore, tone: "vert" },
                  { label: "Climat", value: bank.decarbonizationScore, tone: "vert" },
                ]}
              />
            </>
          ) : (
            <EmptyState title="Calculé avec la pré-faisabilité" />
          )}
        </Card>
      </div>

      {/* Matching */}
      <Card>
        <SectionTitle
          action={
            canAnalyze && pf ? (
              <ActionForm action={runMatchingAction}>
                <input type="hidden" name="opportunityId" value={opp.id} />
                <SubmitButton variant="primary">Lancer le matching</SubmitButton>
              </ActionForm>
            ) : undefined
          }
        >
          Moteur de matching
        </SectionTitle>
        {opp.matches.length === 0 ? (
          <EmptyState title="Aucun appariement">
            {canAnalyze ? "Lancez le matching pondéré (nécessite la pré-faisabilité)." : "En attente."}
          </EmptyState>
        ) : (
          <ul className="space-y-3">
            {opp.matches.map((m) => (
              <li key={m.id} className="rounded-lg border border-navy-100 p-4">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="font-medium text-navy-800">{m.developerProfile.organization.name}</div>
                  <div className="flex items-center gap-2">
                    <span className="text-lg font-semibold text-gold-600">
                      {(m.compatibilityScore * 100).toFixed(0)}%
                    </span>
                    <Badge tone={m.status === "valide_admin" ? "vert" : m.status === "ecarte" ? "muted" : "navy"}>
                      {m.status === "valide_admin" ? "Validé" : m.status === "ecarte" ? "Écarté" : "Proposé"}
                    </Badge>
                  </div>
                </div>
                <div className="mt-2 grid grid-cols-2 gap-2 text-xs text-navy-500 sm:grid-cols-4">
                  <span>Géo {(m.geographyScore * 100).toFixed(0)}%</span>
                  <span>Techno {(m.technologyScore * 100).toFixed(0)}%</span>
                  <span>Taille {(m.sizeScore * 100).toFixed(0)}%</span>
                  <span>Banca. {(m.bankabilityAlignment * 100).toFixed(0)}%</span>
                </div>
                {m.explanation && <p className="mt-2 text-sm text-navy-600">{m.explanation}</p>}
                {isAdmin && m.status !== "valide_admin" && (
                  <div className="mt-3 flex gap-2">
                    <ActionForm action={updateMatchStatusAction}>
                      <input type="hidden" name="matchId" value={m.id} />
                      <input type="hidden" name="status" value="valide_admin" />
                      <SubmitButton variant="vert">Valider</SubmitButton>
                    </ActionForm>
                    <ActionForm action={updateMatchStatusAction}>
                      <input type="hidden" name="matchId" value={m.id} />
                      <input type="hidden" name="status" value="ecarte" />
                      <SubmitButton variant="ghost">Écarter</SubmitButton>
                    </ActionForm>
                  </div>
                )}
              </li>
            ))}
          </ul>
        )}
      </Card>

      {/* Note de concept */}
      <Card>
        <SectionTitle
          action={
            canAnalyze && te ? (
              <ActionForm action={generateConceptNoteAction}>
                <input type="hidden" name="opportunityId" value={opp.id} />
                <SubmitButton variant="gold">Générer une note (IA)</SubmitButton>
              </ActionForm>
            ) : undefined
          }
        >
          Notes de concept chiffrées
        </SectionTitle>
        {opp.conceptNotes.length === 0 ? (
          <EmptyState title="Aucune note">
            {canAnalyze ? "Générez une note (économie + CO₂ évité + fiabilité)." : "En attente."}
          </EmptyState>
        ) : (
          <div className="space-y-3">
            {opp.conceptNotes.map((n) => (
              <details key={n.id} className="rounded-lg border border-navy-100 p-3">
                <summary className="cursor-pointer text-sm font-medium">
                  Version {n.version} · {n.generatedBy === "ia" ? "IA" : "Humain"} ·{" "}
                  {n.createdAt.toLocaleDateString("fr-FR")}
                </summary>
                <pre className="mt-2 whitespace-pre-wrap font-sans text-sm text-navy-700">{n.content}</pre>
              </details>
            ))}
          </div>
        )}
      </Card>

      {/* Développeur : expression d'intérêt */}
      {isDeveloper && (
        <Card>
          <SectionTitle>Expression d'intérêt</SectionTitle>
          {!devProfile ? (
            <EmptyState title="Complétez votre profil développeur pour manifester votre intérêt." />
          ) : existingEoi ? (
            <p className="text-sm">
              Intérêt {existingEoi.status === "acceptee" ? "accepté ✅" : existingEoi.status === "refusee" ? "refusé" : "soumis, en attente"}.
              {existingEoi.message && <span className="mt-1 block text-navy-500">« {existingEoi.message} »</span>}
            </p>
          ) : (
            <ActionForm action={submitEoiAction} className="space-y-3">
              <input type="hidden" name="opportunityId" value={opp.id} />
              <textarea name="message" className="textarea" rows={3} placeholder="Note d'intention (optionnelle)…" />
              <SubmitButton variant="vert">Manifester mon intérêt</SubmitButton>
            </ActionForm>
          )}
        </Card>
      )}

      {/* Offtaker/Admin : expressions d'intérêt reçues */}
      {canAnalyze && (
        <Card>
          <SectionTitle>Expressions d'intérêt reçues</SectionTitle>
          {opp.expressions.length === 0 ? (
            <EmptyState title="Aucune expression d'intérêt" />
          ) : (
            <ul className="space-y-2">
              {opp.expressions.map((e) => (
                <li key={e.id} className="flex items-center justify-between rounded-lg border border-navy-100 p-3">
                  <div>
                    <div className="font-medium">{e.developerProfile.organization.name}</div>
                    {e.message && <div className="text-sm text-navy-500">« {e.message} »</div>}
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge tone={e.status === "acceptee" ? "vert" : e.status === "refusee" ? "muted" : "navy"}>
                      {e.status === "acceptee" ? "Acceptée" : e.status === "refusee" ? "Refusée" : "Soumise"}
                    </Badge>
                    {e.status === "soumise" && (
                      <>
                        <ActionForm action={respondEoiAction}>
                          <input type="hidden" name="eoiId" value={e.id} />
                          <input type="hidden" name="status" value="acceptee" />
                          <SubmitButton variant="vert">Accepter</SubmitButton>
                        </ActionForm>
                        <ActionForm action={respondEoiAction}>
                          <input type="hidden" name="eoiId" value={e.id} />
                          <input type="hidden" name="status" value="refusee" />
                          <SubmitButton variant="ghost">Refuser</SubmitButton>
                        </ActionForm>
                      </>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          )}
        </Card>
      )}

      {/* Messagerie */}
      <MessageThread
        opportunityId={opp.id}
        currentUserId={session.userId}
        ownerUserId={opp.ownerUserId}
        messages={opp.messages.map((m) => ({
          id: m.id,
          body: m.body,
          senderName: m.sender.fullName,
          fromMe: m.senderUserId === session.userId,
          at: m.createdAt.toLocaleString("fr-FR"),
        }))}
        canCompose={Boolean(opp.ownerUserId)}
        isOwner={isOwner}
        recipientUserId={recipientUserId}
      />

      {/* Progression du pipeline */}
      {canAnalyze && (
        <Card>
          <SectionTitle>Pipeline</SectionTitle>
          <ActionForm action={updateStageAction} className="flex flex-wrap items-end gap-3">
            <input type="hidden" name="opportunityId" value={opp.id} />
            <div>
              <label className="label">Étape</label>
              <select name="stage" defaultValue={opp.stage} className="select">
                {STAGES.map((s) => (
                  <option key={s} value={s}>{STAGE_LABELS[s]}</option>
                ))}
              </select>
            </div>
            <SubmitButton variant="ghost">Mettre à jour</SubmitButton>
          </ActionForm>
        </Card>
      )}
    </div>
  );
}

function MiniStat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg bg-navy-50 p-3">
      <div className="text-xs text-navy-400">{label}</div>
      <div className="font-semibold text-navy-800">{value}</div>
    </div>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between border-b border-navy-50 pb-1">
      <dt className="text-navy-400">{label}</dt>
      <dd className="font-medium text-navy-800">{value}</dd>
    </div>
  );
}
