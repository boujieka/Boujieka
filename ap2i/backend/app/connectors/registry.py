"""Connector registry: every connector is a plugin registered by key.

Adding a donor = add a DONORS row (app.reference.catalog) + register a connector class here.
Connectors without an implementation are still listed so that coverage gaps are visible.
"""

from __future__ import annotations

from collections.abc import Iterator

from app.connectors.base import Connector, ConnectorError, NormalizedRecord, RawRecord, SyncParams
from app.connectors.iati import (
    TIER2_3_IATI,
    AFDIATIConnector,
    AfDBIATIConnector,
    IATIConnector,
    WorldBankIATIConnector,
)
from app.connectors.manual import ManualUploadConnector
from app.connectors.worldbank import WorldBankProjectsConnector


class _NotImplemented(Connector):
    implemented = False
    access_method = "not_available"
    default_schedule = None

    def fetch(self, params: SyncParams) -> Iterator[RawRecord]:
        raise ConnectorError(f"{self.key}: no automated access implemented — {self.usage_terms}")

    def normalize(self, raw: RawRecord) -> NormalizedRecord | None:  # pragma: no cover
        return None


def _placeholder(key: str, name: str, partner: str, tier: int, reason: str, base_url: str | None = None):
    return type(f"Placeholder_{key}", (_NotImplemented,), {
        "key": key, "name": name, "partner_code": partner, "tier": tier, "usage_terms": reason, "base_url": base_url,
    })


AfDBPortalProbe = _placeholder(
    "afdb_portal", "African Development Bank — Projects portal / MapAfrica (direct)", "AFDB", 1,
    "projectsportal.afdb.org was unreachable from the AP²I environment on 2026-10-22 (proxy CONNECT 502) and no "
    "documented public API was identified. AfDB project data is ingested through AfDB's own IATI publication "
    "(connector afdb_iati); the portal remains a documented manual-import source.",
    "https://projectsportal.afdb.org",
)
AFDOpenDataProbe = _placeholder(
    "afd_opendata", "AFD — opendata.afd.fr (direct, Opendatasoft)", "AFD", 1,
    "opendata.afd.fr reset the connection from the AP²I environment on 2026-10-22 and afd.fr was in maintenance "
    "(HTTP 503). AFD project data is ingested through AFD's own IATI publication (connector afd_iati).",
    "https://opendata.afd.fr",
)
NO_CONNECTOR = [
    _placeholder("isdb", "Islamic Development Bank", "ISDB", 2,
                 "No IsDB IATI publication observed for Cameroon; official project pages need a source-specific connector."),
    _placeholder("kfw", "KfW Development Bank", "KFW", 2,
                 "KfW is not a separate IATI reporting organisation for Cameroon (German flows appear under DE-1/BMZ)."),
    _placeholder("jica", "JICA", "JICA", 2, "No JICA IATI publication observed for Cameroon; manual import workflow."),
    _placeholder("gef", "Global Environment Facility", "GEF", 2,
                 "GEF project database not yet assessed; GEF-funded UNDP activities appear in undp_iati."),
    _placeholder("gcf", "Green Climate Fund", "GCF", 2, "GCF open data not yet assessed; manual import workflow."),
    _placeholder("badea", "BADEA", "BADEA", 3, "No machine-readable source identified; manual import workflow."),
    _placeholder("sfd", "Saudi Fund for Development", "SFD", 3, "No machine-readable source identified; manual import workflow."),
    _placeholder("kfaed", "Kuwait Fund", "KFAED", 3, "No machine-readable source identified; manual import workflow."),
    _placeholder("adfd", "Abu Dhabi Fund for Development", "ADFD", 3, "No machine-readable source identified; manual import workflow."),
]

CONNECTORS: dict[str, type[Connector]] = {}
for _cls in [WorldBankProjectsConnector, WorldBankIATIConnector, AfDBIATIConnector, AFDIATIConnector,
             IATIConnector, *TIER2_3_IATI, ManualUploadConnector, AfDBPortalProbe, AFDOpenDataProbe, *NO_CONNECTOR]:
    CONNECTORS[_cls.key] = _cls

# Connectors enabled by default for the initial Cameroon deployment (Tier 1).
DEFAULT_ENABLED = {"worldbank_projects", "worldbank_iati", "afdb_iati", "afd_iati"}


def get_connector(key: str, config: dict | None = None) -> Connector:
    try:
        return CONNECTORS[key](config=config)
    except KeyError as exc:
        raise ConnectorError(f"Unknown connector {key}") from exc
