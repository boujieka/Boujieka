import {
  type CountryCode, type CurrencyCode, type FxRate, type TransferOrder, convertFloor, crossRate, flowKey, minBig,
} from '@diasposwap/shared-types';

/**
 * Level 4 - multilateral compensation, SIMULATION ONLY.
 *
 * Corridors form a directed weighted graph: node = country, edge u->v weight = EUR-cent value of
 * pending orders sending from u to v. A cycle u1->u2->...->u1 can be netted by its bottleneck:
 * money collected in each country pays beneficiaries in the same country, so no value crosses a border.
 *
 * Production use is refused: multilateral netting needs legal, operational and regulatory validation.
 */
export interface FlowEdge { from: CountryCode; to: CountryCode; eurCents: bigint }

export interface CycleProposal {
  path: CountryCode[]; // closed: first === last
  eurCents: bigint;
}

export interface MultilateralResult {
  simulationOnly: true;
  edgesBefore: FlowEdge[];
  edgesAfter: FlowEdge[];
  bilateral: CycleProposal[];
  cycles: CycleProposal[];
  grossBefore: bigint;
  grossAfterBilateral: bigint;
  grossAfterMultilateral: bigint;
}

export class ProductionRefused extends Error {}

export function buildFlowGraph(orders: readonly TransferOrder[], rates: Record<CurrencyCode, FxRate>): Map<string, FlowEdge> {
  const g = new Map<string, FlowEdge>();
  for (const o of orders) {
    if (o.remaining <= 0n || o.compliance !== 'CLEARED') continue;
    const k = flowKey(o.fromCountry, o.toCountry);
    const e = g.get(k) ?? { from: o.fromCountry, to: o.toCountry, eurCents: 0n };
    e.eurCents += convertFloor(o.remaining, crossRate(o.sendCurrency, 'EUR', rates));
    g.set(k, e);
  }
  return g;
}

const gross = (g: Map<string, FlowEdge>) => [...g.values()].reduce((s, e) => s + e.eurCents, 0n);

/** All simple cycles of length 3..maxLen, deterministic order. Graph is small (<= ~15 countries). */
function simpleCycles(g: Map<string, FlowEdge>, maxLen: number): CountryCode[][] {
  const nodes = [...new Set([...g.values()].flatMap((e) => [e.from, e.to]))].sort();
  const adj = new Map<CountryCode, CountryCode[]>();
  for (const e of g.values()) if (e.eurCents > 0n) adj.set(e.from, [...(adj.get(e.from) ?? []), e.to].sort());
  const out: CountryCode[][] = [];
  for (const start of nodes) {
    const dfs = (path: CountryCode[]) => {
      const last = path[path.length - 1] as CountryCode;
      for (const nxt of adj.get(last) ?? []) {
        if (nxt === start && path.length >= 3) out.push([...path, start]);
        // canonical form: start is the smallest node of the cycle
        else if (!path.includes(nxt) && nxt > start && path.length < maxLen) dfs([...path, nxt]);
      }
    };
    dfs([start]);
  }
  return out;
}

export function simulateMultilateral(
  orders: readonly TransferOrder[],
  rates: Record<CurrencyCode, FxRate>,
  opts: { mode: 'simulation' | 'production'; maxCycleLength?: number } = { mode: 'simulation' },
): MultilateralResult {
  if (opts.mode !== 'simulation') {
    throw new ProductionRefused('Multilateral netting is disabled outside simulation pending legal/regulatory validation');
  }
  const g = buildFlowGraph(orders, rates);
  const edgesBefore = [...g.values()].map((e) => ({ ...e }));
  const grossBefore = gross(g);

  // 1) bilateral netting
  const bilateral: CycleProposal[] = [];
  for (const k of [...g.keys()].sort()) {
    const e = g.get(k);
    if (!e) continue;
    const back = g.get(flowKey(e.to, e.from));
    if (!back || e.from > e.to) continue;
    const m = minBig(e.eurCents, back.eurCents);
    if (m > 0n) {
      e.eurCents -= m;
      back.eurCents -= m;
      bilateral.push({ path: [e.from, e.to, e.from], eurCents: m });
    }
  }
  const grossAfterBilateral = gross(g);

  // 2) greedy cycle cancelling: repeatedly net the cycle with the largest bottleneck
  const cycles: CycleProposal[] = [];
  const maxLen = opts.maxCycleLength ?? 4;
  for (let guard = 0; guard < 1000; guard++) {
    let best: CycleProposal | null = null;
    for (const c of simpleCycles(g, maxLen)) {
      let bottleneck: bigint | null = null;
      for (let i = 0; i < c.length - 1; i++) {
        const w = g.get(flowKey(c[i] as CountryCode, c[i + 1] as CountryCode))?.eurCents ?? 0n;
        bottleneck = bottleneck === null ? w : minBig(bottleneck, w);
      }
      if (bottleneck && bottleneck > 0n && (!best || bottleneck > best.eurCents)) best = { path: c, eurCents: bottleneck };
    }
    if (!best) break;
    for (let i = 0; i < best.path.length - 1; i++) {
      const e = g.get(flowKey(best.path[i] as CountryCode, best.path[i + 1] as CountryCode));
      if (e) e.eurCents -= best.eurCents;
    }
    cycles.push(best);
  }

  return {
    simulationOnly: true,
    edgesBefore,
    edgesAfter: [...g.values()].map((e) => ({ ...e })),
    bilateral,
    cycles,
    grossBefore,
    grossAfterBilateral,
    grossAfterMultilateral: gross(g),
  };
}
