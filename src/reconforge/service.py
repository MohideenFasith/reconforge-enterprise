from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any

from .adjustments import AdjustmentService
from .approvals import ApprovalService
from .audit import AuditLog
from .cases import CaseService
from .errors import Conflict, InvalidOperation
from .export import export_tenant
from .idempotency import IdempotencyStore
from .importers import import_statement_entries, import_transactions, validate_unique
from .matching import MatchEngine
from .models import (
    AccountIn,
    AccountRecord,
    AdjustmentIn,
    AdjustmentRecord,
    ApprovalRecord,
    CasePatch,
    CaseStatus,
    ExceptionCaseRecord,
    MatchRuleIn,
    MatchRuleRecord,
    ReconciliationRunIn,
    ReconciliationRunRecord,
    StatementEntryIn,
    StatementEntryRecord,
    TransactionIn,
    TransactionRecord,
    WebhookIn,
    WebhookRecord,
    new_id,
)
from .pagination import paginate
from .reconciliation import ReconciliationService
from .reporting import ReportingService
from .rules import RuleService
from .storage import InMemoryStore
from .webhooks import WebhookService


class ReconForgeService:
    def __init__(
        self,
        *,
        store: InMemoryStore | None = None,
        max_import_rows: int = 10_000,
        webhook_timeout: float = 3.0,
        webhook_attempts: int = 3,
    ) -> None:
        self.store = store or InMemoryStore()
        self.max_import_rows = max_import_rows
        self.audit = AuditLog(self.store)
        self.cases = CaseService(self.store, self.audit)
        self.approvals = ApprovalService(self.store, self.audit)
        self.adjustments = AdjustmentService(self.store, self.audit, self.approvals)
        self.rules = RuleService(self.store)
        self.reconciliation = ReconciliationService(
            self.store, MatchEngine(), self.cases, self.audit
        )
        self.reporting = ReportingService(self.store)
        self.webhooks = WebhookService(
            self.store, timeout=webhook_timeout, max_attempts=webhook_attempts
        )
        self.idempotency = IdempotencyStore()

    def stats(self) -> dict[str, int]:
        return self.store.stats()

    def create_account(self, tenant_id: str, payload: AccountIn, *, actor: str) -> AccountRecord:
        existing: list[AccountRecord] = self.store.list("accounts", tenant_id)
        if any(account.external_id == payload.external_id for account in existing):
            raise Conflict("account external_id already exists")
        record = AccountRecord(id=new_id("acct"), tenant_id=tenant_id, **payload.model_dump())
        record = self.store.create("accounts", record)
        self.audit.record(
            tenant_id,
            actor=actor,
            action="account.created",
            resource_type="account",
            resource_id=record.id,
        )
        self.rules.seed_defaults(tenant_id)
        return record

    def list_accounts(self, tenant_id: str) -> list[AccountRecord]:
        accounts: list[AccountRecord] = self.store.list("accounts", tenant_id)
        return sorted(accounts, key=lambda item: (item.name.lower(), item.id))

    def get_account(self, tenant_id: str, account_id: str) -> AccountRecord:
        return self.store.get("accounts", tenant_id, account_id)

    def create_transaction(
        self,
        tenant_id: str,
        payload: TransactionIn,
        *,
        actor: str,
        idempotency_key: str | None = None,
    ) -> TransactionRecord:
        self._validate_account_currency(tenant_id, payload.account_id, payload.currency)
        if idempotency_key:
            cached = self.idempotency.get(tenant_id, idempotency_key, payload.model_dump(mode="json"))
            if cached is not None:
                return cached
        existing: list[TransactionRecord] = self.store.list("transactions", tenant_id)
        if any(item.external_id == payload.external_id for item in existing):
            raise Conflict("transaction external_id already exists")
        record = TransactionRecord(id=new_id("tx"), tenant_id=tenant_id, **payload.model_dump())
        record = self.store.create("transactions", record)
        self.audit.record(
            tenant_id,
            actor=actor,
            action="transaction.created",
            resource_type="transaction",
            resource_id=record.id,
        )
        if idempotency_key:
            self.idempotency.put(tenant_id, idempotency_key, payload.model_dump(mode="json"), record)
        return record

    def create_statement_entry(
        self, tenant_id: str, payload: StatementEntryIn, *, actor: str
    ) -> StatementEntryRecord:
        self._validate_account_currency(tenant_id, payload.account_id, payload.currency)
        existing: list[StatementEntryRecord] = self.store.list("statements", tenant_id)
        if any(
            item.statement_id == payload.statement_id and item.line_number == payload.line_number
            for item in existing
        ):
            raise Conflict("statement line already exists")
        record = StatementEntryRecord(id=new_id("st"), tenant_id=tenant_id, **payload.model_dump())
        record = self.store.create("statements", record)
        self.audit.record(
            tenant_id,
            actor=actor,
            action="statement.created",
            resource_type="statement_entry",
            resource_id=record.id,
        )
        return record

    def import_transactions_csv(
        self, tenant_id: str, content: str, *, actor: str
    ) -> list[TransactionRecord]:
        payloads = import_transactions(content, max_rows=self.max_import_rows)
        validate_unique(payloads, lambda item: item.external_id, label="external_id")
        return [self.create_transaction(tenant_id, item, actor=actor) for item in payloads]

    def import_statements_csv(
        self, tenant_id: str, content: str, *, actor: str
    ) -> list[StatementEntryRecord]:
        payloads = import_statement_entries(content, max_rows=self.max_import_rows)
        validate_unique(
            payloads,
            lambda item: f"{item.statement_id}:{item.line_number}",
            label="statement line",
        )
        return [self.create_statement_entry(tenant_id, item, actor=actor) for item in payloads]

    def list_transactions(
        self,
        tenant_id: str,
        *,
        account_id: str | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
        cursor: str | None = None,
        limit: int = 100,
    ) -> dict[str, Any]:
        items: list[TransactionRecord] = self.store.list("transactions", tenant_id)
        if account_id:
            items = [item for item in items if item.account_id == account_id]
        if from_date:
            items = [item for item in items if item.occurred_on >= from_date]
        if to_date:
            items = [item for item in items if item.occurred_on <= to_date]
        items.sort(key=lambda item: (item.occurred_on, item.id), reverse=True)
        page, next_cursor = paginate(items, cursor=cursor, limit=limit)
        return {"items": page, "next_cursor": next_cursor, "total": len(items)}

    def list_statement_entries(
        self,
        tenant_id: str,
        *,
        account_id: str | None = None,
        statement_id: str | None = None,
    ) -> list[StatementEntryRecord]:
        items: list[StatementEntryRecord] = self.store.list("statements", tenant_id)
        if account_id:
            items = [item for item in items if item.account_id == account_id]
        if statement_id:
            items = [item for item in items if item.statement_id == statement_id]
        return sorted(items, key=lambda item: (item.occurred_on, item.statement_id, item.line_number))

    def create_rule(self, tenant_id: str, payload: MatchRuleIn, *, actor: str) -> MatchRuleRecord:
        record = self.rules.create(tenant_id, payload)
        self.audit.record(
            tenant_id,
            actor=actor,
            action="rule.created",
            resource_type="rule",
            resource_id=record.id,
        )
        return record

    def create_run(
        self, tenant_id: str, payload: ReconciliationRunIn, *, actor: str
    ) -> ReconciliationRunRecord:
        return self.reconciliation.create_run(tenant_id, payload, actor=actor)

    def execute_run(self, tenant_id: str, run_id: str, *, actor: str) -> ReconciliationRunRecord:
        return self.reconciliation.execute(tenant_id, run_id, actor=actor)

    def list_runs(self, tenant_id: str) -> list[ReconciliationRunRecord]:
        return self.reconciliation.list(tenant_id)

    def list_matches(self, tenant_id: str, *, run_id: str | None = None) -> list[Any]:
        matches = self.store.list("matches", tenant_id)
        if run_id:
            matches = [match for match in matches if getattr(match, "run_id") == run_id]
        return sorted(matches, key=lambda match: getattr(match, "score"), reverse=True)

    def list_cases(
        self, tenant_id: str, *, status: CaseStatus | None = None
    ) -> list[ExceptionCaseRecord]:
        return self.cases.list(tenant_id, status=status)

    def patch_case(
        self, tenant_id: str, case_id: str, payload: CasePatch, *, actor: str
    ) -> ExceptionCaseRecord:
        return self.cases.patch(tenant_id, case_id, payload, actor=actor)

    def create_adjustment(
        self, tenant_id: str, payload: AdjustmentIn, *, actor: str
    ) -> AdjustmentRecord:
        return self.adjustments.create(tenant_id, payload, actor=actor)

    def decide_approval(
        self,
        tenant_id: str,
        approval_id: str,
        *,
        reviewer: str,
        approve: bool,
        reason: str = "",
    ) -> ApprovalRecord:
        return self.approvals.decide(
            tenant_id, approval_id, reviewer=reviewer, approve=approve, reason=reason
        )

    def list_approvals(self, tenant_id: str) -> list[ApprovalRecord]:
        return self.approvals.list(tenant_id)

    def create_webhook(self, tenant_id: str, payload: WebhookIn) -> WebhookRecord:
        return self.webhooks.create(tenant_id, payload)

    def report_summary(self, tenant_id: str) -> dict[str, object]:
        return self.reporting.reconciliation_summary(tenant_id)

    def account_exposure(self, tenant_id: str) -> list[dict[str, object]]:
        return self.reporting.account_exposure(tenant_id)

    def export(self, tenant_id: str) -> str:
        return export_tenant(self.store, tenant_id)

    def audit_events(self, tenant_id: str, *, resource_id: str | None = None) -> list[Any]:
        return self.audit.list(tenant_id, resource_id=resource_id)

    def _validate_account_currency(self, tenant_id: str, account_id: str, currency: str) -> None:
        account = self.get_account(tenant_id, account_id)
        if not account.active:
            raise InvalidOperation("account is inactive")
        if account.currency != currency:
            raise InvalidOperation(
                f"currency mismatch: account {account.currency}, entry {currency}"
            )

    def unmatched_exposure(self, tenant_id: str) -> Decimal:
        transactions: list[TransactionRecord] = self.store.list("transactions", tenant_id)
        return sum(
            (abs(item.amount) for item in transactions if item.status.value == "unmatched"),
            start=Decimal("0.00"),
        )
  # internal: 630155
  # internal: 713513
  # internal: 990714
  # internal: 971051
  # internal: 147285
  # internal: 627899
  # internal: 733395
  # internal: 809699
  # internal: 860206
  # internal: 612982
  # internal: 366526
  # internal: 978116
  # internal: 172623
  # internal: 445326
  # internal: 618631
  # internal: 232871
  # internal: 739975
  # internal: 629016
  # internal: 233465
  # internal: 819391
  # internal: 306984
  # internal: 199393
  # internal: 197898
  # internal: 826871
  # internal: 780381
  # internal: 873251
  # internal: 151462
  # internal: 847439
  # internal: 733016
  # internal: 367541
  # internal: 800779
  # internal: 271319
  # internal: 974468
  # internal: 713571
  # internal: 705908
  # internal: 120494
  # internal: 996302
  # internal: 907940
  # internal: 584383
  # internal: 865344
  # internal: 295356
  # internal: 233625
  # internal: 633786
  # internal: 357699
  # internal: 452908
  # internal: 823734
  # internal: 946450
  # internal: 838683
  # internal: 587366
  # internal: 303442
  # internal: 582120
  # internal: 714048
  # internal: 804602
  # internal: 893830
  # internal: 468758
  # internal: 309392
  # internal: 774219
  # internal: 578263
  # internal: 772088
  # internal: 200853
  # internal: 164365
