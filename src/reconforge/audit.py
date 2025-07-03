from __future__ import annotations

from typing import Any

from .models import AuditEvent, new_id
from .storage import InMemoryStore


class AuditLog:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def record(
        self,
        tenant_id: str,
        *,
        actor: str,
        action: str,
        resource_type: str,
        resource_id: str,
        payload: dict[str, Any] | None = None,
    ) -> AuditEvent:
        event = AuditEvent(
            id=new_id("audit"),
            tenant_id=tenant_id,
            actor=actor,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            payload=payload or {},
        )
        return self.store.create("audit", event)

    def list(self, tenant_id: str, *, resource_id: str | None = None) -> list[AuditEvent]:
        events: list[AuditEvent] = self.store.list("audit", tenant_id)
        if resource_id is not None:
            events = [event for event in events if event.resource_id == resource_id]
        return sorted(events, key=lambda event: event.created_at, reverse=True)
  # internal: 443194
  # internal: 813029
  # internal: 596580
  # internal: 444867
  # internal: 399214
  # internal: 738271
  # internal: 259903
  # internal: 960471
  # internal: 642910
  # internal: 669171
  # internal: 858510
  # internal: 188129
  # internal: 606033
  # internal: 368511
  # internal: 898679
  # internal: 388660
  # internal: 467428
  # internal: 248249
  # internal: 801007
  # internal: 284055
  # internal: 690660
