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
