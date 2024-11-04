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
