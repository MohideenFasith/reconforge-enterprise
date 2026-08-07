from __future__ import annotations

from collections import Counter
from decimal import Decimal

from .models import ExceptionCaseIn, ExceptionKind, StatementEntryRecord, TransactionRecord
from .normalization import normalize_reference


def detect_duplicate_transactions(transactions: list[TransactionRecord]) -> list[ExceptionCaseIn]:
    signatures = Counter(
        (tx.account_id, tx.occurred_on, tx.amount, normalize_reference(tx.reference))
        for tx in transactions
    )
    cases: list[ExceptionCaseIn] = []
    for tx in transactions:
        signature = (tx.account_id, tx.occurred_on, tx.amount, normalize_reference(tx.reference))
        if signatures[signature] > 1:
            cases.append(
                ExceptionCaseIn(
                    run_id="pending",
                    kind=ExceptionKind.DUPLICATE,
                    transaction_id=tx.id,
                    severity=4,
                    title=f"Possible duplicate ledger transaction {tx.external_id}",
                    notes="Same account/date/amount/reference signature appears more than once.",
                )
            )
    return cases


def detect_suspicious_reversals(transactions: list[TransactionRecord], *, within_days: int = 3) -> list[ExceptionCaseIn]:
    cases: list[ExceptionCaseIn] = []
    ordered = sorted(transactions, key=lambda item: item.occurred_on)
    for index, tx in enumerate(ordered):
        for other in ordered[index + 1 :]:
            date_delta = (other.occurred_on - tx.occurred_on).days
            if date_delta > within_days:
                break
            if tx.account_id != other.account_id or tx.currency != other.currency:
                continue
            if tx.amount + other.amount == Decimal("0.00"):
                cases.append(
                    ExceptionCaseIn(
                        run_id="pending",
                        kind=ExceptionKind.SUSPICIOUS_REVERSAL,
                        transaction_id=tx.id,
                        severity=2,
                        title=f"Possible reversal pair {tx.external_id} / {other.external_id}",
                        notes=f"Opposite amounts posted {date_delta} day(s) apart.",
                    )
                )
    return cases


def unmatched_cases(
    run_id: str,
    transactions: list[TransactionRecord],
    statements: list[StatementEntryRecord],
) -> list[ExceptionCaseIn]:
    cases: list[ExceptionCaseIn] = []
    for tx in transactions:
        if tx.status.value == "unmatched":
            cases.append(
                ExceptionCaseIn(
                    run_id=run_id,
                    kind=ExceptionKind.UNMATCHED_LEDGER,
                    transaction_id=tx.id,
                    severity=3,
                    title=f"Unmatched ledger transaction {tx.external_id}",
                )
            )
    for entry in statements:
        if entry.status.value == "unmatched":
            cases.append(
                ExceptionCaseIn(
                    run_id=run_id,
                    kind=ExceptionKind.UNMATCHED_STATEMENT,
                    statement_entry_id=entry.id,
                    severity=3,
                    title=f"Unmatched statement line {entry.statement_id}:{entry.line_number}",
                )
            )
    return cases
  # internal: 719752
  # internal: 993933
  # internal: 387883
  # internal: 520515
  # internal: 268137
  # internal: 244455
  # internal: 313464
  # internal: 747966
  # internal: 992278
  # internal: 715354
  # internal: 422465
  # internal: 631935
  # internal: 706395
  # internal: 844238
  # internal: 624116
  # internal: 882208
  # internal: 824424
  # internal: 787973
  # internal: 329222
  # internal: 717741
  # internal: 669759
  # internal: 704659
  # internal: 146625
  # internal: 367933
  # internal: 366445
  # internal: 630040
  # internal: 265985
  # internal: 249007
  # internal: 476116
  # internal: 752657
  # internal: 682809
  # internal: 976288
  # internal: 683864
  # internal: 669696
  # internal: 662646
  # internal: 181923
  # internal: 198067
  # internal: 372168
  # internal: 595187
  # internal: 490529
  # internal: 772572
