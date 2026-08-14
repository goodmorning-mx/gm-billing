# gm-billing

Reusable GoodMorning usage metering and ledger module. It records product,
organization, user, provider, model, input/output/cached tokens, request ID,
timestamp, provider cost, and GoodMorning charge. Pricing is explicit and
versionable; the ledger is append-only at the service boundary.

`migrations/001_usage_ledger.sql` is PostgreSQL-ready. The in-memory store is
for local development/tests; production adapters implement `add_usage` and
`add_ledger` against the product's PostgreSQL service. No payment gateway is
included. A future wallet can be added as another ledger entry type without
changing usage metering.

Install backend with `pip install gm-billing`; install frontend from
`frontend/` as `@goodmorning/gm-billing`. `create_app()` exposes `/health`,
`POST /usage`, and `GET /usage/summary`.
