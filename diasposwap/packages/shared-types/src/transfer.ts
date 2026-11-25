import type { CountryCode } from './corridors';
import type { CurrencyCode } from './money';

export const TRANSFER_STATES = [
  'DRAFT', 'QUOTED', 'PENDING_VERIFICATION', 'PENDING_FUNDING', 'FUNDED', 'QUEUED',
  'PARTIALLY_MATCHED', 'MATCHED', 'SETTLEMENT_PENDING', 'SETTLED', 'FAILED', 'EXPIRED',
  'CANCELLED', 'REFUND_PENDING', 'REFUNDED', 'DISPUTED',
] as const;
export type TransferState = (typeof TRANSFER_STATES)[number];

/** Explicit allowed transitions. Anything not listed is rejected. */
export const TRANSITIONS: Readonly<Record<TransferState, readonly TransferState[]>> = {
  DRAFT: ['QUOTED', 'CANCELLED'],
  QUOTED: ['PENDING_VERIFICATION', 'PENDING_FUNDING', 'EXPIRED', 'CANCELLED'],
  PENDING_VERIFICATION: ['PENDING_FUNDING', 'FAILED', 'CANCELLED'],
  PENDING_FUNDING: ['FUNDED', 'EXPIRED', 'CANCELLED', 'FAILED'],
  FUNDED: ['QUEUED', 'REFUND_PENDING'],
  QUEUED: ['PARTIALLY_MATCHED', 'MATCHED', 'EXPIRED', 'REFUND_PENDING'],
  PARTIALLY_MATCHED: ['PARTIALLY_MATCHED', 'MATCHED', 'SETTLEMENT_PENDING', 'EXPIRED', 'REFUND_PENDING'],
  MATCHED: ['SETTLEMENT_PENDING'],
  SETTLEMENT_PENDING: ['SETTLED', 'DISPUTED', 'REFUND_PENDING'],
  SETTLED: ['DISPUTED'],
  FAILED: [],
  EXPIRED: ['REFUND_PENDING'],
  CANCELLED: [],
  REFUND_PENDING: ['REFUNDED', 'DISPUTED'],
  REFUNDED: [],
  DISPUTED: ['SETTLED', 'REFUND_PENDING'],
};

export class TransitionError extends Error {}

export function canTransition(from: TransferState, to: TransferState): boolean {
  return TRANSITIONS[from].includes(to);
}

export function assertTransition(from: TransferState, to: TransferState): void {
  if (!canTransition(from, to)) throw new TransitionError(`Illegal transition ${from} -> ${to}`);
}

export type ComplianceStatus = 'NOT_CHECKED' | 'CLEARED' | 'REVIEW' | 'BLOCKED';

/** A transfer order as seen by the matching engine. Amounts are minor units of `sendCurrency`. */
export interface TransferOrder {
  id: string;
  userId: string;
  fromCountry: CountryCode;
  toCountry: CountryCode;
  sendCurrency: CurrencyCode;
  receiveCurrency: CurrencyCode;
  /** Principal to transfer, excluding fees. */
  principal: bigint;
  /** Principal not yet allocated to a match. */
  remaining: bigint;
  createdAt: string;
  expiresAt: string;
  /** If false, the order is all-or-none: matched in full in one run or not at all. */
  allowPartial: boolean;
  state: TransferState;
  compliance: ComplianceStatus;
}

export interface StateChange {
  orderId: string;
  from: TransferState;
  to: TransferState;
  at: string;
  reason: string;
  actor: string;
}
