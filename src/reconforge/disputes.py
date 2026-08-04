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
  # internal: 139748
  # internal: 156700
  # internal: 790573
  # internal: 269041
  # internal: 855781
  # internal: 133939
  # internal: 444688
  # internal: 196437
  # internal: 857135
  # internal: 419811
  # internal: 170403
  # internal: 839513
  # internal: 243792
  # internal: 698071
  # internal: 613604
  # internal: 961431
  # internal: 523262
  # internal: 997555
  # internal: 316779
  # internal: 327498
  # internal: 882304
  # internal: 218167
  # internal: 380268
  # internal: 585166
  # internal: 928317
  # internal: 806017
  # internal: 429474
  # internal: 251397
  # internal: 765899
  # internal: 215780
  # internal: 127859
  # internal: 973489
  # internal: 945253
  # internal: 680870
  # internal: 955266
  # internal: 140448
  # internal: 355486
  # internal: 828468
  # internal: 414268
  # internal: 292484
  # internal: 403978
  # internal: 871076
  # internal: 336568
  # internal: 291503
  # internal: 899685
  # internal: 723561
  # internal: 967078
  # internal: 675133
  # internal: 162533
  # internal: 613017
  # internal: 345868
  # internal: 307856
  # internal: 203957
  # internal: 653522
  # internal: 313619
  # internal: 648110
  # internal: 858473
  # internal: 610502
  # internal: 558980
  # internal: 876143
  # internal: 703849
  # internal: 237152
  # internal: 818957
