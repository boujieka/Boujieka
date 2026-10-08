// Run: node --test site/tests/simcalc.test.js   (loads site/simcalc.js into a VM context; also run by backend/tests/test_site_sim.py)
const test = require("node:test"), assert = require("node:assert/strict");
const fs = require("fs"), vm = require("vm");
const ctx = { Math, Number, Object }; vm.createContext(ctx);
vm.runInContext(fs.readFileSync(require("path").join(__dirname, "..", "simcalc.js"), "utf8") + ";this.S=SimCalc;", ctx);
const S = ctx.S, near = (a, b, e = 1e-6) => assert.ok(Math.abs(a - b) <= e, `${a} != ${b}`);
test("par bond: price 100 when coupon == yield", () => near(S.price(6, 6, 5), 100));
test("hold at par: total = amount + h coupons", () => { const r = S.hold(1e6, 6, 6, 5); near(r.total, 1.3e6, 1e-3); near(r.gain, 3e5, 1e-3); });
test("premium bond (coupon > yield) priced above par", () => assert.ok(S.price(5, 7, 5) > 100));
test("zero yield: price = 100 + h*c, gain 0", () => { near(S.price(0, 5, 5), 125); near(S.hold(1e6, 0, 5, 5).gain, 0); });
test("bill branch: coupon null -> simple interest", () => { const r = S.hold(1e6, 5, null, 1); assert.equal(r.kind, "bill"); near(r.gain, 5e4); });
test("coupon undefined treated as bill", () => assert.equal(S.hold(1e6, 5, undefined, 3).kind, "bill"));
test("reinvested compounds", () => near(S.reinvested(100, 10, 2), 121));
test("sensitivity: down < 0 < up, null for h<2 or bills", () => { const s = S.sensitivity(7, 6, 5); assert.ok(s.down < 0 && s.up > 0); assert.equal(S.sensitivity(7, 6, 1), null); assert.equal(S.sensitivity(7, null, 5), null); });
test("goal: zero rate is linear", () => near(S.goal(0, 1200, 0, 1).monthly, 100));
test("goal: capital already enough -> done", () => assert.equal(S.goal(2e6, 1e6, 5, 5).done, true));
// Out-of-domain inputs give null, never NaN or Infinity:
test("goal: tiny positive rate stays finite", () => assert.ok(Number.isFinite(S.goal(0, 1e6, 1e-15, 10).monthly)));
test("goal: huge horizon stays finite or flagged", () => { const g = S.goal(0, 1e6, 6, 1e6); assert.ok(g == null || g.done || Number.isFinite(g.monthly)); });
test("goal: h=0 is rejected", () => { const g = S.goal(0, 1e6, 5, 0); assert.ok(g == null || Number.isFinite(g.monthly)); });
test("hold: yield <= -100 rejected", () => { const r = S.hold(1e6, -100, 5, 5); assert.ok(r == null || Number.isFinite(r.price)); });
test("hold: NaN yield rejected", () => { const r = S.hold(1e6, NaN, 5, 5); assert.ok(r == null || Number.isFinite(r.total)); });
test("hold: non-integer horizon consistent", () => { const r = S.hold(1e6, 6, 6, 2.5); assert.ok(r == null || Math.abs(r.coupons / r.annual - Math.floor(2.5)) < 1e-9); });
test("goal: tiny rate matches the zero-rate result", () => near(S.goal(0, 1e6, 1e-12, 10).monthly, 1e6 / 120, 1e-3));
test("goal: out-of-range inputs give null", () => { assert.equal(S.goal(0, 1e6, 6, 0), null); assert.equal(S.goal(0, 1e6, 6, 1e6), null); assert.equal(S.goal(0, 1e6, -3, 5), null); assert.equal(S.goal(0, 0, 6, 5), null); });
test("hold: reference case (1M at 7.05 %, coupon 5.45 %, 5 years)", () => { const r = S.hold(1e6, 7.05, 5.45, 5); near(r.price, 93.45, 0.01); near(r.gain, 361713, 1); });
test("hold: non-positive or huge amounts give null", () => { assert.equal(S.hold(0, 6, 6, 5), null); assert.equal(S.hold(-5, 6, 6, 5), null); assert.equal(S.hold(1e400, 6, 6, 5), null); });
test("goal reference: 2M to 10M at 7 % over 5 years", () => near(S.goal(2e6, 1e7, 7, 5).monthly, 100076.5, 1));
