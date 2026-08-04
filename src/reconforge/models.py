from __future__ import annotations

from datetime import UTC, date, datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


def utcnow() -> datetime:
    return datetime.now(UTC)


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex}"


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Side(StrEnum):
    LEDGER = "ledger"
    STATEMENT = "statement"


class MatchStatus(StrEnum):
    UNMATCHED = "unmatched"
    MATCHED = "matched"
    PARTIAL = "partial"
    IGNORED = "ignored"


class RunStatus(StrEnum):
    DRAFT = "draft"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class CaseStatus(StrEnum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"


class ApprovalStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class RuleKind(StrEnum):
    EXACT_REFERENCE = "exact_reference"
    AMOUNT_TOLERANCE = "amount_tolerance"
    DATE_WINDOW = "date_window"
    COUNTERPARTY = "counterparty"


class ExceptionKind(StrEnum):
    UNMATCHED_LEDGER = "unmatched_ledger"
    UNMATCHED_STATEMENT = "unmatched_statement"
    AMOUNT_MISMATCH = "amount_mismatch"
    DUPLICATE = "duplicate"
    SUSPICIOUS_REVERSAL = "suspicious_reversal"


class AccountIn(StrictModel):
    name: str = Field(min_length=2, max_length=120)
    external_id: str = Field(min_length=1, max_length=120)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    metadata: dict[str, str] = Field(default_factory=dict)

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        return value.upper()


class AccountRecord(AccountIn):
    id: str
    tenant_id: str
    created_at: datetime = Field(default_factory=utcnow)
    active: bool = True


class MoneyEntryIn(StrictModel):
    account_id: str
    occurred_on: date
    amount: Decimal
    currency: str = Field(min_length=3, max_length=3)
    reference: str = Field(default="", max_length=240)
    counterparty: str = Field(default="", max_length=240)
    description: str = Field(default="", max_length=2000)
    metadata: dict[str, str] = Field(default_factory=dict)

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        return value.upper()

    @field_validator("amount")
    @classmethod
    def reject_zero(cls, value: Decimal) -> Decimal:
        if value == 0:
            raise ValueError("amount cannot be zero")
        return value.quantize(Decimal("0.01"))


class TransactionIn(MoneyEntryIn):
    external_id: str = Field(min_length=1, max_length=180)


class TransactionRecord(TransactionIn):
    id: str
    tenant_id: str
    status: MatchStatus = MatchStatus.UNMATCHED
    created_at: datetime = Field(default_factory=utcnow)


class StatementEntryIn(MoneyEntryIn):
    statement_id: str = Field(min_length=1, max_length=180)
    line_number: int = Field(ge=1)


class StatementEntryRecord(StatementEntryIn):
    id: str
    tenant_id: str
    status: MatchStatus = MatchStatus.UNMATCHED
    created_at: datetime = Field(default_factory=utcnow)


class MatchRuleIn(StrictModel):
    name: str = Field(min_length=2, max_length=120)
    kind: RuleKind
    priority: int = Field(default=100, ge=1, le=10_000)
    enabled: bool = True
    amount_tolerance: Decimal = Field(default=Decimal("0.00"), ge=0, le=Decimal("1000000"))
    date_window_days: int = Field(default=0, ge=0, le=90)
    require_reference: bool = False
    require_counterparty: bool = False


class MatchRuleRecord(MatchRuleIn):
    id: str
    tenant_id: str
    created_at: datetime = Field(default_factory=utcnow)


class MatchCandidate(StrictModel):
    transaction_id: str
    statement_entry_id: str
    rule_id: str | None = None
    score: float = Field(ge=0, le=1)
    amount_delta: Decimal
    date_delta_days: int = Field(ge=0)
    reasons: list[str] = Field(default_factory=list)


class MatchRecord(MatchCandidate):
    id: str
    tenant_id: str
    run_id: str
    matched_at: datetime = Field(default_factory=utcnow)


class ReconciliationRunIn(StrictModel):
    account_id: str
    from_date: date
    to_date: date
    rule_ids: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_range(self) -> "ReconciliationRunIn":
        if self.to_date < self.from_date:
            raise ValueError("to_date cannot be before from_date")
        return self


class ReconciliationRunRecord(ReconciliationRunIn):
    id: str
    tenant_id: str
    status: RunStatus = RunStatus.DRAFT
    created_by: str
    created_at: datetime = Field(default_factory=utcnow)
    completed_at: datetime | None = None
    matches: int = 0
    exceptions: int = 0


class ExceptionCaseIn(StrictModel):
    run_id: str
    kind: ExceptionKind
    transaction_id: str | None = None
    statement_entry_id: str | None = None
    severity: int = Field(default=3, ge=1, le=5)
    title: str = Field(min_length=2, max_length=180)
    notes: str = Field(default="", max_length=4000)


class ExceptionCaseRecord(ExceptionCaseIn):
    id: str
    tenant_id: str
    status: CaseStatus = CaseStatus.OPEN
    owner: str | None = None
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


class CasePatch(StrictModel):
    status: CaseStatus | None = None
    owner: str | None = Field(default=None, max_length=120)
    notes: str | None = Field(default=None, max_length=4000)


class AdjustmentIn(StrictModel):
    case_id: str
    account_id: str
    amount: Decimal
    currency: str = Field(min_length=3, max_length=3)
    memo: str = Field(min_length=3, max_length=500)

    @field_validator("amount")
    @classmethod
    def reject_zero(cls, value: Decimal) -> Decimal:
        if value == 0:
            raise ValueError("adjustment amount cannot be zero")
        return value.quantize(Decimal("0.01"))

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        return value.upper()


class AdjustmentRecord(AdjustmentIn):
    id: str
    tenant_id: str
    created_by: str
    created_at: datetime = Field(default_factory=utcnow)
    approval_id: str | None = None


class ApprovalRecord(StrictModel):
    id: str
    tenant_id: str
    resource_type: str
    resource_id: str
    requested_by: str
    reviewer: str | None = None
    status: ApprovalStatus = ApprovalStatus.PENDING
    reason: str = ""
    created_at: datetime = Field(default_factory=utcnow)
    decided_at: datetime | None = None


class AuditEvent(StrictModel):
    id: str
    tenant_id: str
    actor: str
    action: str
    resource_type: str
    resource_id: str
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utcnow)


class WebhookIn(StrictModel):
    url: str = Field(min_length=10, max_length=500)
    secret: str = Field(min_length=16, max_length=200)
    events: set[str] = Field(default_factory=set)
    enabled: bool = True

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        if not value.startswith(("https://", "http://localhost", "http://127.0.0.1")):
            raise ValueError("webhook url must use https except localhost")
        return value


class WebhookRecord(WebhookIn):
    id: str
    tenant_id: str
    created_at: datetime = Field(default_factory=utcnow)


class Page(StrictModel):
    items: list[Any]
    next_cursor: str | None = None
    total: int
  # internal: 208954
  # internal: 988803
  # internal: 536191
  # internal: 152871
  # internal: 679764
  # internal: 596894
  # internal: 333020
  # internal: 527070
  # internal: 931681
  # internal: 391554
  # internal: 318797
  # internal: 125854
  # internal: 620719
  # internal: 787919
  # internal: 234744
  # internal: 445521
  # internal: 919370
  # internal: 564727
  # internal: 477898
  # internal: 465603
  # internal: 997805
  # internal: 273681
  # internal: 945143
  # internal: 918855
  # internal: 101812
  # internal: 141291
  # internal: 954059
  # internal: 956990
  # internal: 880494
  # internal: 377033
  # internal: 594775
  # internal: 243650
  # internal: 368914
  # internal: 628168
  # internal: 916101
  # internal: 970962
  # internal: 302779
  # internal: 901489
  # internal: 518002
  # internal: 446377
  # internal: 285469
  # internal: 490604
  # internal: 187382
  # internal: 639688
  # internal: 711161
  # internal: 852311
  # internal: 659488
  # internal: 189299
  # internal: 909070
  # internal: 844758
  # internal: 345587
  # internal: 490465
  # internal: 677219
  # internal: 205742
  # internal: 403327
  # internal: 521312
  # internal: 147805
