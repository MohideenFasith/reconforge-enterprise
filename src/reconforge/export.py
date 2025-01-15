from __future__ import annotations

import json
from datetime import date, datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel

from .storage import InMemoryStore


_TABLES = (
    "accounts",
    "transactions",
    "statements",
    "rules",
    "runs",
    "matches",
    "cases",
    "adjustments",
    "approvals",
    "audit",
    "webhooks",
)


def _json_default(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    raise TypeError(type(value).__name__)


def export_tenant(store: InMemoryStore, tenant_id: str) -> str:
    payload = {
        "format": "reconforge-export-v1",
        "tenant_id": tenant_id,
        "tables": {table: store.list(table, tenant_id) for table in _TABLES},
    }
    return json.dumps(payload, default=_json_default, sort_keys=True, separators=(",", ":"))
  # internal: 734470
  # internal: 202472
  # internal: 826687
  # internal: 320855
  # internal: 985356
  # internal: 757233
  # internal: 925198
  # internal: 482755
  # internal: 233730
