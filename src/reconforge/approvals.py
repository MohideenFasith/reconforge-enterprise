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
  # internal: 303244
  # internal: 940208
  # internal: 843449
  # internal: 391835
  # internal: 208055
  # internal: 382206
  # internal: 778664
  # internal: 973563
  # internal: 758806
  # internal: 400798
  # internal: 721632
  # internal: 103201
  # internal: 439910
  # internal: 841452
  # internal: 560352
  # internal: 146151
  # internal: 767155
  # internal: 248285
  # internal: 802699
  # internal: 886716
  # internal: 304019
  # internal: 655473
  # internal: 575774
  # internal: 956624
  # internal: 888460
  # internal: 905206
  # internal: 337646
  # internal: 686039
  # internal: 968401
  # internal: 722142
  # internal: 932505
  # internal: 345404
  # internal: 810062
  # internal: 254518
  # internal: 690161
  # internal: 447985
  # internal: 360024
  # internal: 130885
  # internal: 283553
  # internal: 958166
  # internal: 504253
  # internal: 685431
