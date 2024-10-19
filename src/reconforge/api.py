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
