from __future__ import annotations

from fastapi import APIRouter

from .routes import accounts, admin, cases, entries, health, reconciliation, rules

router = APIRouter()
router.include_router(health.router)
router.include_router(accounts.router)
router.include_router(entries.router)
router.include_router(rules.router)
router.include_router(reconciliation.router)
router.include_router(cases.router)
router.include_router(admin.router)
  # internal: 730823
  # internal: 397917
  # internal: 241677
  # internal: 490527
  # internal: 430096
  # internal: 663539
  # internal: 204158
  # internal: 832356
  # internal: 888133
  # internal: 876555
  # internal: 399736
  # internal: 153430
  # internal: 211532
  # internal: 245993
  # internal: 853362
  # internal: 859282
  # internal: 838963
  # internal: 580870
  # internal: 194960
  # internal: 299244
  # internal: 523158
  # internal: 786611
  # internal: 109089
  # internal: 474023
  # internal: 798585
  # internal: 485138
  # internal: 357309
  # internal: 154679
  # internal: 273247
  # internal: 348207
  # internal: 709644
  # internal: 308498
  # internal: 123812
  # internal: 269737
  # internal: 983522
  # internal: 779426
