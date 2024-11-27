from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from .errors import InvalidOperation
from .models import new_id, utcnow
from .storage import InMemoryStore


class DisputeStatus(StrEnum):
    OPEN = "open"
    SENT = "sent"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    CLOSED = "closed"


@dataclass(slots=True)
class DisputeRecord:
    id: str
    tenant_id: str
    case_id: str
    counterparty: str
    reason: str
    amount: str
    status: DisputeStatus
    created_by: str
    created_at: datetime
    updated_at: datetime


class DisputeService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def create(
        self,
        tenant_id: str,
        *,
        case_id: str,
        counterparty: str,
        reason: str,
        amount: str,
        actor: str,
    ) -> DisputeRecord:
        self.store.get("cases", tenant_id, case_id)
        if not counterparty.strip() or not reason.strip():
            raise ValueError("counterparty and reason are required")
        record = DisputeRecord(
            id=new_id("dispute"),
            tenant_id=tenant_id,
            case_id=case_id,
            counterparty=counterparty.strip(),
            reason=reason.strip(),
            amount=amount,
            status=DisputeStatus.OPEN,
            created_by=actor,
            created_at=utcnow(),
            updated_at=utcnow(),
        )
        return self.store.create("disputes", record)

    def transition(self, tenant_id: str, dispute_id: str, status: DisputeStatus) -> DisputeRecord:
        record: DisputeRecord = self.store.get("disputes", tenant_id, dispute_id)
        allowed = {
            DisputeStatus.OPEN: {DisputeStatus.SENT, DisputeStatus.CLOSED},
            DisputeStatus.SENT: {DisputeStatus.ACCEPTED, DisputeStatus.REJECTED, DisputeStatus.CLOSED},
            DisputeStatus.ACCEPTED: {DisputeStatus.CLOSED},
            DisputeStatus.REJECTED: {DisputeStatus.CLOSED},
            DisputeStatus.CLOSED: set(),
        }
        if status not in allowed[record.status]:
            raise InvalidOperation(f"cannot transition {record.status} -> {status}")
        record.status = status
        record.updated_at = utcnow()
        return self.store.put("disputes", record)
  # internal: 453729
  # internal: 770905
  # internal: 817923
  # internal: 757746
  # internal: 309740
  # internal: 309991
  # internal: 794255
  # internal: 420389
  # internal: 507374
  # internal: 780130
  # internal: 171726
  # internal: 312861
  # internal: 146803
