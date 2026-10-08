// Shared bond arithmetic for the simulators (home page and platform). Pure functions, no data.
// Rates are in percent per year; amounts in the security's currency. Annual coupons assumed.
// Every function returns null for inputs outside its domain instead of NaN or Infinity.
const SimCalc = (() => {
  const fin = (...v) => v.every((x) => typeof x === "number" && Number.isFinite(x));
  const okYield = (y) => fin(y) && y > -100 && y <= 100;
  const okH = (h) => Number.isInteger(h) && h >= 1 && h <= 50;
  const out = (o) => (Object.values(o).every((v) => v === null || typeof v !== "number" || Number.isFinite(v)) ? o : null);
  // Price per 100 of nominal for a bond paying an annual coupon c (%) for h whole years at yield y (%).
  const price = (y, c, h) => {
    if (!okYield(y) || !fin(c) || c < 0 || !okH(h)) return null;
    const r = y / 100; let p = 0;
    for (let t = 1; t <= h; t++) p += c / Math.pow(1 + r, t);
    return p + 100 / Math.pow(1 + r, h);
  };
  // Hold to maturity: buy at the price implied by the published yield, cash every coupon, get the nominal back.
  function hold(amount, y, coupon, h) {
    if (!fin(amount) || amount <= 0 || !okYield(y) || !okH(h)) return null;
    if (coupon == null) {  // bill-like: simple interest at the published rate over the horizon (rolled over at the same rate)
      const gain = amount * (y / 100) * h;
      return out({ kind: "bill", price: null, nominal: null, annual: amount * y / 100, coupons: gain, capital: amount, total: amount + gain, gain });
    }
    const p = price(y, coupon, h);
    if (p == null || p <= 0) return null;
    const nominal = amount * 100 / p, annual = nominal * coupon / 100, coupons = annual * h;
    return out({ kind: "bond", price: p, nominal, annual, coupons, capital: nominal, total: nominal + coupons, gain: nominal + coupons - amount });
  }
  // Coupons reinvested at the same rate until the horizon.
  const reinvested = (amount, y, h) => (fin(amount) && amount > 0 && okYield(y) && okH(h) ? amount * Math.pow(1 + y / 100, h) : null);
  // Resale value right after purchase if market yields move by d points (exact repricing).
  function sensitivity(y, coupon, h, d = 1) {
    if (coupon == null || !okH(h) || h < 2 || !fin(d)) return null;
    const p0 = price(y, coupon, h), pd = price(y + d, coupon, h), pu = price(y - d, coupon, h);
    return p0 && pd != null && pu != null ? { down: pd / p0 - 1, up: pu / p0 - 1 } : null;
  }
  // Monthly saving needed to reach a target from a starting capital at rate y (0-40 %) over h whole years (1-50).
  function goal(capital, target, y, h) {
    if (!fin(capital, target, y) || capital < 0 || target <= 0 || y < 0 || y > 40 || !okH(h)) return null;
    const i = y / 100 / 12, n = h * 12;
    const growth = i < 1e-9 ? 0 : Math.expm1(n * Math.log1p(i));  // (1+i)^n - 1 without rounding loss
    const fvCap = capital * (1 + growth);
    if (fvCap >= target) return { monthly: 0, done: true };
    const m = i < 1e-9 ? (target - capital) / n : (target - fvCap) * i / growth;
    return Number.isFinite(m) ? { monthly: m, done: false } : null;
  }
  return { price, hold, reinvested, sensitivity, goal };
})();
if (typeof module !== "undefined") module.exports = SimCalc;  // node tests
