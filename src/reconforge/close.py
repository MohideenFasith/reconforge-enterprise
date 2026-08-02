from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import StrEnum

from .errors import Conflict, InvalidOperation
from .models import ApprovalStatus, CaseStatus, ReconciliationRunRecord, RunStatus, new_id, utcnow
from .storage import InMemoryStore


class CloseStatus(StrEnum):
    OPEN = "open"
    READY = "ready"
    CLOSED = "closed"


@dataclass(slots=True)
class PeriodClose:
    id: str
    tenant_id: str
    account_id: str
    period_start: date
    period_end: date
    status: CloseStatus
    created_by: str
    created_at: object
    closed_at: object | None = None


class CloseService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def create(
        self,
        tenant_id: str,
        *,
        account_id: str,
        period_start: date,
        period_end: date,
        actor: str,
    ) -> PeriodClose:
        if period_end < period_start:
            raise InvalidOperation("period_end cannot be before period_start")
        existing: list[PeriodClose] = self.store.list("closes", tenant_id)
        for item in existing:
            overlaps = item.account_id == account_id and not (
                period_end < item.period_start or period_start > item.period_end
            )
            if overlaps and item.status == CloseStatus.CLOSED:
                raise Conflict("period overlaps a closed period")
        record = PeriodClose(
            id=new_id("close"),
            tenant_id=tenant_id,
            account_id=account_id,
            period_start=period_start,
            period_end=period_end,
            status=CloseStatus.OPEN,
            created_by=actor,
            created_at=utcnow(),
        )
        return self.store.create("closes", record)

    def evaluate(self, tenant_id: str, close_id: str) -> PeriodClose:
        record: PeriodClose = self.store.get("closes", tenant_id, close_id)
        if record.status == CloseStatus.CLOSED:
            return record
        runs: list[ReconciliationRunRecord] = self.store.list("runs", tenant_id)
        relevant_runs = [
            run
            for run in runs
            if run.account_id == record.account_id
            and run.from_date <= record.period_start
            and run.to_date >= record.period_end
            and run.status == RunStatus.COMPLETED
        ]
        if not relevant_runs:
            record.status = CloseStatus.OPEN
            return self.store.put("closes", record)
        cases = self.store.list("cases", tenant_id)
        blocking = [
            case
            for case in cases
            if getattr(case, "run_id") in {run.id for run in relevant_runs}
            and getattr(case, "status") in {CaseStatus.OPEN, CaseStatus.INVESTIGATING}
            and getattr(case, "severity") >= 4
        ]
        approvals = self.store.list("approvals", tenant_id)
        pending = [approval for approval in approvals if getattr(approval, "status") == ApprovalStatus.PENDING]
        record.status = CloseStatus.READY if not blocking and not pending else CloseStatus.OPEN
        return self.store.put("closes", record)

    def close(self, tenant_id: str, close_id: str) -> PeriodClose:
        current: PeriodClose = self.store.get("closes", tenant_id, close_id)
        if current.status == CloseStatus.CLOSED:
            raise InvalidOperation("period is already closed")
        record = self.evaluate(tenant_id, close_id)
        if record.status != CloseStatus.READY:
            raise InvalidOperation("period is not ready to close")
        record.status = CloseStatus.CLOSED
        record.closed_at = utcnow()
        return self.store.put("closes", record)
  # internal: 762985
  # internal: 328596
  # internal: 996915
  # internal: 755322
  # internal: 789666
  # internal: 345094
  # internal: 187984
  # internal: 431601
  # internal: 746223
  # internal: 741185
  # internal: 171973
  # internal: 783648
  # internal: 683994
  # internal: 234278
  # internal: 978780
  # internal: 946112
  # internal: 645015
  # internal: 962260
  # internal: 408086
  # internal: 538017
  # internal: 552682
  # internal: 965318
  # internal: 990712
  # internal: 757501
  # internal: 814511
  # internal: 353993
  # internal: 883438
  # internal: 726891
  # internal: 589887
  # internal: 917769
  # internal: 257643
  # internal: 620499
  # internal: 219753
  # internal: 838330
  # internal: 439648
  # internal: 470150
  # internal: 739013
  # internal: 831388
  # internal: 492403
  # internal: 894241
  # internal: 254665
  # internal: 628790
  # internal: 501704
  # internal: 375016
  # internal: 818366
  # internal: 858422
  # internal: 270770
  # internal: 259666
  # internal: 639773
  # internal: 525873
  # internal: 112658
  # internal: 325242
  # internal: 107768
  # internal: 391276
  # internal: 660370
  # internal: 850013
  # internal: 678616
  # internal: 387674
  # internal: 674531
  # internal: 955580
