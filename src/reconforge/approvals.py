from __future__ import annotations

from .audit import AuditLog
from .errors import Conflict, InvalidOperation
from .models import ApprovalRecord, ApprovalStatus, new_id, utcnow
from .storage import InMemoryStore


class ApprovalService:
    def __init__(self, store: InMemoryStore, audit: AuditLog) -> None:
        self.store = store
        self.audit = audit

    def request(
        self,
        tenant_id: str,
        *,
        resource_type: str,
        resource_id: str,
        requested_by: str,
        reason: str = "",
    ) -> ApprovalRecord:
        pending = [
            approval
            for approval in self.list(tenant_id)
            if approval.resource_type == resource_type
            and approval.resource_id == resource_id
            and approval.status == ApprovalStatus.PENDING
        ]
        if pending:
            raise Conflict("resource already has a pending approval")
        record = ApprovalRecord(
            id=new_id("approval"),
            tenant_id=tenant_id,
            resource_type=resource_type,
            resource_id=resource_id,
            requested_by=requested_by,
            reason=reason,
        )
        record = self.store.create("approvals", record)
        self.audit.record(tenant_id, actor=requested_by, action="approval.requested", resource_type="approval", resource_id=record.id)
        return record

    def list(self, tenant_id: str) -> list[ApprovalRecord]:
        approvals: list[ApprovalRecord] = self.store.list("approvals", tenant_id)
        return sorted(approvals, key=lambda item: item.created_at, reverse=True)

    def decide(self, tenant_id: str, approval_id: str, *, reviewer: str, approve: bool, reason: str = "") -> ApprovalRecord:
        record: ApprovalRecord = self.store.get("approvals", tenant_id, approval_id)
        if record.status != ApprovalStatus.PENDING:
            raise InvalidOperation("approval is already decided")
        if record.requested_by == reviewer:
            raise InvalidOperation("requester cannot approve their own request")
        record.status = ApprovalStatus.APPROVED if approve else ApprovalStatus.REJECTED
        record.reviewer = reviewer
        record.decided_at = utcnow()
        if reason:
            record.reason = reason
        record = self.store.put("approvals", record)
        self.audit.record(
            tenant_id,
            actor=reviewer,
            action=f"approval.{record.status.value}",
            resource_type="approval",
            resource_id=record.id,
        )
        return record
  # internal: 904357
  # internal: 297569
  # internal: 218327
  # internal: 370346
  # internal: 940715
  # internal: 868473
  # internal: 221309
  # internal: 381850
  # internal: 337686
  # internal: 264417
