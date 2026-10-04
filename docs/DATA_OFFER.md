# Offers, waiting list and daily brief

Phase 1 of monetisation: test demand and price before building accounts or payments.
The site's « Offres » section (`#offres`) presents three products. None of them is on sale yet.

| Offer | What is public | What is private (not deployed) | Built by |
|---|---|---|---|
| Quarterly report | Previews `/rapports/` (HTML and PDF) | Complete editions `site/reports/<quarter>/` | `site/report.py` |
| Data licence | Dictionary and coverage `/donnees/fr.html` and `/donnees/en.html`, plus a sample of 25 rows `/donnees/echantillon.csv` | `site/reports/data/` (`auctions.csv`, `securities.csv`, `documents.csv`, `LISEZMOI.txt`) | `site/dataset.py` |
| Auction brief | Section `#brief`, plus e-mail-ready pages `/brief/fr.html` and `/brief/en.html` | none | `site/brief.py` |

`site/build.py` runs all three, so the daily job refreshes them.

## The brief

The brief contains only facts:

- the verified results of the last 7 days;
- the 7-day issuance totals next to the previous 7 days (a calculation);
- the securities in our data that mature in the next 14 days.

It contains no ranking, no opinion and no recommendation. Amounts outstanding at maturity are not published per security, so they are not shown.

The brief is not e-mailed yet. Sending it needs:

- an e-mail provider account opened by the owner;
- a sender domain;
- consent and unsubscribe handling.

## Waiting list (Netlify Forms)

The form `liste-attente` collects the following fields:

- e-mail, profile and consent (required);
- organisation and country;
- interests, as one checkbox per product;
- the acceptable price for each product (ranges in USD);
- an optional message;
- the interface language.

Spam is filtered with a honeypot field (`bot-field`). The JavaScript posts the form to `/`; without JavaScript, the browser posts it natively and lands on `/merci.html`. The CSP allows `form-action 'self'`.

- **Where submissions go:** Netlify → project `cartouche-africa` → Forms. They can be exported as CSV from there.
- **Removal requests:** the person sends the form again with "Me retirer de la liste" ticked. Delete all of that address's submissions.
- **Privacy notice:** the text under the form says that the data are stored by Netlify in the United States and are used only for this purpose.
- **Plan limits:** check them in Netlify. The number of free submissions per month depends on the plan.

## Before selling

1. **Data licence:** check the reuse terms of UMOA-Titres' publications. Commercial redistribution of figures extracted from their reports may be restricted.
2. **Coats of arms in the paid report:** see `docs/QUARTERLY_REPORT.md`.
3. **Prices:** read the waiting-list answers. The price question per product is the point of the test.
4. **Payment:** use a payment link (Stripe, Gumroad, Lemon Squeezy…) opened by the owner. Then set `CARTOUCHE_REPORT_PURCHASE_URL` so the button appears.

The platform's free tier already lets anyone browse the market table and export it as CSV. The data licence sells something different:

- the consolidated file with full provenance;
- updates;
- the right to reuse the data in the buyer's own products.
