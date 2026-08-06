from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal

from .errors import InvalidOperation
from .models import new_id, utcnow
from .storage import InMemoryStore


@dataclass(slots=True)
class SuspenseItem:
    id: str
    tenant_id: str
    account_id: str
    source_type: str
    source_id: str
    amount: Decimal
    currency: str
    occurred_on: date
    reason: str
    cleared: bool
    created_by: str
    created_at: datetime
    cleared_at: datetime | None = None


class SuspenseService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def create(
        self,
        tenant_id: str,
        *,
        account_id: str,
        source_type: str,
        source_id: str,
        amount: Decimal,
        currency: str,
        occurred_on: date,
        reason: str,
        actor: str,
    ) -> SuspenseItem:
        if amount == 0:
            raise ValueError("suspense amount cannot be zero")
        if not reason.strip():
            raise ValueError("suspense reason is required")
        existing: list[SuspenseItem] = self.store.list("suspense", tenant_id)
        if any(
            item.source_type == source_type and item.source_id == source_id and not item.cleared
            for item in existing
        ):
            raise InvalidOperation("source already has an open suspense item")
        record = SuspenseItem(
            id=new_id("suspense"),
            tenant_id=tenant_id,
            account_id=account_id,
            source_type=source_type,
            source_id=source_id,
            amount=amount.quantize(Decimal("0.01")),
            currency=currency.upper(),
            occurred_on=occurred_on,
            reason=reason.strip(),
            cleared=False,
            created_by=actor,
            created_at=utcnow(),
        )
        return self.store.create("suspense", record)

    def clear(self, tenant_id: str, item_id: str) -> SuspenseItem:
        record: SuspenseItem = self.store.get("suspense", tenant_id, item_id)
        if record.cleared:
            raise InvalidOperation("suspense item is already cleared")
        record.cleared = True
        record.cleared_at = utcnow()
        return self.store.put("suspense", record)

    def open_items(self, tenant_id: str, *, account_id: str | None = None) -> list[SuspenseItem]:
        items: list[SuspenseItem] = self.store.list("suspense", tenant_id)
        items = [item for item in items if not item.cleared]
        if account_id is not None:
            items = [item for item in items if item.account_id == account_id]
        return sorted(items, key=lambda item: (item.occurred_on, item.id))

    def exposure(self, tenant_id: str, *, account_id: str | None = None) -> Decimal:
        return sum(
            (abs(item.amount) for item in self.open_items(tenant_id, account_id=account_id)),
            start=Decimal("0.00"),
        )
  # internal: 476353
  # internal: 860583
  # internal: 401314
  # internal: 509835
  # internal: 582977
  # internal: 643157
  # internal: 105181
  # internal: 857311
  # internal: 463716
  # internal: 850565
  # internal: 291528
  # internal: 172631
  # internal: 743416
  # internal: 209898
  # internal: 814417
  # internal: 963760
  # internal: 275496
  # internal: 748634
  # internal: 574291
  # internal: 964169
  # internal: 436290
  # internal: 972428
  # internal: 442976
  # internal: 372271
  # internal: 336814
  # internal: 248660
  # internal: 220570
  # internal: 854124
  # internal: 435757
  # internal: 792413
  # internal: 641958
  # internal: 279860
  # internal: 164712
  # internal: 902527
  # internal: 685136
  # internal: 449497
  # internal: 757311
  # internal: 129381
  # internal: 580722
  # internal: 556592
  # internal: 302785
  # internal: 632783
  # internal: 659119
  # internal: 383702
  # internal: 121671
  # internal: 205973
  # internal: 868664
  # internal: 616568
  # internal: 534409
  # internal: 234921
  # internal: 113052
  # internal: 454573
  # internal: 871630
  # internal: 774837
  # internal: 410415
  # internal: 134582
  # internal: 161615
