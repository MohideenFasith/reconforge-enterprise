# Architecture

## Design goals

ReconForge isolates financial-domain rules from transport and infrastructure code. HTTP routes translate validated input into service calls; domain services own reconciliation behavior; the storage layer provides tenant-scoped persistence; utility modules remain deterministic and independently testable.

## Boundaries

`main.py` creates FastAPI application state, installs metrics middleware, and maps domain errors to stable HTTP responses.

`routes/` is intentionally thin. Route handlers resolve the authenticated principal and service, then delegate behavior.

`service.py` is the application facade for common workflows: account setup, ingestion, reconciliation, exception management, approvals, reporting, webhooks, and exports.

`reconciliation.py` owns run state transitions and the one-to-one auto-match loop. It does not know about HTTP.

`matching/` contains candidate generation and decision logic. Exact, tolerance, fuzzy, grouping, and many-to-one logic are separated so matching strategies can evolve independently.

`storage.py` provides a thread-safe tenant-scoped in-memory adapter. Returned values are deep-copied to prevent mutation from bypassing persistence semantics.

## Domain invariants

- financial entry amounts cannot be zero;
- entry currency must match the selected account;
- transaction external identifiers are unique within a tenant;
- statement identifier + line number is unique within a tenant;
- a reconciliation run executes only from draft or failed state;
- accepted one-to-one matches consume a statement entry once;
- material adjustments require independent approval;
- requesters cannot approve their own adjustment approval;
- journal entries must balance independently by currency;
- closed accounting periods cannot be closed again;
- webhook signatures cover timestamp + canonical JSON payload;
- tenant IDs come from authenticated principals, not client payloads.

## Extension points

A production deployment can replace `InMemoryStore` with a database-backed adapter while retaining the service and domain layers. Webhook HTTP transport is injected through a protocol. Matching policies and reconciliation rules can be extended without changing route definitions.
