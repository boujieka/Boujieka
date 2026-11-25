# API walkthrough (simulation)

```bash
cd diasposwap
DIASPOSWAP_ADMIN_KEYS=ops-dev-key:ops DIASPOSWAP_SEED_DEMO=true npm run api
```

The seeded demo users are fictional (`seedDemo`, seed 42). List them, with country and beneficiary ids:
`curl -s localhost:3000/v1/demo/users -H 'x-admin-key: ops-dev-key'`. Then, with a user living in France:

```bash
curl -s localhost:3000/health
curl -s -X POST localhost:3000/v1/quotes -H 'content-type: application/json' -H 'x-demo-user: <a FR user id>' \
  -d '{"from":"FR","to":"CM","amount":"1000"}'
curl -s -X POST localhost:3000/v1/admin/matching/run -H 'x-admin-key: ops-dev-key'
curl -s localhost:3000/v1/admin/reconciliation -H 'x-admin-key: ops-dev-key'
```

The full contract is `openapi.yaml`; the e2e tests in `apps/api/test/api.e2e.test.ts` are executable examples.
