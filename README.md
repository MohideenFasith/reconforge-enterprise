# ReconForge Enterprise

ReconForge Enterprise is a self-contained financial reconciliation and exception-management backend for teams that need to compare internal ledger transactions with external bank or processor statements, explain differences, route exceptions, approve adjustments, and retain an auditable evidence trail.

The repository is intentionally designed as a real backend system rather than a demo. It includes domain matching strategies, multi-tenant isolation, API-key authentication, sliding-window rate limiting, idempotent writes, reconciliation orchestration, exception cases, approvals, journal controls, period close controls, webhooks, reporting, audit events, deterministic exports, Prometheus metrics, Docker, CI, strict typing configuration, and an 80% coverage gate.

## Core workflows

1. Create a financial account.
2. Ingest ledger transactions and statement entries through JSON or CSV.
3. Configure or use seeded reconciliation rules.
4. Create a reconciliation run for an account and date window.
5. Execute the run to produce accepted matches and exception cases.
6. Investigate cases, attach evidence, create adjustments, and request approvals for material entries.
7. Review reporting, audit history, and export tenant data.

## Architecture

```text
HTTP routes
   |
   v
ReconForgeService
   |
   +-- accounts / transactions / statement ingestion
   +-- reconciliation orchestration
   |     +-- exact matching
   |     +-- tolerance matching
   |     +-- fuzzy matching
   |     +-- one-to-many / many-to-one grouping helpers
   |
   +-- exception cases / approvals / adjustments
   +-- audit / reporting / webhooks / exports
   +-- close controls / journals / evidence / disputes
   |
   v
InMemoryStore (tenant-scoped, thread-safe)
```

The default storage adapter is deliberately in-process so the whole repository can be built and tested without external databases, queues, object stores, or network services. Domain services depend on the storage abstraction rather than on FastAPI request objects.

See `ARCHITECTURE.md` for module boundaries and invariants.

## Requirements

- Python 3.11–3.13
- pip
- Docker optional

## Fresh-clone setup

```bash
git clone <repository-url>
cd reconforge-enterprise
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.lock
python -m pip install -e . --no-deps
python scripts/verify_reproducibility.py
pytest -q
```

The runtime and development lock artifacts are committed at repository root. `scripts/check_lock.py` verifies that all direct project pins remain aligned with them.

## Run locally

```bash
cp .env.example .env
uvicorn reconforge.main:app --reload
```

Health endpoints:

```text
GET /v1/health
GET /v1/ready
GET /metrics
```

The local development key from `.env.example` can be sent as:

```text
X-API-Key: local-dev-key
```

## Docker

```bash
docker compose up --build
```

The image runs as a non-root user, uses a read-only container filesystem in Compose, exposes a health check, and does not require an external service.

## Tests

```bash
pytest -q
```

Pytest is configured in `pyproject.toml` with branch coverage and an enforced minimum of 80%.

Useful focused commands:

```bash
pytest -q tests/test_reconciliation.py
pytest -q tests/test_matching.py
pytest -q tests/test_api.py
pytest -q tests/test_webhooks.py
```

## Quality checks

```bash
make verify
make lint
make typecheck
make test
make audit
```

CI runs reproducibility checks, Ruff, strict mypy, pytest with coverage, a fresh Docker smoke test, and `pip-audit` as separate jobs.

## Authentication and tenancy

API keys use the form:

```text
key:name:tenant:role+role
```

Multiple keys are separated by commas. The API key is mapped to a `Principal`, and every domain read/write is scoped by its tenant identifier. The service does not trust a tenant identifier supplied in request payloads.

The rate limiter is keyed independently per API key and emits rate-limit headers on authenticated responses.

## Reconciliation behavior

The seeded rule set contains:

- exact reference + amount matching;
- amount tolerance matching with a short date window;
- counterparty-aware fallback matching.

The matching engine also exposes fuzzy fallback logic. Ambiguous candidates are intentionally not auto-accepted when the confidence gap is too small.

Additional finance modules support:

- one-to-many allocations;
- many-to-one allocations;
- net settlement grouping;
- duplicate fingerprints;
- payment-reference parsing;
- business-day calendars;
- currency quantization and FX conversion;
- journal balancing;
- materiality policies;
- variance rules;
- reconciliation quality scoring;
- quality-control sampling;
- exception aging and SLA state;
- close readiness controls;
- suspense exposure;
- evidence and dispute workflows;
- resource lineage and snapshots.

## Example API flow

Create an account:

```bash
curl -X POST http://localhost:8000/v1/accounts \
  -H 'content-type: application/json' \
  -H 'X-API-Key: local-dev-key' \
  -d '{"name":"Operating Account","external_id":"BANK-001","currency":"USD"}'
```

Create a ledger transaction:

```bash
curl -X POST http://localhost:8000/v1/transactions \
  -H 'content-type: application/json' \
  -H 'X-API-Key: local-dev-key' \
  -H 'Idempotency-Key: ledger-2026-08-001' \
  -d '{"external_id":"TX-001","account_id":"<account-id>","occurred_on":"2026-08-01","amount":"125.50","currency":"USD","reference":"INV-9001","counterparty":"Acme Ltd"}'
```

Create the matching statement line and then POST a reconciliation run to `/v1/reconciliation-runs` before executing `/v1/reconciliation-runs/{run_id}/execute`.

## CSV imports

Transaction CSV requires:

```text
external_id,account_id,occurred_on,amount,currency
```

Statement CSV requires:

```text
statement_id,line_number,account_id,occurred_on,amount,currency
```

Optional columns include `reference`, `counterparty`, and `description`. Imports have a configurable maximum row count and reject malformed dates, amounts, missing columns, and duplicate identifiers.

## Repository hygiene

The repository deliberately rejects synthetic source-padding markers through `scripts/check_no_padding.py`. Do not add meaningless comments or manufactured commit history to increase line counts or commit counts.

For future development, each behavior change should be committed with the test that proves it. Keep feature changes, refactors, formatting, and dependency bumps separate when practical.

## Security

See `SECURITY.md`. The baseline includes:

- API-key authentication;
- tenant-scoped storage;
- role-gated administrative endpoints;
- sliding-window rate limiting;
- strict Pydantic request validation;
- webhook HMAC signatures;
- HTTPS-only webhook destinations except localhost;
- no committed `.env` secrets;
- read-only Docker runtime configuration;
- dependency auditing in CI.

## License

See `LICENSE.txt`. Replace the placeholder licensing terms before public distribution or commercial licensing if your intended terms differ.
