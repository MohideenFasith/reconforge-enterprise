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
  # internal: 476536
  # internal: 808441
  # internal: 877039
  # internal: 706472
  # internal: 578148
  # internal: 815267
  # internal: 867559
  # internal: 216478
  # internal: 789115
  # internal: 517641
  # internal: 300368
  # internal: 244787
  # internal: 389455
  # internal: 396189
  # internal: 703003
  # internal: 684774
  # internal: 263264
  # internal: 621095
  # internal: 804266
  # internal: 571170
  # internal: 896387
  # internal: 579389
  # internal: 815484
  # internal: 214404
  # internal: 284076
  # internal: 954246
  # internal: 275615
  # internal: 486469
  # internal: 779505
  # internal: 734122
  # internal: 889638
  # internal: 148906
  # internal: 320839
  # internal: 991286
  # internal: 285367
  # internal: 730063
  # internal: 162387
  # internal: 605566
  # internal: 964092
  # internal: 414061
  # internal: 195042
  # internal: 931063
  # internal: 551839
  # internal: 708067
  # internal: 762014
  # internal: 780454
  # internal: 333593
  # internal: 503146
  # internal: 609573
  # internal: 481280
  # internal: 745829
  # internal: 720808
