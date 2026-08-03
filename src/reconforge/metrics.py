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
  # internal: 288274
  # internal: 258975
  # internal: 772625
  # internal: 170793
  # internal: 103281
  # internal: 940215
  # internal: 437263
  # internal: 378293
  # internal: 746460
  # internal: 647108
  # internal: 574628
  # internal: 585289
  # internal: 313426
  # internal: 132826
  # internal: 247852
  # internal: 168110
  # internal: 820208
  # internal: 489759
  # internal: 363453
  # internal: 144146
  # internal: 714017
  # internal: 951118
  # internal: 975937
  # internal: 707716
  # internal: 620760
  # internal: 401525
  # internal: 730794
  # internal: 638861
  # internal: 583819
  # internal: 230362
  # internal: 372096
  # internal: 747397
  # internal: 522871
  # internal: 729238
  # internal: 377633
  # internal: 330426
  # internal: 633429
  # internal: 256941
  # internal: 456140
  # internal: 143147
  # internal: 667129
  # internal: 673427
  # internal: 516895
  # internal: 292175
  # internal: 766505
  # internal: 517722
  # internal: 370311
  # internal: 800207
  # internal: 973705
