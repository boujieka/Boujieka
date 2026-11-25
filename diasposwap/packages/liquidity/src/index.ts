import {
  type CorridorConfig, type CurrencyCode, type FxRate, type TransferOrder,
  INITIAL_CORRIDORS, convertFloor, crossRate, divFloor,
} from '@diasposwap/shared-types';

/**
 * SwapLiquidity - deterministic corridor imbalance analytics. All outputs are ESTIMATES.
 * No machine learning: simple counting statistics until enough reliable data exists.
 */
export interface CorridorLiquidity {
  corridorId: string;
  /** Pending value a->b and b->a, EUR cents. */
  pendingAB: bigint;
  pendingBA: bigint;
  /** Value that bilateral matching can compensate right now. */
  matchable: bigint;
  /** |pendingAB - pendingBA|: what would need prefunding to clear everything now. */
  prefundingNeed: bigint;
  dominantDirection: string | null;
  /** 0..10000 basis points: 0 = perfectly balanced, 10000 = one-way. */
  imbalanceBps: number;
  /** Observed opposite-direction arrival rate (EUR cents/day) over the window, per direction. */
  inflowPerDayAB: bigint;
  inflowPerDayBA: bigint;
  /** Estimated days for the dominant side's excess to be absorbed by opposite inflow; null if no inflow. */
  estimatedClearDays: number | null;
  /** Qualitative uncertainty: few observations -> HIGH. */
  uncertainty: 'LOW' | 'MEDIUM' | 'HIGH';
  structurallyImbalanced: boolean;
  observations: number;
}

export interface LiquidityInput {
  orders: readonly TransferOrder[];
  rates: Record<CurrencyCode, FxRate>;
  now: Date;
  windowDays?: number;
  corridors?: readonly CorridorConfig[];
}

export function analyseLiquidity(input: LiquidityInput): CorridorLiquidity[] {
  const windowDays = input.windowDays ?? 30;
  const since = input.now.getTime() - windowDays * 86400_000;
  const eur = (o: TransferOrder, amt: bigint) => convertFloor(amt, crossRate(o.sendCurrency, 'EUR', input.rates));
  return (input.corridors ?? INITIAL_CORRIDORS).map((c) => {
    let pendingAB = 0n, pendingBA = 0n, flowAB = 0n, flowBA = 0n, obs = 0;
    for (const o of input.orders) {
      const ab = o.fromCountry === c.a && o.toCountry === c.b;
      const ba = o.fromCountry === c.b && o.toCountry === c.a;
      if (!ab && !ba) continue;
      if ((o.state === 'QUEUED' || o.state === 'PARTIALLY_MATCHED') && o.remaining > 0n) {
        if (ab) pendingAB += eur(o, o.remaining); else pendingBA += eur(o, o.remaining);
      }
      if (Date.parse(o.createdAt) >= since) {
        obs++;
        if (ab) flowAB += eur(o, o.principal); else flowBA += eur(o, o.principal);
      }
    }
    const matchable = pendingAB < pendingBA ? pendingAB : pendingBA;
    const prefundingNeed = pendingAB > pendingBA ? pendingAB - pendingBA : pendingBA - pendingAB;
    const total = pendingAB + pendingBA;
    const imbalanceBps = total === 0n ? 0 : Number(divFloor(prefundingNeed * 10_000n, total));
    const inflowPerDayAB = divFloor(flowAB, BigInt(windowDays));
    const inflowPerDayBA = divFloor(flowBA, BigInt(windowDays));
    const dominantDirection = pendingAB === pendingBA ? null : pendingAB > pendingBA ? `${c.a}>${c.b}` : `${c.b}>${c.a}`;
    const oppositeInflow = pendingAB > pendingBA ? inflowPerDayBA : inflowPerDayAB;
    const estimatedClearDays = prefundingNeed === 0n ? 0 : oppositeInflow === 0n ? null : Number(divFloor(prefundingNeed * 10n, oppositeInflow)) / 10;
    const totalFlow = flowAB + flowBA;
    const flowImbalance = totalFlow === 0n ? 0 : Number(divFloor((flowAB > flowBA ? flowAB - flowBA : flowBA - flowAB) * 10_000n, totalFlow));
    return {
      corridorId: c.id, pendingAB, pendingBA, matchable, prefundingNeed, dominantDirection, imbalanceBps,
      inflowPerDayAB, inflowPerDayBA, estimatedClearDays,
      uncertainty: obs < 30 ? 'HIGH' : obs < 200 ? 'MEDIUM' : 'LOW',
      structurallyImbalanced: obs >= 30 && flowImbalance >= 6_000,
      observations: obs,
    };
  });
}
