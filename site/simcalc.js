// Shared bond arithmetic for the simulators (home page and platform). Pure functions, no data.
// Rates are in percent per year; amounts in the security's currency. Annual coupons assumed.
const SimCalc = (() => {
  // Price per 100 of nominal for a bond paying an annual coupon c (%) for h years at yield y (%).
  const price = (y, c, h) => {
    const r = y / 100; let p = 0;
    for (let t = 1; t <= h; t++) p += c / Math.pow(1 + r, t);
    return p + 100 / Math.pow(1 + r, h);
  };
  // Hold to maturity: buy at the price implied by the published yield, cash every coupon, get the nominal back.
  function hold(amount, y, coupon, h) {
    if (coupon == null || h < 1) {  // bill-like: simple interest at the published rate over the horizon
      const gain = amount * (y / 100) * h;
      return { kind: "bill", price: null, nominal: null, annual: amount * y / 100, coupons: gain, capital: amount, total: amount + gain, gain };
    }
    const p = price(y, coupon, h), nominal = amount * 100 / p, annual = nominal * coupon / 100, coupons = annual * h;
    return { kind: "bond", price: p, nominal, annual, coupons, capital: nominal, total: nominal + coupons, gain: nominal + coupons - amount };
  }
  // Coupons reinvested at the same rate until the horizon.
  const reinvested = (amount, y, h) => amount * Math.pow(1 + y / 100, h);
  // Resale value right after purchase if market yields move by d points (exact repricing).
  function sensitivity(y, coupon, h, d = 1) {
    if (coupon == null || h < 2) return null;
    const p0 = price(y, coupon, h);
    return { down: price(y + d, coupon, h) / p0 - 1, up: price(y - d, coupon, h) / p0 - 1 };
  }
  // Monthly saving needed to reach a target from a starting capital at rate y over h years.
  function goal(capital, target, y, h) {
    const i = y / 100 / 12, n = Math.round(h * 12), fvCap = capital * Math.pow(1 + i, n);
    if (fvCap >= target) return { monthly: 0, done: true };
    const m = i === 0 ? (target - capital) / n : (target - fvCap) * i / (Math.pow(1 + i, n) - 1);
    return { monthly: m, done: false };
  }
  return { price, hold, reinvested, sensitivity, goal };
})();
