"""IATI connector family (Master prompt §12) and IATI-published donor connectors (§10, §11, Tier 2/3).

Access methods (verified 2026-10-22):
  * Official IATI Datastore API (https://api.iatistandard.org/datastore) — requires a free
    subscription key (header Ocp-Apim-Subscription-Key). Used when AP2I_IATI_API_KEY is set.
    Not exercised in this build because no key was available (reported as a blocker).
  * Code for IATI Datastore (https://datastore.codeforiati.org/api/1/access/activity.xml) — a
    community-run public mirror of the same IATI publications, no key needed. It returns the
    activities' original IATI XML, which is what AP²I stores as the source record.
Data licence: each publisher states its own licence in the IATI Registry (most use open licences
such as CC BY / ODbL / Etalab). Attribution = the reporting organisation, kept on every record.

Semantics that matter:
  * An IATI activity is NOT necessarily one project. AFD (FR-3) publishes a parent activity
    (hierarchy 1, no transactions) per project and child activities (hierarchy 2) per financing.
    Children carry `related-activity type="1"` pointing at the parent. AP²I creates one master
    project per parent and one financing agreement per child — so nothing is counted twice.
  * World Bank IATI activities (44000-Pxxxxxx) designate the same operations as the World Bank
    Projects API (Pxxxxxx): deterministic equivalence, never a second project.
  * Transaction types used: 2 = outgoing commitment (negative = de-commitment/cancellation),
    3 = disbursement, 4 = expenditure. 5/6 (interest/loan repayment), 1/11 (incoming) and budgets
    are kept as provenance only. Budgets are plans, never flows.
  * Multi-country activities: transactions are attributed to a country only when the transaction
    itself names the country or the activity has a single recipient country. No pro-rating.
"""

from __future__ import annotations

import hashlib
from collections.abc import Iterator
from decimal import Decimal

from lxml import etree

from app.connectors.base import (
    Connector,
    Money,
    NormalizedAgreement,
    NormalizedRecord,
    RawRecord,
    SyncParams,
    parse_date,
    parse_decimal,
)
from app.reference.catalog import (
    DAC3_TO_SECTOR,
    DAC5_TO_SECTOR,
    DONORS,
    IATI_FINANCE_TYPE_TO_INSTRUMENT,
)
from app.reference.countries import BY_ISO2, BY_ISO3

XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"

STATUS_MAP = {"1": "pipeline", "2": "active", "3": "completed", "4": "closed", "5": "cancelled", "6": "suspended"}
STATUS_LABEL = {"1": "Pipeline/identification", "2": "Implementation", "3": "Finalisation", "4": "Closed",
                "5": "Cancelled", "6": "Suspended"}
TX_TYPES = {"1": "Incoming Funds", "2": "Outgoing Commitment", "3": "Disbursement", "4": "Expenditure",
            "5": "Interest Payment", "6": "Loan Repayment", "7": "Reimbursement", "8": "Purchase of Equity",
            "9": "Sale of Equity", "10": "Credit Guarantee", "11": "Incoming Commitment",
            "12": "Outgoing Pledge", "13": "Incoming Pledge"}
DOC_CATEGORY = {"A01": "Pre- and post-project impact appraisal", "A02": "Objectives / Purpose of activity",
                "A07": "Review of project performance and evaluation", "A08": "Results, outcomes and outputs",
                "A09": "Memorandum of understanding", "A12": "Activity web page", "B05": "Annual report"}

REF_TO_PARTNER: dict[str, str] = {ref: d["code"] for d in DONORS for ref in d["iati_org_refs"]}


def _narratives(el) -> list[tuple[str, str | None]]:
    if el is None:
        return []
    out = []
    for n in el.findall("narrative"):
        text = (n.text or "").strip()
        if text:
            out.append((text, n.get(XML_LANG)))
    return out


def _pick(narr: list[tuple[str, str | None]], default_lang: str | None) -> tuple[str | None, str | None]:
    if not narr:
        return None, None
    text, lang = narr[0]
    return text, lang or default_lang


class IATIConnector(Connector):
    key = "iati_generic"
    name = "IATI — all publishers (Code for IATI datastore mirror)"
    partner_code = "IATI"
    tier = 1
    access_method = "public_xml_api (IATI Standard 2.0x)"
    base_url = "https://datastore.codeforiati.org/api/1/access/activity.xml"
    documentation_url = "https://iatistandard.org/en/iati-tools-and-resources/iati-datastore/"
    usage_terms = "Licence set per publisher in the IATI Registry; attribution to the reporting organisation."
    update_frequency = "Varies by publisher (monthly to quarterly is common); mirror refreshed daily"
    default_schedule = "30 2 * * *"
    page_size = 100
    reporting_orgs: tuple[str, ...] = ()  # empty = all publishers

    def _orgs(self) -> list[str | None]:
        orgs = self.config.get("reporting_orgs") or list(self.reporting_orgs)
        return orgs or [None]

    def fetch(self, params: SyncParams) -> Iterator[RawRecord]:
        if self.settings.iati_api_key and self.config.get("use_official_api", True):
            yield from self._fetch_official(params)
            return
        url = self.config.get("base_url") or (self.settings.iati_datastore_url.rstrip("/") + "/activity.xml")
        retrieved = 0
        for iso3 in params.countries:
            ref = BY_ISO3.get(iso3)
            if ref is None:
                continue
            for org in self._orgs():
                offset = 0
                while True:
                    q = {"recipient-country": ref.iso2, "limit": self.page_size, "offset": offset}
                    if org:
                        q["reporting-org"] = org
                    resp = self.get(url, params=q)
                    root = etree.fromstring(resp.content)
                    acts = root.findall(".//iati-activity")
                    total = int(root.findtext(".//query/total-count") or 0)
                    for a in acts:
                        rec = self._raw_from_xml(a, iso3, resp.url)
                        if rec is None:
                            continue
                        yield rec
                        retrieved += 1
                        if params.limit and retrieved >= params.limit:
                            return
                    offset += self.page_size
                    if not acts or offset >= total:
                        break

    def _fetch_official(self, params: SyncParams) -> Iterator[RawRecord]:
        """Official IATI Datastore (Solr). Requires AP2I_IATI_API_KEY. Not exercised without a key."""
        url = self.settings.iati_official_api_url.rstrip("/") + "/activity/select"
        headers = {"Ocp-Apim-Subscription-Key": self.settings.iati_api_key or ""}
        retrieved = 0
        for iso3 in params.countries:
            ref = BY_ISO3.get(iso3)
            if ref is None:
                continue
            for org in self._orgs():
                q = f"recipient_country_code:{ref.iso2}"
                if org:
                    q += f' AND reporting_org_ref:"{org}"'
                start = 0
                while True:
                    resp = self.client.get(url, params={"q": q, "fl": "iati_identifier,iati_xml", "rows": self.page_size,
                                                        "start": start, "wt": "json"}, headers=headers)
                    resp.raise_for_status()
                    body = resp.json()["response"]
                    for doc in body.get("docs", []):
                        a = etree.fromstring(doc["iati_xml"].encode("utf-8"))
                        rec = self._raw_from_xml(a, iso3, str(resp.url))
                        if rec:
                            yield rec
                            retrieved += 1
                            if params.limit and retrieved >= params.limit:
                                return
                    start += self.page_size
                    if start >= body.get("numFound", 0):
                        break

    def _raw_from_xml(self, a, iso3: str, query_url) -> RawRecord | None:
        ident = (a.findtext("iati-identifier") or "").strip()
        if not ident:
            return None
        xml = etree.tostring(a, encoding="unicode")
        reporting = a.find("reporting-org")
        return RawRecord(
            source_identifier=ident,
            record_type="iati_activity",
            country_iso3=iso3,
            payload={
                "iati_identifier": ident,
                "reporting_org_ref": reporting.get("ref") if reporting is not None else None,
                "hierarchy": a.get("hierarchy"),
                "query_url": str(query_url),
            },
            raw_text=xml,
            payload_format="xml",
            source_url=f"https://d-portal.org/ctrack.html#view=act&aid={ident}",
            source_last_updated=a.get("last-updated-datetime"),
        )

    # -- normalization -------------------------------------------------------------------------
    def normalize(self, raw: RawRecord) -> NormalizedRecord | None:
        a = etree.fromstring(raw.raw_text.encode("utf-8"))
        ident = raw.source_identifier
        default_lang = a.get(XML_LANG)
        default_currency = a.get("default-currency")
        reporting = a.find("reporting-org")
        reporting_ref = reporting.get("ref") if reporting is not None else None
        reporting_name, _ = _pick(_narratives(reporting), default_lang)
        partner_code = REF_TO_PARTNER.get(reporting_ref or "", f"IATI:{reporting_ref}" if reporting_ref else "IATI:unknown")
        warnings: list[str] = []

        titles = _narratives(a.find("title"))
        title, title_lang = _pick(titles, default_lang)
        if not title:
            title = ident
            warnings.append("Activity has no title; identifier used as title")
        alt_titles = [(t, lg or default_lang) for t, lg in titles[1:]]

        desc = {d.get("type") or "1": _pick(_narratives(d), default_lang)[0] for d in a.findall("description")}

        status_code = a.find("activity-status").get("code") if a.find("activity-status") is not None else None
        dates = {d.get("type"): parse_date(d.get("iso-date")) for d in a.findall("activity-date")}

        # Sector: highest percentage among DAC vocabularies (1 = 5-digit, 2 = 3-digit).
        sector_code = None
        sector_label = None
        best = Decimal("-1")
        for s in a.findall("sector"):
            vocab = s.get("vocabulary") or "1"
            if vocab not in ("1", "2"):
                continue
            pct = parse_decimal(s.get("percentage")) or Decimal("100")
            if pct > best:
                code = s.get("code") or ""
                mapped = DAC5_TO_SECTOR.get(code) or DAC3_TO_SECTOR.get(code[:3])
                if mapped:
                    best = pct
                    sector_code = mapped
                    sector_label = f"DAC {code}: {_pick(_narratives(s), default_lang)[0] or ''}".strip()

        orgs = []
        implementing = []
        accountable = []
        for po in a.findall("participating-org"):
            name, _ = _pick(_narratives(po), default_lang)
            orgs.append({"role": po.get("role"), "ref": po.get("ref"), "name": name, "type": po.get("type")})
            if po.get("role") == "4" and name:
                implementing.append(name)
            if po.get("role") == "2" and name:
                accountable.append(name)

        recipient_countries = [rc.get("code") for rc in a.findall("recipient-country")]
        multi_country = len(recipient_countries) > 1 or bool(a.findall("recipient-region"))
        if multi_country:
            warnings.append(
                f"Multi-country/regional activity ({', '.join(recipient_countries)}); only transactions that name "
                "this country are attributed to it"
            )

        iso2 = BY_ISO3[raw.country_iso3].iso2 if raw.country_iso3 in BY_ISO3 else None
        finance_type = a.find("default-finance-type")
        instrument_code = IATI_FINANCE_TYPE_TO_INSTRUMENT.get(finance_type.get("code")) if finance_type is not None else None

        commitments: list[Money] = []
        flows: list[Money] = []
        skipped_multi = 0
        for idx, tx in enumerate(a.findall("transaction")):
            ttype_el = tx.find("transaction-type")
            ttype = ttype_el.get("code") if ttype_el is not None else None
            val_el = tx.find("value")
            if val_el is None or ttype not in ("2", "3", "4"):
                continue
            amount = parse_decimal(val_el.text)
            currency = val_el.get("currency") or default_currency
            if amount is None or not currency:
                warnings.append(f"Transaction {idx} ignored: missing value or currency")
                continue
            if multi_country:
                tx_country = tx.find("recipient-country")
                if tx_country is None or tx_country.get("code") != iso2:
                    skipped_multi += 1
                    continue
            vdate = parse_date(val_el.get("value-date")) or parse_date(
                tx.find("transaction-date").get("iso-date") if tx.find("transaction-date") is not None else None)
            key = hashlib.sha256(etree.tostring(tx)).hexdigest()[:24]
            tkey = f"{ident}:tx{idx}:{key}"
            if ttype == "2":
                kind = "cancellation" if amount < 0 else "original"
                commitments.append(Money(amount, currency.upper(), vdate, tkey, kind, f"IATI transaction type 2 ({TX_TYPES['2']})"))
            elif ttype == "3":
                flows.append(Money(amount, currency.upper(), vdate, tkey, "disbursement", f"IATI transaction type 3 ({TX_TYPES['3']})"))
            else:
                flows.append(Money(amount, currency.upper(), vdate, tkey, "expenditure", f"IATI transaction type 4 ({TX_TYPES['4']})"))
            ft = tx.find("finance-type")
            if ft is not None and instrument_code is None:
                instrument_code = IATI_FINANCE_TYPE_TO_INSTRUMENT.get(ft.get("code"))
        if skipped_multi:
            warnings.append(f"{skipped_multi} transaction(s) not attributed (multi-country, no country on transaction)")

        # Positive commitments after the first one are "additional"; the earliest is the original.
        positives = sorted([c for c in commitments if c.amount > 0], key=lambda c: (c.value_date is None, c.value_date))
        for c in positives[1:]:
            c.kind = "additional"
        amount_original = positives[0].amount if positives else None
        agr_currency = positives[0].currency if positives else (default_currency.upper() if default_currency else None)

        related = [(r.get("type"), r.get("ref")) for r in a.findall("related-activity")]
        parent = next((ref for t, ref in related if t == "1" and ref), None)
        has_children = any(t == "2" for t, _ in related)
        has_tx = bool(commitments or flows)

        agreements: list[NormalizedAgreement] = []
        if has_tx or not has_children:
            agreements.append(NormalizedAgreement(
                partner_code=partner_code,
                source_identifier=ident,
                name=title,
                instrument_code=instrument_code,
                instrument_label=(f"IATI finance type {finance_type.get('code')}" if finance_type is not None else None),
                approval_date=dates.get("1") if not commitments else (positives[0].value_date if positives else None),
                signature_date=None,
                closing_date_original=dates.get("3"),
                closing_date_current=dates.get("4") or dates.get("3"),
                status=STATUS_MAP.get(status_code or "", "unknown"),
                currency=agr_currency,
                amount_original=amount_original,
                amount_label="Earliest IATI outgoing commitment (transaction type 2)" if amount_original is not None else None,
                commitments=commitments,
                flows=flows,
            ))

        equivalent = []
        if ident.startswith("44000-"):
            equivalent.append(ident.split("-", 1)[1])  # World Bank P-number
        for oi in a.findall("other-identifier"):
            if oi.get("type") == "A1" and oi.get("ref"):
                equivalent.append(oi.get("ref"))

        rec = NormalizedRecord(
            country_iso3=raw.country_iso3 or "",
            title=title,
            title_language=title_lang,
            alt_titles=alt_titles,
            description=desc.get("1"),
            objectives=desc.get("2"),
            sector_code=sector_code,
            sector_label=sector_label,
            status=STATUS_MAP.get(status_code or "", "unknown"),
            status_label=f"IATI {status_code}: {STATUS_LABEL.get(status_code or '', 'unknown')}" if status_code else None,
            executing_agency="; ".join(accountable) or None,
            implementing_agency="; ".join(implementing) or None,
            approval_date=None,
            start_date=dates.get("2") or dates.get("1"),
            planned_end_date=dates.get("3"),
            actual_end_date=dates.get("4"),
            agreements=agreements,
            participating_orgs=orgs,
            equivalent_identifiers=equivalent,
            parent_identifier=parent,
            warnings=warnings,
        )
        rec.observations.append(("reporting_org", "reporting-org", f"{reporting_ref} {reporting_name or ''}".strip()))
        if desc.get("3"):
            rec.observations.append(("target_groups", "description[@type=3]", desc["3"]))
        if dates.get("1"):
            rec.observations.append(("planned_start_date", "activity-date[@type=1]", dates["1"]))

        for dl in a.findall("document-link"):
            url = dl.get("url")
            if not url:
                continue
            cat = dl.find("category")
            lang = dl.find("language")
            dd = dl.find("document-date")
            rec.documents.append({
                "title": _pick(_narratives(dl.find("title")), default_lang)[0] or "IATI document",
                "url": url,
                "doc_type": DOC_CATEGORY.get(cat.get("code") if cat is not None else "", cat.get("code") if cat is not None else None),
                "language": lang.get("code") if lang is not None else None,
                "date": parse_date(dd.get("iso-date")) if dd is not None else None,
            })
        for loc in a.findall("location"):
            pos = loc.findtext("point/pos")
            lat = lon = None
            if pos:
                parts = pos.split()
                if len(parts) == 2:
                    lat, lon = parse_decimal(parts[0]), parse_decimal(parts[1])
            name = _pick(_narratives(loc.find("name")), default_lang)[0]
            if name or lat is not None:
                exact = loc.find("exactness")
                rec.locations.append({"name": name, "lat": lat, "lon": lon,
                                      "precision": f"IATI exactness {exact.get('code')}" if exact is not None else None})
        for res in a.findall("result"):
            rtitle = _pick(_narratives(res.find("title")), default_lang)[0]
            for ind in res.findall("indicator"):
                ititle = _pick(_narratives(ind.find("title")), default_lang)[0] or rtitle
                base = ind.find("baseline")
                periods = ind.findall("period")
                target = None
                actual = None
                actual_period = None
                for per in periods:
                    t = per.find("target")
                    ac = per.find("actual")
                    if t is not None and t.get("value"):
                        target = parse_decimal(t.get("value"))
                    if ac is not None and ac.get("value"):
                        actual = parse_decimal(ac.get("value"))
                        pe = per.find("period-end")
                        actual_period = parse_date(pe.get("iso-date")) if pe is not None else None
                rec.results.append({
                    "title": ititle,
                    "measure": ind.get("measure"),
                    "baseline": parse_decimal(base.get("value")) if base is not None else None,
                    "baseline_year": base.get("year") if base is not None else None,
                    "target": target,
                    "actual": actual,
                    "actual_date": actual_period,
                })
        return rec


def _donor(code: str) -> dict:
    return next(d for d in DONORS if d["code"] == code)


def make_iati_donor_connector(code: str, key: str, name: str, tier: int, docs: str | None = None):
    """Build a donor-specific connector that reads only that donor's own IATI publication."""
    refs = tuple(_donor(code)["iati_org_refs"])

    cls = type(
        f"IATI_{code}_Connector",
        (IATIConnector,),
        {
            "key": key,
            "name": name,
            "partner_code": code,
            "tier": tier,
            "reporting_orgs": refs,
            "documentation_url": docs or IATIConnector.documentation_url,
        },
    )
    return cls


AfDBIATIConnector = make_iati_donor_connector(
    "AFDB", "afdb_iati", "African Development Bank — IATI publication (XM-DAC-46002)", 1,
    "https://www.afdb.org/en/projects-and-operations",
)
AFDIATIConnector = make_iati_donor_connector(
    "AFD", "afd_iati", "Agence Française de Développement — IATI publication (FR-3)", 1,
    "https://opendata.afd.fr",
)
WorldBankIATIConnector = make_iati_donor_connector(
    "WB", "worldbank_iati", "World Bank — IATI publication (44000): transactions", 1,
    "https://iatiregistry.org/publisher/worldbank",
)
TIER2_3_IATI = [
    make_iati_donor_connector("EIB", "eib_iati", "European Investment Bank — IATI publication (XM-DAC-918-3)", 2),
    make_iati_donor_connector("EU", "eu_intpa_iati", "European Union DG INTPA — IATI publication (XI-IATI-EC_INTPA)", 2),
    make_iati_donor_connector("IFAD", "ifad_iati", "IFAD — IATI publication (XM-DAC-41108)", 3),
    make_iati_donor_connector("UNDP", "undp_iati", "UNDP — IATI publication (XM-DAC-41114)", 3),
    make_iati_donor_connector("UNICEF", "unicef_iati", "UNICEF — IATI publication (XM-DAC-41122)", 3),
    make_iati_donor_connector("FAO", "fao_iati", "FAO — IATI publication (XM-DAC-41301)", 3),
    make_iati_donor_connector("UNIDO", "unido_iati", "UNIDO — IATI publication (XM-DAC-41123)", 3),
    make_iati_donor_connector("BMZ", "bmz_iati", "German BMZ — IATI publication (DE-1)", 3),
]

__all__ = ["IATIConnector", "AfDBIATIConnector", "AFDIATIConnector", "WorldBankIATIConnector", "TIER2_3_IATI", "BY_ISO2"]
