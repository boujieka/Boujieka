import 'reflect-metadata';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import { Test } from '@nestjs/testing';
import type { INestApplication } from '@nestjs/common';
import request from 'supertest';
import { type SwapSimulator, SimulatedProvider } from '@diasposwap/settlement-engine';
import { AppModule } from '../src/app.module';
import { CONFIG, SIMULATOR, createSimulator, loadConfig } from '../src/simulator.provider';
import { configureApp } from '../src/configure';

const cfg = loadConfig({ DIASPOSWAP_ADMIN_KEYS: 'ops-key-123:ops,comp-key-AAA:compliance,comp-key-BBB:compliance', DIASPOSWAP_WEBHOOK_SECRET: 'test-secret' } as NodeJS.ProcessEnv);
let app: INestApplication;
let sim: SwapSimulator;

beforeAll(async () => {
  sim = createSimulator(cfg);
  const mod = await Test.createTestingModule({ imports: [AppModule] }).overrideProvider(CONFIG).useValue(cfg).overrideProvider(SIMULATOR).useValue(sim).compile();
  app = configureApp(mod.createNestApplication({ rawBody: true }));
  await app.init();
  const add = (userId: string, name: string, c: 'FR' | 'CM' | 'CA', pep = false) => sim.addUser({ profile: { userId, fullName: name, country: c, kycLevel: 'VERIFIED', emailVerified: true, phoneVerified: true, pep }, fundingRef: `SIM-${c}-1`, history: [] });
  add('alice', 'Amina Mbarga', 'FR'); add('bob', 'Jean Essomba', 'CM'); add('pep', 'Serge Bakala', 'CA', true);
  sim.addBeneficiary({ id: 'benA', ownerId: 'alice', fullName: 'Paul Mbarga', country: 'CM', verified: true, accountRef: 'SIM-CM-11' });
  sim.addBeneficiary({ id: 'benB', ownerId: 'bob', fullName: 'Grace Essomba', country: 'FR', verified: true, accountRef: 'SIM-FR-22' });
  sim.addBeneficiary({ id: 'benP', ownerId: 'pep', fullName: 'Lea Bakala', country: 'CM', verified: true, accountRef: 'SIM-CM-33' });
});
afterAll(async () => { await app.close(); });

const http = () => request(app.getHttpServer());
const ops = { 'x-admin-key': 'ops-key-123' };

async function placeAndFund(user: string, from: string, to: string, amount: string, ben: string, key: string) {
  const q = await http().post('/v1/quotes').set('x-demo-user', user).send({ from, to, amount }).expect(201);
  const o = await http().post('/v1/orders').set('x-demo-user', user).set('idempotency-key', key).send({ quoteId: q.body.id, beneficiaryId: ben }).expect(201);
  if (o.body.state === 'PENDING_FUNDING') await http().post(`/v1/orders/${o.body.id}/fund`).set('x-demo-user', user).expect(201);
  return { quote: q.body, order: o.body };
}

describe('DiaspoSwap API (simulation)', () => {
  it('health advertises simulation mode', async () => {
    const r = await http().get('/health').expect(200);
    expect(r.body.mode).toBe('SIMULATION');
    expect(r.headers['x-diasposwap-mode']).toBe('SIMULATION');
  });

  it('full France -> Cameroon flow over HTTP, amounts as minor-unit strings', async () => {
    const a = await placeAndFund('alice', 'FR', 'CM', '1000', 'benA', 'alice-key-0001');
    expect(a.quote.principal).toBe('100000');
    expect(a.quote.estimatedReceive).toBe('655957');
    await placeAndFund('bob', 'CM', 'FR', '655957', 'benB', 'bob-key-00001');
    await http().post('/v1/demo/settle-pending').set(ops).expect(201);
    const run = await http().post('/v1/admin/matching/run').set(ops).expect(201);
    expect(run.body.allocations).toHaveLength(1);
    await http().post('/v1/demo/settle-pending').set(ops).expect(201);
    const view = await http().get(`/v1/orders/${a.order.id}`).set('x-demo-user', 'alice').expect(200);
    expect(view.body.state).toBe('SETTLED');
    expect(view.body.beneficiaryReceived).toBe('655957');
    expect(JSON.stringify(view.body)).not.toMatch(/bob|Essomba|SIM-FR/);
    const rec = await http().get('/v1/admin/reconciliation').set(ops).expect(200);
    expect(rec.body.ok).toBe(true);
  });

  it('idempotency: same key returns the same order; key is mandatory', async () => {
    const q = await http().post('/v1/quotes').set('x-demo-user', 'alice').send({ from: 'FR', to: 'CM', amount: '50' }).expect(201);
    const r1 = await http().post('/v1/orders').set('x-demo-user', 'alice').set('idempotency-key', 'same-key-123').send({ quoteId: q.body.id, beneficiaryId: 'benA' }).expect(201);
    const r2 = await http().post('/v1/orders').set('x-demo-user', 'alice').set('idempotency-key', 'same-key-123').send({ quoteId: q.body.id, beneficiaryId: 'benA' }).expect(201);
    expect(r2.body.id).toBe(r1.body.id);
    await http().post('/v1/orders').set('x-demo-user', 'alice').send({ quoteId: q.body.id, beneficiaryId: 'benA' }).expect(400);
  });

  it('validation and ownership', async () => {
    await http().post('/v1/quotes').set('x-demo-user', 'alice').send({ from: 'FR', to: 'XX', amount: '1' }).expect(400);
    await http().post('/v1/quotes').set('x-demo-user', 'alice').send({ from: 'FR', to: 'CM', amount: '1.234' }).expect(400);
    await http().post('/v1/quotes').send({ from: 'FR', to: 'CM', amount: '1' }).expect(401);
    const { order } = await placeAndFund('alice', 'FR', 'CM', '20', 'benA', 'alice-key-0002');
    await http().get(`/v1/orders/${order.id}`).set('x-demo-user', 'bob').expect(404);
  });

  it('webhooks: forged signature refused, valid accepted, replay flagged duplicate', async () => {
    const { order } = await placeAndFund('alice', 'FR', 'CM', '30', 'benA', 'alice-key-0003');
    const o = sim.orders.get(order.id)!;
    const p = sim.providers.find((x) => x.id === 'sim_sepa') as SimulatedProvider;
    const wh = p.complete(o.collectionRef!);
    await http().post('/v1/webhooks/sim_sepa').set('content-type', 'application/json').set('x-signature', 'bad').send(wh.rawBody).expect(403);
    const ok = await http().post('/v1/webhooks/sim_sepa').set('content-type', 'application/json').set('x-signature', wh.signature).send(wh.rawBody).expect(200);
    expect(ok.body).toEqual({ accepted: true });
    const dup = await http().post('/v1/webhooks/sim_sepa').set('content-type', 'application/json').set('x-signature', wh.signature).send(wh.rawBody).expect(200);
    expect(dup.body.duplicate).toBe(true);
  });

  it('admin authorisation: no key 401, wrong role 403', async () => {
    await http().post('/v1/admin/matching/run').expect(401);
    await http().post('/v1/admin/matching/run').set('x-admin-key', 'comp-key-AAA').expect(403);
    await http().post('/v1/admin/compliance/x/decision').set(ops).send({ approve: true }).expect(403);
  });

  it('compliance review requires two different officers (four-eyes)', async () => {
    const { order } = await placeAndFund('pep', 'CA', 'CM', '100', 'benP', 'pep-key-00001');
    expect(order.state).toBe('PENDING_VERIFICATION');
    const path = `/v1/admin/compliance/${order.id}/decision`;
    expect((await http().post(path).set('x-admin-key', 'comp-key-AAA').send({ approve: true }).expect(201)).body.status).toBe('AWAITING_SECOND_APPROVAL');
    await http().post(path).set('x-admin-key', 'comp-key-AAA').send({ approve: true }).expect(403);
    const done = await http().post(path).set('x-admin-key', 'comp-key-BBB').send({ approve: true }).expect(201);
    expect(done.body.status).toBe('APPLIED');
    expect(done.body.order.state).toBe('PENDING_FUNDING');
  });
});
