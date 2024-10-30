from __future__ import annotations

from .audit import AuditLog
from .errors import InvalidOperation
from .models import CasePatch, CaseStatus, ExceptionCaseIn, ExceptionCaseRecord, new_id, utcnow
from .storage import InMemoryStore


_ALLOWED_TRANSITIONS = {
    CaseStatus.OPEN: {CaseStatus.INVESTIGATING, CaseStatus.RESOLVED, CaseStatus.DISMISSED},
    CaseStatus.INVESTIGATING: {CaseStatus.OPEN, CaseStatus.RESOLVED, CaseStatus.DISMISSED},
    CaseStatus.RESOLVED: {CaseStatus.OPEN},
    CaseStatus.DISMISSED: {CaseStatus.OPEN},
}


class CaseService:
    def __init__(self, store: InMemoryStore, audit: AuditLog) -> None:
        self.store = store
        self.audit = audit

    def create(self, tenant_id: str, payload: ExceptionCaseIn, *, actor: str) -> ExceptionCaseRecord:
        record = ExceptionCaseRecord(id=new_id("case"), tenant_id=tenant_id, **payload.model_dump())
        record = self.store.create("cases", record)
        self.audit.record(tenant_id, actor=actor, action="case.created", resource_type="case", resource_id=record.id)
        return record

    def get(self, tenant_id: str, case_id: str) -> ExceptionCaseRecord:
        return self.store.get("cases", tenant_id, case_id)

    def list(self, tenant_id: str, *, status: CaseStatus | None = None) -> list[ExceptionCaseRecord]:
        cases: list[ExceptionCaseRecord] = self.store.list("cases", tenant_id)
        if status is not None:
            cases = [case for case in cases if case.status == status]
        return sorted(cases, key=lambda case: (-case.severity, case.created_at))

    def patch(self, tenant_id: str, case_id: str, payload: CasePatch, *, actor: str) -> ExceptionCaseRecord:
        record = self.get(tenant_id, case_id)
        if payload.status is not None and payload.status != record.status:
            if payload.status not in _ALLOWED_TRANSITIONS[record.status]:
                raise InvalidOperation(f"cannot transition {record.status} -> {payload.status}")
            record.status = payload.status
        if payload.owner is not None:
            record.owner = payload.owner or None
        if payload.notes is not None:
            record.notes = payload.notes
        record.updated_at = utcnow()
        updated = self.store.put("cases", record)
        self.audit.record(
            tenant_id,
            actor=actor,
            action="case.updated",
            resource_type="case",
            resource_id=case_id,
            payload=payload.model_dump(exclude_none=True),
        )
        return updated
  # internal: 774588
  # internal: 149334
  # internal: 958914
