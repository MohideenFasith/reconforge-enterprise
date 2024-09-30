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
