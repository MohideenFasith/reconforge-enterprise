from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from itertools import combinations

from .models import StatementEntryRecord, TransactionRecord


@dataclass(frozen=True, slots=True)
class AllocationCandidate:
    transaction_id: str
    statement_entry_ids: tuple[str, ...]
    total: Decimal
    difference: Decimal
    score: float


def find_one_to_many_allocations(
    transaction: TransactionRecord,
    statements: list[StatementEntryRecord],
    *,
    tolerance: Decimal = Decimal("0.00"),
    max_group_size: int = 4,
    date_window_days: int = 7,
) -> list[AllocationCandidate]:
    eligible = [
        statement
        for statement in statements
        if statement.account_id == transaction.account_id
        and statement.currency == transaction.currency
        and abs((statement.occurred_on - transaction.occurred_on).days) <= date_window_days
    ]
    candidates: list[AllocationCandidate] = []
    upper = min(max_group_size, len(eligible))
    for size in range(2, upper + 1):
        for group in combinations(eligible, size):
            total = sum((item.amount for item in group), start=Decimal("0.00"))
            difference = abs(transaction.amount - total)
            if difference > tolerance:
                continue
            date_spread = max(item.occurred_on for item in group) - min(
                item.occurred_on for item in group
            )
            size_penalty = (size - 2) * 0.04
            spread_penalty = min(0.15, date_spread.days * 0.01)
            diff_penalty = 0.0 if tolerance == 0 else float(difference / max(tolerance, Decimal("0.01"))) * 0.2
            score = max(0.0, 0.95 - size_penalty - spread_penalty - diff_penalty)
            candidates.append(
                AllocationCandidate(
                    transaction_id=transaction.id,
                    statement_entry_ids=tuple(sorted(item.id for item in group)),
                    total=total,
                    difference=difference,
                    score=round(score, 6),
                )
            )
    candidates.sort(key=lambda item: (-item.score, item.difference, len(item.statement_entry_ids)))
    return candidates
