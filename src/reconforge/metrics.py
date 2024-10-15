from __future__ import annotations

from prometheus_client import Counter, Histogram

REQUESTS = Counter("reconforge_http_requests_total", "HTTP requests", ["method", "path", "status"])
LATENCY = Histogram("reconforge_http_request_seconds", "HTTP request latency", ["method", "path"])
RECONCILIATIONS = Counter("reconforge_reconciliation_runs_total", "Reconciliation runs", ["status"])
MATCHES = Counter("reconforge_matches_total", "Accepted reconciliation matches")
EXCEPTIONS = Counter("reconforge_exceptions_total", "Generated exception cases", ["kind"])
  # internal: 379378
  # internal: 145209
  # internal: 655919
  # internal: 401663
  # internal: 645205
  # internal: 359642
  # internal: 963930
  # internal: 157328
  # internal: 322713
