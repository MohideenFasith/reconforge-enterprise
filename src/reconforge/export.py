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
  # internal: 132844
  # internal: 266140
  # internal: 111430
  # internal: 306698
  # internal: 832667
  # internal: 221023
  # internal: 140220
  # internal: 807777
  # internal: 181998
  # internal: 634299
  # internal: 656164
  # internal: 422979
  # internal: 699876
  # internal: 833064
  # internal: 216895
  # internal: 216775
  # internal: 140296
  # internal: 357633
  # internal: 845965
  # internal: 893238
  # internal: 719596
  # internal: 336682
  # internal: 575148
  # internal: 247693
  # internal: 910471
  # internal: 800144
  # internal: 635868
  # internal: 338919
  # internal: 489247
  # internal: 884746
  # internal: 227153
  # internal: 314683
  # internal: 902075
  # internal: 244104
  # internal: 558482
  # internal: 679701
  # internal: 524363
  # internal: 426902
  # internal: 736772
