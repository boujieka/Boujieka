import {
  BadRequestException, Body, Controller, ForbiddenException, Get, Headers, HttpCode, Inject, NotFoundException, Param, Post, Req, UseGuards,
} from '@nestjs/common';
import type { Request } from 'express';
import { z } from 'zod';
import { type CountryCode, COUNTRIES, INITIAL_CORRIDORS, MoneyError, parseMajor } from '@diasposwap/shared-types';
import { SIMULATION_NOTICE_EN, SimulationError, type SwapSimulator } from '@diasposwap/settlement-engine';
import { analyseLiquidity } from '@diasposwap/liquidity';
import { simulateMultilateral } from '@diasposwap/matching-engine';
import { AdminGuard, Roles, UserGuard } from './guards';
import { SIMULATOR } from './simulator.provider';
import { toJson } from './serialize';

const country = z.enum(Object.keys(COUNTRIES) as [CountryCode, ...CountryCode[]]);
const QuoteBody = z.object({ from: country, to: country, amount: z.string().min(1).max(20) });
const OrderBody = z.object({ quoteId: z.string().min(1), beneficiaryId: z.string().min(1), allowPartial: z.boolean().default(true) });
const DecisionBody = z.object({ approve: z.boolean() });

function parse<T>(schema: z.ZodType<T>, body: unknown): T {
  const r = schema.safeParse(body);
  if (!r.success) throw new BadRequestException({ code: 'VALIDATION', issues: r.error.issues.map((i) => ({ path: i.path.join('.'), message: i.message })) });
  return r.data;
}

function wrap<T>(fn: () => T): unknown {
  try {
    return toJson(fn());
  } catch (e) {
    if (e instanceof SimulationError) {
      if (e.code.startsWith('UNKNOWN_')) throw new NotFoundException({ code: e.code, message: e.message });
      throw new BadRequestException({ code: e.code, message: e.message });
    }
    if (e instanceof MoneyError) throw new BadRequestException({ code: 'INVALID_AMOUNT', message: e.message });
    throw e;
  }
}

@Controller()
export class PublicController {
  constructor(@Inject(SIMULATOR) private readonly sim: SwapSimulator) {}

  @Get('health')
  health() { return { status: 'ok', mode: 'SIMULATION', notice: SIMULATION_NOTICE_EN }; }

  @Get('v1/corridors')
  corridors() { return toJson(INITIAL_CORRIDORS); }

  @Get('v1/rates')
  rates() { return toJson(this.sim.rates()); }
}

@Controller('v1')
@UseGuards(UserGuard)
export class TransferController {
  constructor(@Inject(SIMULATOR) private readonly sim: SwapSimulator) {}

  @Post('quotes')
  quote(@Headers('x-demo-user') userId: string, @Body() body: unknown) {
    const b = parse(QuoteBody, body);
    return wrap(() => this.sim.quote(userId, b.from, b.to, parseMajor(b.amount, COUNTRIES[b.from].currency)));
  }

  @Post('orders')
  create(@Headers('x-demo-user') userId: string, @Headers('idempotency-key') idem: string | undefined, @Body() body: unknown) {
    if (!idem || idem.length < 8) throw new BadRequestException({ code: 'IDEMPOTENCY_KEY_REQUIRED', message: 'Idempotency-Key header (>= 8 chars) is required' });
    const b = parse(OrderBody, body);
    const q = this.sim.quotes.get(b.quoteId);
    if (!q || q.userId !== userId) throw new NotFoundException({ code: 'UNKNOWN_QUOTE' });
    return wrap(() => this.sim.createOrder({ ...b, idempotencyKey: `${userId}:${idem}` }));
  }

  @Post('orders/:id/fund')
  fund(@Headers('x-demo-user') userId: string, @Param('id') id: string) {
    this.owned(userId, id);
    return wrap(() => this.sim.fund(id));
  }

  @Post('orders/:id/cancel')
  cancel(@Headers('x-demo-user') userId: string, @Param('id') id: string) {
    this.owned(userId, id);
    return wrap(() => this.sim.userView(this.sim.cancel(id, userId).id));
  }

  @Get('orders/:id')
  get(@Headers('x-demo-user') userId: string, @Param('id') id: string) {
    this.owned(userId, id);
    return wrap(() => this.sim.userView(id));
  }

  @Get('orders')
  list(@Headers('x-demo-user') userId: string) {
    return wrap(() => [...this.sim.orders.values()].filter((o) => o.userId === userId).map((o) => this.sim.userView(o.id)));
  }

  private owned(userId: string, id: string) {
    const o = this.sim.orders.get(id);
    // same response for "not found" and "not yours": no order enumeration
    if (!o || o.userId !== userId) throw new NotFoundException({ code: 'UNKNOWN_ORDER' });
  }
}

@Controller('v1/webhooks')
export class WebhookController {
  constructor(@Inject(SIMULATOR) private readonly sim: SwapSimulator) {}

  /** Provider callbacks. The signature is an HMAC-SHA256 of the RAW body. */
  @Post(':providerId')
  @HttpCode(200)
  receive(@Param('providerId') providerId: string, @Headers('x-signature') signature: string | undefined, @Req() req: Request & { rawBody?: Buffer }) {
    const raw = req.rawBody?.toString('utf8') ?? '';
    const r = this.sim.handleWebhook(providerId, raw, signature ?? '');
    if (!r.accepted) throw new ForbiddenException({ code: r.reason });
    return r;
  }
}

@Controller('v1/admin')
@UseGuards(AdminGuard)
export class AdminController {
  /** Pending four-eyes approvals: orderId -> first officer. */
  private readonly pendingDecisions = new Map<string, { officer: string; approve: boolean }>();

  constructor(@Inject(SIMULATOR) private readonly sim: SwapSimulator) {}

  @Post('matching/run')
  @Roles('ops')
  run() { return wrap(() => this.sim.runMatching()); }

  @Get('reconciliation')
  reconcile() { return wrap(() => ({ ...this.sim.reconcile(), trialBalance: this.sim.ledger.trialBalance() })); }

  @Get('liquidity')
  liquidity() {
    const orders = [...this.sim.orders.values()];
    return wrap(() => ({ corridors: analyseLiquidity({ orders, rates: this.sim.rates(), now: new Date() }), multilateral: simulateMultilateral(orders, this.sim.rates(), { mode: 'simulation' }) }));
  }

  @Get('stats')
  stats() {
    const orders = [...this.sim.orders.values()];
    const byState: Record<string, number> = {};
    for (const o of orders) byState[o.state] = (byState[o.state] ?? 0) + 1;
    return wrap(() => ({
      mode: 'SIMULATION', users: this.sim.users.size, orders: orders.length, byState,
      allocations: this.sim.allocations.length, exceptions: this.sim.exceptions.length,
      reviewQueue: orders.filter((o) => o.compliance === 'REVIEW').map((o) => o.id),
    }));
  }

  @Get('audit/:orderId')
  audit(@Param('orderId') orderId: string) {
    return wrap(() => ({ stateChanges: this.sim.audit.filter((a) => a.orderId === orderId), ledger: this.sim.ledger.forReference(orderId) }));
  }

  /** Sensitive decision: requires two DIFFERENT compliance officers agreeing (four-eyes). */
  @Post('compliance/:orderId/decision')
  @Roles('compliance')
  decide(@Param('orderId') orderId: string, @Body() body: unknown, @Req() req: Request & { adminKeyId?: string }) {
    const { approve } = parse(DecisionBody, body);
    const officer = req.adminKeyId ?? 'unknown';
    const first = this.pendingDecisions.get(orderId);
    if (!first) {
      this.pendingDecisions.set(orderId, { officer, approve });
      return { status: 'AWAITING_SECOND_APPROVAL' };
    }
    if (first.officer === officer) throw new ForbiddenException({ code: 'SAME_OFFICER', message: 'A second, different officer must confirm' });
    if (first.approve !== approve) {
      this.pendingDecisions.delete(orderId);
      return { status: 'CONFLICT_ESCALATED' };
    }
    this.pendingDecisions.delete(orderId);
    return wrap(() => ({ status: 'APPLIED', order: this.sim.userView(this.sim.reviewDecision(orderId, approve, `${first.officer}+${officer}`).id) }));
  }
}

@Controller('v1/demo')
@UseGuards(AdminGuard)
export class DemoController {
  constructor(@Inject(SIMULATOR) private readonly sim: SwapSimulator) {}

  /** Completes every pending SIMULATED provider operation (delivers signed webhooks). */
  @Post('settle-pending')
  @Roles('ops')
  settle() { return { completed: this.sim.settleAllPending() }; }

  /** Fictional demo users with their country and beneficiary ids (no names), to drive the API by hand. */
  @Get('users')
  users() {
    return [...this.sim.users.values()].slice(0, 200).map((u) => ({
      userId: u.profile.userId, country: u.profile.country,
      beneficiaries: [...this.sim.beneficiaries.values()].filter((b) => b.ownerId === u.profile.userId).map((b) => ({ id: b.id, country: b.country })),
    }));
  }
}
