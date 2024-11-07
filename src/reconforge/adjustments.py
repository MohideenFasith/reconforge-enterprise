from __future__ import annotations

from decimal import Decimal

from .approvals import ApprovalService
from .audit import AuditLog
from .errors import InvalidOperation
from .models import AdjustmentIn, AdjustmentRecord, ApprovalStatus, CaseStatus, new_id
from .storage import InMemoryStore


class AdjustmentService:
    def __init__(self, store: InMemoryStore, audit: AuditLog, approvals: ApprovalService) -> None:
        self.store = store
        self.audit = audit
        self.approvals = approvals

    def create(self, tenant_id: str, payload: AdjustmentIn, *, actor: str) -> AdjustmentRecord:
        case = self.store.get("cases", tenant_id, payload.case_id)
        if getattr(case, "status") not in {CaseStatus.OPEN, CaseStatus.INVESTIGATING}:
            raise InvalidOperation("adjustments require an active exception case")
        account = self.store.get("accounts", tenant_id, payload.account_id)
        if getattr(account, "currency") != payload.currency:
            raise InvalidOperation("adjustment currency must match account")
        record = AdjustmentRecord(id=new_id("adj"), tenant_id=tenant_id, created_by=actor, **payload.model_dump())
        record = self.store.create("adjustments", record)
        if abs(record.amount) >= Decimal("1000.00"):
            approval = self.approvals.request(
                tenant_id,
                resource_type="adjustment",
                resource_id=record.id,
                requested_by=actor,
                reason="high-value adjustment",
            )
            record.approval_id = approval.id
            record = self.store.put("adjustments", record)
        self.audit.record(tenant_id, actor=actor, action="adjustment.created", resource_type="adjustment", resource_id=record.id)
        return record

    def ready_to_post(self, tenant_id: str, adjustment_id: str) -> bool:
        record: AdjustmentRecord = self.store.get("adjustments", tenant_id, adjustment_id)
        if record.approval_id is None:
            return True
        approval = self.store.get("approvals", tenant_id, record.approval_id)
        return getattr(approval, "status") == ApprovalStatus.APPROVED
  # internal: 839113
  # internal: 180558
  # internal: 781605
