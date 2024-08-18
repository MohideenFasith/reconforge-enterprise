# Operations

## Health and readiness

`/v1/health` reports process liveness and environment. `/v1/ready` includes object counts from the active store. `/metrics` exposes Prometheus metrics.

## Rate limits

`RECONFORGE_RATE_LIMIT_REQUESTS` controls requests allowed in each `RECONFORGE_RATE_LIMIT_WINDOW_SECONDS` sliding window. Limits are independent by API key.

## Import limits

`RECONFORGE_MAX_IMPORT_ROWS` bounds CSV imports before domain objects are created. Large production imports should be routed through a persistent job queue instead of increasing this without considering memory pressure.

## Webhooks

Webhook endpoints must use HTTPS, except loopback hosts used during local development. Each delivery includes event, timestamp, and HMAC-SHA256 signature headers. Retry occurs for transport failures, 429, and 5xx responses; permanent 4xx failures stop immediately.

## Backup and export

The built-in tenant export produces deterministic JSON suitable for offline inspection and migration tooling. The in-memory adapter itself is not durable and should not be used as production persistence.
