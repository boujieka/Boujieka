# Investor journey (`#parcours`)

**Information only, not investment advice.** The platform recommends no country, amount or security, ranks nothing, optimises nothing and promises no return. Personalised investment advice is a regulated activity, so this feature must not drift into it without a licensed partner or an authorisation.

## Flow

1. **Profile:** the client enters their country of residence, currency, horizon (≤1, 1–3, 3–5 or >5 years) and total amount.
2. **Countries:** the client ticks the countries they are interested in. Countries with verified market data (WAEMU, CEMAC) are listed first.
3. **Split:** the client enters an amount per country. The optional "split equally" button is plain arithmetic the client triggers; the platform never proposes a split.
4. **Result, per country:**
   - **Amount and share:** the amount chosen and its share of the total.
   - **Exchange note:** whether a conversion is needed, given that XOF and XAF are pegged to the euro but not interchangeable.
   - **Latest published rates (FACT):** for the maturity buckets of the chosen horizon, over the last 12 months, with the auction date and a link to the source PDF.
   - **Gross interest per year at that past rate (CALCULATION):** amount × rate, before fees, taxes and risks.
   - **Access route:** from the sourced access cards.
   - **Accredited intermediaries:** from the official lists.
5. **Then:**
   - the subscription steps, the questions to ask each intermediary and the risks (default/restructuring, exchange rate, liquidity, tax and fees, past rates);
   - a printable roadmap (browser print → PDF);
   - an optional request to be put in touch with a licensed adviser (Netlify form `mise-en-relation`, which carries a summary of the journey).
   - No partner adviser is appointed yet, and the form says so.

## Accounts and storage

- **Account requirement:** when Supabase accounts are active, the journey requires a free account. Until then, it is open to everyone.
- **Where choices are kept:** in the browser (`localStorage`, key `abm-parcours`). When the client is signed in, they are also saved to their Supabase user metadata (`parcours`).

## Simulate, compare, access (ABM 2.0 phase 1)

- Home page widget « Que pourrait rapporter votre argent ? » and platform section `#comparer`
  (up to 5 countries, goal planner, watchlist in the browser) apply `site/simcalc.js` to
  `yield_points` (build.py): per country and horizon, the latest verified issuance auction of the
  last 12 months whose residual maturity falls in the horizon window. Rate = FACT with its PDF;
  everything else = CALCULATION. CEMAC countries are absent: their recent results publish prices.
- No risk indicator, no score, no automatic allocation: no verified source supports one, and an
  allocation proposer would be personalised advice.
- Section `#acces`: procedure per country (sourced buyer cards; missing fields say « Non renseigné »;
  minimum amount is not in our sources) and a directory of the 320 listings from official lists.
  Only the ⚪ « Liste officielle » status exists; 🔵 / 🟠 / 🟢 need the institution registry
  (phase 2, Supabase) and a documented human verification. No status can be bought.
