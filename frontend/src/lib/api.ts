import "server-only";

import type {
  Auction,
  AuctionDetail,
  CountryDetail,
  Country,
  DashboardSummary,
  DataQualityReport,
  HeatGrid,
  MaturityWall,
  OpportunityPage,
  Page,
  SecurityDetail,
  SourceOut,
  YieldCurve,
} from "./types";

// Server-side only: the browser never talks to the API directly and never sees credentials.
const BASE = process.env.ABI_API_URL ?? "http://localhost:8000/api/v1";

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
  }
}

type Params = Record<string, string | number | boolean | string[] | undefined | null>;

function query(params: Params = {}): string {
  const qs = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value === undefined || value === null || value === "") continue;
    if (Array.isArray(value)) value.forEach((v) => qs.append(key, v));
    else qs.append(key, String(value));
  }
  const s = qs.toString();
  return s ? `?${s}` : "";
}

async function get<T>(path: string, params?: Params): Promise<T> {
  const res = await fetch(`${BASE}${path}${query(params)}`, { cache: "no-store" });
  if (!res.ok) throw new ApiError(res.status, `${res.status} ${res.statusText} for ${path}`);
  return res.json() as Promise<T>;
}

export const api = {
  summary: (asOf?: string) => get<DashboardSummary>("/dashboard/summary", { as_of: asOf }),
  auctions: (params: Params) => get<Page<Auction>>("/auctions", params),
  auction: (id: number) => get<AuctionDetail>(`/auctions/${id}`),
  countries: () => get<Country[]>("/countries"),
  country: (iso3: string) => get<CountryDetail>(`/countries/${iso3}`),
  yieldCurve: (iso3: string) => get<YieldCurve>(`/countries/${iso3}/yield-curve`),
  security: (id: number) => get<SecurityDetail>(`/securities/${id}`),
  sources: () => get<SourceOut[]>("/sources"),
  dataQuality: () => get<DataQualityReport>("/data-quality"),
  opportunities: (params: Params) => get<OpportunityPage>("/opportunities", params),
  heatGrid: () => get<HeatGrid>("/market/heat-grid"),
  maturityWall: (iso3: string) => get<MaturityWall>(`/countries/${iso3}/maturity-wall`),
};
