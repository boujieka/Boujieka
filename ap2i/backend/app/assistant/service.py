"""AP²I Intelligence Assistant (Master prompt §22).

Architecture (provider-agnostic, retrieval-first):
  1. Parse the question into a structured query (donor, sector, years, intent) — deterministic.
  2. Retrieve ONLY authorised database records (tenant isolation applies) and compute transparent
     calculations.
  3. Return a structured answer: facts / calculations / interpretations / recommendations /
     missing information, with citations to AP²I identifiers and source records.
  4. Optionally (AP2I_LLM_PROVIDER != "none") ask an LLM to phrase a short narrative from the
     facts only. The narrative is checked: every number it contains must appear in the facts,
     otherwise it is discarded. Untrusted text (descriptions, documents) is fenced as data.
Without an LLM the assistant still answers — it never needs a model to be truthful.
"""

from __future__ import annotations

import json
import re
import unicodedata
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.assistant.safety import SYSTEM_GUARD, wrap_untrusted
from app.config import get_settings
from app.finance.fx import FX
from app.finance.indicators import agreement_position, ratio
from app.models import (
    Country,
    FinancingAgreement,
    FinancingCommitment,
    FinancingPartner,
    Project,
    ProjectAlert,
    Sector,
)
from app.reference.catalog import DONORS

DONOR_PATTERNS = {
    "WB": [r"world ?bank", r"banque mondiale", r"\bibrd\b", r"\bida\b", r"\bbird\b"],
    "AFDB": [r"\bafdb\b", r"\bbad\b", r"african development bank", r"banque africaine de d[eé]veloppement"],
    "AFD": [r"\bafd\b", r"agence fran[cç]aise de d[eé]veloppement"],
    "EIB": [r"\beib\b", r"\bbei\b", r"european investment bank", r"banque europ[eé]enne d'investissement"],
    "EU": [r"european union", r"union europ[eé]enne", r"\beu\b", r"\bue\b"],
    "IFAD": [r"\bifad\b", r"\bfida\b"], "UNDP": [r"\bundp\b", r"\bpnud\b"], "UNICEF": [r"unicef"],
    "FAO": [r"\bfao\b"], "UNIDO": [r"unido", r"onudi"], "BMZ": [r"\bbmz\b"],
    "ISDB": [r"\bisdb\b", r"\bbid\b", r"islamic development bank"], "JICA": [r"jica"], "KFW": [r"kfw"],
}
SECTOR_PATTERNS = {
    "ENERGY": [r"energ", r"electri", r"power", r"hydro"], "TRANSPORT": [r"transport", r"road", r"rout", r"highway"],
    "WATER": [r"water", r"\beau\b", r"sanitation", r"assainissement"], "HEALTH": [r"health", r"sant[eé]", r"hospital", r"h[oô]pital"],
    "EDUCATION": [r"educat", r"school", r"[eé]cole"], "AGRICULTURE": [r"agricultur", r"agricole", r"rural"],
    "DIGITAL": [r"digital", r"num[eé]rique", r"\bict\b", r"\btic\b", r"broadband"],
    "URBAN": [r"urban", r"urbain"], "ENVIRONMENT": [r"environment", r"environnement"], "CLIMATE": [r"climat"],
    "MINING": [r"mining", r"\bmines?\b", r"minier"], "PUBADMIN": [r"public administration", r"administration publique", r"governance", r"gouvernance"],
    "INDUSTRY": [r"industr"], "HOUSING": [r"housing", r"logement"],
}
INFRA_HINT = [r"infrastructure"]


@dataclass
class ParsedQuery:
    intent: str
    donors: list[str] = field(default_factory=list)
    sectors: list[str] = field(default_factory=list)
    year_from: int | None = None
    year_to: int | None = None
    country: str = "CMR"
    project_ref: str | None = None
    language: str = "en"


def _norm(q: str) -> str:
    return unicodedata.normalize("NFC", q.lower())


def parse(question: str, default_country: str) -> ParsedQuery:
    q = _norm(question)
    lang = "fr" if re.search(r"\b(les|des|projets|quels|quelles|entre|depuis|engagements|décaiss|décaissement)\b", q) else "en"
    donors = [code for code, pats in DONOR_PATTERNS.items() if any(re.search(p, q) for p in pats)]
    sectors = [code for code, pats in SECTOR_PATTERNS.items() if any(re.search(p, q) for p in pats)]
    years = [int(y) for y in re.findall(r"\b(19[6-9]\d|20[0-4]\d)\b", q)]
    yf = yt = None
    if len(years) >= 2:
        yf, yt = min(years[:2]), max(years[:2])
    elif len(years) == 1:
        if re.search(r"since|depuis|after|apr[eè]s", q):
            yf = years[0]
        else:
            yf = yt = years[0]
    ref = None
    m = re.search(r"ap2i-[a-z]{3}-[a-z]+-\d{6}", q)
    if m:
        ref = m.group(0).upper()
    country = default_country
    for iso3, names in (("CMR", ("cameroon", "cameroun")),):
        if any(n in q for n in names):
            country = iso3
    if re.search(r"recovery|rescue|redressement|plan d'action|corrective|correctiv", q):
        intent = "recovery_plan"
    elif re.search(r"low disburse|faible(s)? d[eé]caiss|slow disburse|d[eé]caissement(s)? faible", q):
        intent = "low_disbursement"
    elif re.search(r"not operational|non[- ]op[eé]rationnel|non fonctionnel|not in operation", q):
        intent = "completed_not_operational"
    elif re.search(r"compar", q) and len(donors) >= 2:
        intent = "compare_commitments"
    elif re.search(r"annual|annuel|per year|par an|by year|par ann[eé]e", q) and re.search(r"commit|engagement|invest", q):
        intent = "annual_commitments"
    else:
        intent = "list_projects"
    return ParsedQuery(intent, donors, sectors, yf, yt, country, ref, lang)


@dataclass
class Answer:
    question: str
    parsed: dict
    facts: list[dict] = field(default_factory=list)
    calculations: list[dict] = field(default_factory=list)
    interpretations: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    missing_information: list[str] = field(default_factory=list)
    citations: list[dict] = field(default_factory=list)
    narrative: str | None = None
    provider: str = "none"
    grounding: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {k: getattr(self, k) for k in ("question", "parsed", "facts", "calculations", "interpretations",
                                              "recommendations", "missing_information", "citations", "narrative",
                                              "provider", "grounding")} | {
            "data_nature": {"facts": "officially_reported", "calculations": "calculated",
                            "interpretations": "calculated (rule-based)", "narrative": "ai_generated" if self.narrative else None},
            "disclaimer": "Answers use only records imported into AP²I; coverage is limited to the connected sources.",
        }


def _project_query(db: Session, pq: ParsedQuery, tenant_cond):
    country = db.scalar(select(Country).where(Country.iso3 == pq.country))
    q = select(Project).where(Project.merged_into_id.is_(None), tenant_cond).options(
        selectinload(Project.agreements).selectinload(FinancingAgreement.partner), selectinload(Project.sector))
    if country:
        q = q.where(Project.country_id == country.id)
    if pq.sectors:
        q = q.join(Sector, Sector.id == Project.sector_id).where(Sector.code.in_(pq.sectors))
    return q


def _in_years(d: date | None, pq: ParsedQuery) -> bool:
    if pq.year_from is None and pq.year_to is None:
        return True
    if d is None:
        return False
    return (pq.year_from is None or d.year >= pq.year_from) and (pq.year_to is None or d.year <= pq.year_to)


def _approval(p: Project) -> date | None:
    ds = [a.approval_date for a in p.agreements if a.approval_date]
    return p.original_approval_date or (min(ds) if ds else None)


def _cite(p: Project) -> dict:
    return {"ap2i_id": p.ap2i_id, "project_id": p.id, "title": p.title,
            "sources": sorted({a.source_identifier for a in p.agreements})}


def answer(db: Session, question: str, tenant_cond, default_country: str = "CMR") -> Answer:
    pq = parse(question, default_country)
    ans = Answer(question=question, parsed=pq.__dict__.copy())
    partners = {p.code: p for p in db.scalars(select(FinancingPartner))}
    donor_ids = {partners[c].id for c in pq.donors if c in partners}
    unknown = [c for c in pq.donors if c not in partners]
    if unknown:
        ans.missing_information.append(f"No financing partner registered for: {', '.join(unknown)}")
    projects = list(db.scalars(_project_query(db, pq, tenant_cond)).unique())
    if donor_ids:
        projects = [p for p in projects if any(a.partner_id in donor_ids for a in p.agreements)]
    no_connector = [d["short_name"] for d in DONORS if d["code"] in pq.donors and not d.get("connector_key")]
    if no_connector:
        ans.missing_information.append(f"No automated data source for {', '.join(no_connector)}: results may be incomplete.")

    if pq.intent == "low_disbursement":
        alerts = db.scalars(select(ProjectAlert).where(ProjectAlert.rule_code == "LOW_DISBURSEMENT", ProjectAlert.is_active.is_(True),
                                                       ProjectAlert.project_id.in_([p.id for p in projects]))).all()
        by_id = {p.id: p for p in projects}
        for a in alerts:
            p = by_id[a.project_id]
            ans.facts.append({"ap2i_id": p.ap2i_id, "title": p.title, "observed": a.observed_value, "alert_id": a.public_id,
                              "level": a.level, "source": a.source})
            ans.citations.append(_cite(p))
        ans.calculations.append({"name": "rule", "formula": "LOW_DISBURSEMENT: disbursed/committed ≤ threshold while elapsed share ≥ threshold",
                                 "thresholds": "see /api/v1/alerts/rules"})
        with_data = sum(1 for p in projects if any(agreement_position(db, a).disbursed is not None for a in p.agreements))
        ans.missing_information.append(f"{len(projects) - with_data} of {len(projects)} matching projects have no published disbursement figure and cannot be assessed.")
        ans.interpretations.append(f"{len(alerts)} financing(s) meet the low-disbursement rule. This is a signal for verification, not a finding of mismanagement.")
        if alerts:
            ans.recommendations.append("Open each project in Project Rescue to review the evidence and draft a verification plan.")
    elif pq.intent == "completed_not_operational":
        done = [p for p in projects if p.status in ("completed", "closed")]
        not_op = [p for p in done if p.operational_status == "not_operational"]
        unknown_op = [p for p in done if p.operational_status == "unknown"]
        for p in not_op:
            ans.facts.append({"ap2i_id": p.ap2i_id, "title": p.title, "status": p.status, "operational_status": p.operational_status})
            ans.citations.append(_cite(p))
        ans.calculations.append({"name": "completed_projects", "value": len(done)})
        ans.missing_information.append(f"Operational status is undocumented for {len(unknown_op)} of {len(done)} completed/closed projects; "
                                       "they cannot be classified as operational or not.")
        ans.interpretations.append(f"{len(not_op)} completed project(s) are documented as not operational.")
    elif pq.intent == "compare_commitments":
        fx = FX(db)
        for code in pq.donors:
            if code not in partners:
                continue
            pid = partners[code].id
            per_cur: dict[str, Decimal] = defaultdict(Decimal)
            usd = Decimal(0)
            unconverted = Decimal(0)
            n = 0
            for p in projects:
                for a in p.agreements:
                    if a.partner_id != pid:
                        continue
                    for c in db.scalars(select(FinancingCommitment).where(FinancingCommitment.agreement_id == a.id,
                                                                          FinancingCommitment.is_counted.is_(True))):
                        if not _in_years(c.value_date, pq):
                            continue
                        per_cur[c.currency] += c.amount
                        n += 1
                        conv = fx.convert(c.amount, c.currency, "USD", c.value_date.year if c.value_date else None)
                        if conv.value is None:
                            unconverted += 1
                        else:
                            usd += conv.value
            ans.facts.append({"partner": partners[code].short_name, "commitments_by_currency": {k: str(v) for k, v in per_cur.items()},
                              "transactions": n})
            ans.calculations.append({"partner": partners[code].short_name, "usd_equivalent": str(usd.quantize(Decimal('0.01'))),
                                     "method": "each commitment converted at the annual average rate of its year",
                                     "unconverted_transactions": int(unconverted)})
        ans.interpretations.append("Totals cover only commitments recorded in AP²I's connected sources for the selected period.")
    elif pq.intent == "annual_commitments":
        fx = FX(db)
        yf, yt = pq.year_from or 2011, pq.year_to or 2026
        rows: dict[int, dict] = {y: {"by_currency": defaultdict(Decimal), "usd": Decimal(0), "unconverted": 0} for y in range(yf, yt + 1)}
        for p in projects:
            for a in p.agreements:
                if donor_ids and a.partner_id not in donor_ids:
                    continue
                for c in db.scalars(select(FinancingCommitment).where(FinancingCommitment.agreement_id == a.id,
                                                                      FinancingCommitment.is_counted.is_(True))):
                    if c.value_date and yf <= c.value_date.year <= yt:
                        slot = rows[c.value_date.year]
                        slot["by_currency"][c.currency] += c.amount
                        conv = fx.convert(c.amount, c.currency, "USD", c.value_date.year)
                        if conv.value is None:
                            slot["unconverted"] += 1
                        else:
                            slot["usd"] += conv.value
        for y, slot in rows.items():
            ans.facts.append({"year": y, "commitments_by_currency": {k: str(v) for k, v in slot["by_currency"].items()}})
            ans.calculations.append({"year": y, "usd_equivalent": str(slot["usd"].quantize(Decimal('0.01'))),
                                     "unconverted_transactions": slot["unconverted"]})
        ans.missing_information.append("Government-funded investment (national budget) is not included unless budget data was imported.")
    elif pq.intent == "recovery_plan":
        from app.rescue.engine import PLAYBOOK, diagnose

        target = None
        if pq.project_ref:
            target = next((p for p in projects if p.ap2i_id == pq.project_ref), None)
        if target is None:
            ans.missing_information.append("Name the project with its AP²I identifier (e.g. AP2I-CMR-ENERGY-000001) to draft a recovery plan.")
        else:
            diag = diagnose(db, target)
            ans.facts.append({"ap2i_id": target.ap2i_id, "alerts": diag["alerts"]})
            ans.citations.append(_cite(target))
            for al in diag["alerts"]:
                if al["rule"] in PLAYBOOK:
                    ans.recommendations.append(f"[{al['alert_id']}] {PLAYBOOK[al['rule']][1]}")
            if not diag["alerts"]:
                ans.recommendations.append("No active alert for this project. Further investigation required.")
            ans.interpretations.append("Likely causes are not stated unless documented in sources: Further investigation required.")
    else:
        items = [p for p in projects if _in_years(_approval(p), pq)]
        for p in items[:200]:
            positions = [agreement_position(db, a) for a in p.agreements if not donor_ids or a.partner_id in donor_ids]
            ans.facts.append({
                "ap2i_id": p.ap2i_id, "title": p.title, "sector": p.sector.name_en if p.sector else None,
                "approval_date": _approval(p).isoformat() if _approval(p) else None, "status": p.status,
                "financing": [{"partner": pos.partner, "id": pos.source_identifier, "committed": str(pos.committed) if pos.committed is not None else None,
                               "currency": pos.currency} for pos in positions],
            })
            ans.citations.append(_cite(p))
        undated = sum(1 for p in projects if _approval(p) is None)
        ans.calculations.append({"name": "matching_projects", "value": len(items)})
        if (pq.year_from or pq.year_to) and undated:
            ans.missing_information.append(f"{undated} project(s) have no approval date and could not be placed in the period.")
        if len(items) > 200:
            ans.missing_information.append("Only the first 200 projects are listed; use the Data Explorer for the full list.")

    _maybe_narrate(ans)
    return ans


# --- optional LLM narrative --------------------------------------------------------------------

NUM_RX = re.compile(r"\d[\d,.\s]*\d|\d")


def _numbers(text: str) -> set[str]:
    return {re.sub(r"[,\s]", "", m.group(0)).rstrip(".") for m in NUM_RX.finditer(text)}


def grounding_check(narrative: str, facts_blob: str) -> dict:
    allowed = _numbers(facts_blob)
    found = _numbers(narrative)
    unsupported = sorted(n for n in found if n not in allowed and not any(n in a for a in allowed))
    return {"numbers_in_narrative": len(found), "unsupported_numbers": unsupported, "passed": not unsupported}


class LLMProvider:
    def complete(self, system: str, user: str) -> str:  # pragma: no cover - interface
        raise NotImplementedError


class AnthropicProvider(LLMProvider):
    def __init__(self, api_key: str, model: str, base_url: str | None = None):
        self.api_key, self.model, self.base_url = api_key, model, base_url or "https://api.anthropic.com"

    def complete(self, system: str, user: str) -> str:
        r = httpx.post(f"{self.base_url}/v1/messages", timeout=60, headers={
            "x-api-key": self.api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
            json={"model": self.model, "max_tokens": 600, "system": system, "messages": [{"role": "user", "content": user}]})
        r.raise_for_status()
        return "".join(b.get("text", "") for b in r.json().get("content", []))


class OpenAICompatibleProvider(LLMProvider):
    def __init__(self, api_key: str, model: str, base_url: str):
        self.api_key, self.model, self.base_url = api_key, model, base_url

    def complete(self, system: str, user: str) -> str:
        r = httpx.post(f"{self.base_url.rstrip('/')}/chat/completions", timeout=60,
                       headers={"Authorization": f"Bearer {self.api_key}"},
                       json={"model": self.model, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]})
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]


_test_provider: LLMProvider | None = None


def set_provider_for_tests(p: LLMProvider | None) -> None:
    global _test_provider
    _test_provider = p


def get_provider() -> tuple[str, LLMProvider | None]:
    if _test_provider is not None:
        return "test", _test_provider
    s = get_settings()
    if s.llm_provider == "anthropic" and s.llm_api_key and s.llm_model:
        return "anthropic", AnthropicProvider(s.llm_api_key, s.llm_model, s.llm_base_url)
    if s.llm_provider == "openai_compatible" and s.llm_api_key and s.llm_model and s.llm_base_url:
        return "openai_compatible", OpenAICompatibleProvider(s.llm_api_key, s.llm_model, s.llm_base_url)
    return "none", None


def _maybe_narrate(ans: Answer) -> None:
    name, provider = get_provider()
    ans.provider = name
    if provider is None or not ans.facts:
        return
    facts_blob = json.dumps({"facts": ans.facts[:60], "calculations": ans.calculations, "missing": ans.missing_information},
                            ensure_ascii=False, default=str)
    titles = "\n".join(wrap_untrusted(f["ap2i_id"], f.get("title") or "") for f in ans.facts[:30] if f.get("ap2i_id"))
    user = (f"QUESTION:\n{wrap_untrusted('user_question', ans.question, 1000)}\n\nFACTS (authoritative, from the AP²I database):\n"
            f"{facts_blob}\n\nPROJECT TITLES (quoted source text):\n{titles}\n\nWrite at most 120 words summarising the facts. "
            "Use only numbers present in FACTS.")
    try:
        text = provider.complete(SYSTEM_GUARD, user)
    except Exception as exc:  # noqa: BLE001 — the structured answer stands without a narrative
        ans.grounding = {"passed": False, "error": f"provider error: {type(exc).__name__}"}
        return
    check = grounding_check(text, facts_blob)
    ans.grounding = check
    if check["passed"]:
        ans.narrative = text.strip()
