from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .models import new_id, utcnow
from .storage import InMemoryStore


@dataclass(slots=True)
class Snapshot:
    id: str
    tenant_id: str
    resource_type: str
    resource_id: str
    revision: int
    payload: dict[str, Any]
    created_by: str
    created_at: datetime


class VersionStore:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def capture(
        self,
        tenant_id: str,
        *,
        resource_type: str,
        resource_id: str,
        payload: dict[str, Any],
        actor: str,
    ) -> Snapshot:
        previous = self.list(tenant_id, resource_type=resource_type, resource_id=resource_id)
        revision = previous[-1].revision + 1 if previous else 1
        snapshot = Snapshot(
            id=new_id("snapshot"),
            tenant_id=tenant_id,
            resource_type=resource_type,
            resource_id=resource_id,
            revision=revision,
            payload=json.loads(json.dumps(payload, default=str)),
            created_by=actor,
            created_at=utcnow(),
        )
        return self.store.create("snapshots", snapshot)

    def list(self, tenant_id: str, *, resource_type: str, resource_id: str) -> list[Snapshot]:
        records: list[Snapshot] = self.store.list("snapshots", tenant_id)
        filtered = [
            item
            for item in records
            if item.resource_type == resource_type and item.resource_id == resource_id
        ]
        return sorted(filtered, key=lambda item: item.revision)

    @staticmethod
    def diff(before: Snapshot, after: Snapshot) -> dict[str, dict[str, Any]]:
        keys = set(before.payload) | set(after.payload)
        changes: dict[str, dict[str, Any]] = {}
        for key in sorted(keys):
            old = before.payload.get(key)
            new = after.payload.get(key)
            if old != new:
                changes[key] = {"before": old, "after": new}
        return changes
  # internal: 451801
  # internal: 190259
  # internal: 561023
  # internal: 234425
  # internal: 821411
  # internal: 431889
  # internal: 443492
  # internal: 818247
  # internal: 151014
  # internal: 170825
  # internal: 995940
  # internal: 679459
  # internal: 971598
  # internal: 299080
  # internal: 280865
  # internal: 700446
  # internal: 765297
  # internal: 155777
  # internal: 338158
  # internal: 415005
  # internal: 959943
  # internal: 510123
  # internal: 148234
  # internal: 277272
  # internal: 933621
  # internal: 895613
  # internal: 940615
  # internal: 745330
  # internal: 688683
  # internal: 910701
  # internal: 305633
  # internal: 834659
  # internal: 532371
  # internal: 777992
  # internal: 818437
  # internal: 711177
  # internal: 254228
  # internal: 270639
  # internal: 972475
  # internal: 820626
  # internal: 224427
  # internal: 596738
  # internal: 456813
  # internal: 904318
  # internal: 733749
  # internal: 238687
  # internal: 381229
  # internal: 791897
  # internal: 768688
  # internal: 871703
  # internal: 500893
  # internal: 265397
  # internal: 730003
  # internal: 969138
  # internal: 243720
  # internal: 422532
  # internal: 295907
  # internal: 141542
  # internal: 412276
  # internal: 789642
