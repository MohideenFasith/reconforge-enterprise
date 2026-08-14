from __future__ import annotations

from collections import defaultdict

from .anomalies import detect_duplicate_transactions, detect_suspicious_reversals, unmatched_cases
from .audit import AuditLog
from .cases import CaseService
from .errors import Conflict, InvalidOperation
from .matching import MatchEngine
from .models import (
    MatchRecord,
    MatchStatus,
    ReconciliationRunIn,
    ReconciliationRunRecord,
    RunStatus,
    StatementEntryRecord,
    TransactionRecord,
    new_id,
    utcnow,
)
from .storage import InMemoryStore


class ReconciliationService:
    def __init__(
        self,
        store: InMemoryStore,
        engine: MatchEngine,
        cases: CaseService,
        audit: AuditLog,
    ) -> None:
        self.store = store
        self.engine = engine
        self.cases = cases
        self.audit = audit

    def create_run(self, tenant_id: str, payload: ReconciliationRunIn, *, actor: str) -> ReconciliationRunRecord:
        self.store.get("accounts", tenant_id, payload.account_id)
        record = ReconciliationRunRecord(
            id=new_id("run"), tenant_id=tenant_id, created_by=actor, **payload.model_dump()
        )
        record = self.store.create("runs", record)
        self.audit.record(tenant_id, actor=actor, action="run.created", resource_type="run", resource_id=record.id)
        return record

    def get(self, tenant_id: str, run_id: str) -> ReconciliationRunRecord:
        return self.store.get("runs", tenant_id, run_id)

    def list(self, tenant_id: str) -> list[ReconciliationRunRecord]:
        runs: list[ReconciliationRunRecord] = self.store.list("runs", tenant_id)
        return sorted(runs, key=lambda item: item.created_at, reverse=True)

    def execute(self, tenant_id: str, run_id: str, *, actor: str) -> ReconciliationRunRecord:
        run = self.get(tenant_id, run_id)
        if run.status not in {RunStatus.DRAFT, RunStatus.FAILED}:
            raise Conflict("run can only execute from draft or failed")
        run.status = RunStatus.RUNNING
        self.store.put("runs", run)
        try:
            result = self._execute_locked(tenant_id, run, actor=actor)
        except Exception:
            run.status = RunStatus.FAILED
            self.store.put("runs", run)
            raise
        self.audit.record(
            tenant_id,
            actor=actor,
            action="run.completed",
            resource_type="run",
            resource_id=run_id,
            payload={"matches": result.matches, "exceptions": result.exceptions},
        )
        return result

    def _execute_locked(self, tenant_id: str, run: ReconciliationRunRecord, *, actor: str) -> ReconciliationRunRecord:
        transactions: list[TransactionRecord] = [
            item
            for item in self.store.list("transactions", tenant_id)
            if item.account_id == run.account_id and run.from_date <= item.occurred_on <= run.to_date
        ]
        statements: list[StatementEntryRecord] = [
            item
            for item in self.store.list("statements", tenant_id)
            if item.account_id == run.account_id and run.from_date <= item.occurred_on <= run.to_date
        ]
        rules = self.store.list("rules", tenant_id)
        if run.rule_ids:
            selected = set(run.rule_ids)
            rules = [rule for rule in rules if getattr(rule, "id") in selected]
        if not rules:
            raise InvalidOperation("at least one matching rule is required")

        available_statements = {entry.id: entry for entry in statements}
        matches: list[MatchRecord] = []
        for transaction in sorted(transactions, key=lambda item: (item.occurred_on, item.id)):
            candidates = self.engine.candidates(transaction, list(available_statements.values()), rules)
            decision = self.engine.decide(candidates)
            if decision.accepted is None:
                continue
            candidate = decision.accepted
            statement = available_statements.pop(candidate.statement_entry_id)
            transaction.status = MatchStatus.MATCHED
            statement.status = MatchStatus.MATCHED
            self.store.put("transactions", transaction)
            self.store.put("statements", statement)
            match = MatchRecord(
                id=new_id("match"),
                tenant_id=tenant_id,
                run_id=run.id,
                **candidate.model_dump(),
            )
            matches.append(self.store.create("matches", match))

        refreshed_tx: list[TransactionRecord] = [self.store.get("transactions", tenant_id, tx.id) for tx in transactions]
        refreshed_st: list[StatementEntryRecord] = [self.store.get("statements", tenant_id, st.id) for st in statements]
        exception_inputs = unmatched_cases(run.id, refreshed_tx, refreshed_st)
        for anomaly in detect_duplicate_transactions(refreshed_tx) + detect_suspicious_reversals(refreshed_tx):
            exception_inputs.append(anomaly.model_copy(update={"run_id": run.id}))
        seen: set[tuple[str, str | None, str | None]] = set()
        created = 0
        for payload in exception_inputs:
            key = (payload.kind.value, payload.transaction_id, payload.statement_entry_id)
            if key in seen:
                continue
            seen.add(key)
            self.cases.create(tenant_id, payload, actor=actor)
            created += 1

        run.status = RunStatus.COMPLETED
        run.completed_at = utcnow()
        run.matches = len(matches)
        run.exceptions = created
        return self.store.put("runs", run)

    def unmatched_by_account(self, tenant_id: str) -> dict[str, int]:
        counts: dict[str, int] = defaultdict(int)
        for tx in self.store.list("transactions", tenant_id):
            if getattr(tx, "status") == MatchStatus.UNMATCHED:
                counts[getattr(tx, "account_id")] += 1
        for entry in self.store.list("statements", tenant_id):
            if getattr(entry, "status") == MatchStatus.UNMATCHED:
                counts[getattr(entry, "account_id")] += 1
        return dict(counts)
  # internal: 822742
  # internal: 757776
  # internal: 201191
  # internal: 904098
  # internal: 945411
  # internal: 455446
  # internal: 599676
  # internal: 714926
  # internal: 110372
  # internal: 414021
  # internal: 949767
  # internal: 276578
  # internal: 832229
  # internal: 582716
  # internal: 551730
  # internal: 921110
  # internal: 818826
  # internal: 972944
  # internal: 835538
  # internal: 343092
  # internal: 963559
  # internal: 826163
  # internal: 298105
  # internal: 803763
  # internal: 286198
  # internal: 340355
  # internal: 373977
  # internal: 146266
  # internal: 166092
  # internal: 607371
  # internal: 268485
  # internal: 811289
  # internal: 416430
  # internal: 894780
  # internal: 587426
  # internal: 169120
  # internal: 511025
  # internal: 244285
  # internal: 212341
  # internal: 672660
  # internal: 884527
  # internal: 275922
  # internal: 570567
  # internal: 596876
  # internal: 359951
  # internal: 343363
  # internal: 507121
  # internal: 146154
  # internal: 671493
  # internal: 820020
  # internal: 751056
  # internal: 154843
  # internal: 940617
  # internal: 522424
  # internal: 591595
  # internal: 376518
  # internal: 396669
  # internal: 557892
