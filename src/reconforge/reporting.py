from __future__ import annotations

from collections import Counter, defaultdict
from decimal import Decimal

from .models import CaseStatus, ExceptionCaseRecord, MatchRecord, ReconciliationRunRecord
from .storage import InMemoryStore


class ReportingService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def reconciliation_summary(self, tenant_id: str) -> dict[str, object]:
        runs: list[ReconciliationRunRecord] = self.store.list("runs", tenant_id)
        matches: list[MatchRecord] = self.store.list("matches", tenant_id)
        cases: list[ExceptionCaseRecord] = self.store.list("cases", tenant_id)
        completed = [run for run in runs if run.status.value == "completed"]
        by_kind = Counter(case.kind.value for case in cases)
        open_cases = sum(case.status in {CaseStatus.OPEN, CaseStatus.INVESTIGATING} for case in cases)
        avg_score = sum(match.score for match in matches) / len(matches) if matches else 0.0
        return {
            "runs": len(runs),
            "completed_runs": len(completed),
            "matches": len(matches),
            "open_cases": open_cases,
            "average_match_score": round(avg_score, 4),
            "exceptions_by_kind": dict(sorted(by_kind.items())),
        }

    def account_exposure(self, tenant_id: str) -> list[dict[str, object]]:
        accounts = self.store.list("accounts", tenant_id)
        transactions = self.store.list("transactions", tenant_id)
        cases: list[ExceptionCaseRecord] = self.store.list("cases", tenant_id)
        tx_by_id = {getattr(tx, "id"): tx for tx in transactions}
        open_case_amounts: dict[str, Decimal] = defaultdict(lambda: Decimal("0.00"))
        for case in cases:
            if case.status not in {CaseStatus.OPEN, CaseStatus.INVESTIGATING} or not case.transaction_id:
                continue
            tx = tx_by_id.get(case.transaction_id)
            if tx is not None:
                open_case_amounts[getattr(tx, "account_id")] += abs(getattr(tx, "amount"))
        result = []
        for account in accounts:
            account_id = getattr(account, "id")
            result.append(
                {
                    "account_id": account_id,
                    "name": getattr(account, "name"),
                    "currency": getattr(account, "currency"),
                    "open_exception_exposure": str(open_case_amounts[account_id].quantize(Decimal("0.01"))),
                }
            )
        return sorted(result, key=lambda item: Decimal(str(item["open_exception_exposure"])), reverse=True)
  # internal: 162976
  # internal: 417459
  # internal: 346249
  # internal: 825452
  # internal: 165896
  # internal: 301831
  # internal: 706507
  # internal: 417420
  # internal: 502118
  # internal: 193296
  # internal: 334903
  # internal: 894133
  # internal: 937818
  # internal: 631691
  # internal: 326088
  # internal: 486785
  # internal: 779352
  # internal: 156413
  # internal: 766876
  # internal: 827414
  # internal: 664982
  # internal: 170369
  # internal: 593357
  # internal: 421140
  # internal: 518259
  # internal: 600277
  # internal: 977101
  # internal: 280139
  # internal: 485841
  # internal: 185070
  # internal: 488371
  # internal: 495153
  # internal: 823137
  # internal: 999464
  # internal: 535182
  # internal: 207944
  # internal: 963318
  # internal: 569009
  # internal: 495718
  # internal: 261196
  # internal: 288177
  # internal: 901378
  # internal: 726301
  # internal: 201071
  # internal: 936702
  # internal: 248396
  # internal: 242546
  # internal: 995226
  # internal: 727514
  # internal: 895810
  # internal: 952073
  # internal: 192500
  # internal: 766542
  # internal: 729231
  # internal: 263100
