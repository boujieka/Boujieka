# DiaspoSwap mobile (Expo SDK 58)

Simulation mode only: every screen shows "Mode simulation — aucun argent réel". The financial engines from
`packages/*` run inside the app (no backend required for the demo).

```bash
# from the monorepo root (diasposwap/)
npm install
npm --workspace apps/mobile run start      # Expo dev server (scan with Expo Go / dev build)
npm --workspace apps/mobile run web        # browser
npm --workspace apps/mobile run typecheck
```

Demo flow: onboarding → demo login (any 4-digit PIN) → *Envoyer* → 1000 EUR to Cameroon → confirm →
on the tracking screen use the demo tools: *Simuler un ordre inverse*, *Lancer le matching*, *Confirmer les paiements simulés*.
