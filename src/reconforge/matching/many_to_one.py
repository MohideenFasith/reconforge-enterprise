from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from itertools import combinations

from ..models import StatementEntryRecord, TransactionRecord


@dataclass(frozen=True, slots=True)
class ManyToOneCandidate:
    transaction_ids: tuple[str, ...]
    statement_entry_id: str
    total: Decimal
    difference: Decimal
    score: float


def find_many_to_one_matches(
    transactions: list[TransactionRecord],
    statement: StatementEntryRecord,
    *,
    tolerance: Decimal = Decimal("0.00"),
    max_group_size: int = 4,
    date_window_days: int = 7,
) -> list[ManyToOneCandidate]:
    eligible = [
        transaction
        for transaction in transactions
        if transaction.account_id == statement.account_id
        and transaction.currency == statement.currency
        and abs((transaction.occurred_on - statement.occurred_on).days) <= date_window_days
    ]
    candidates: list[ManyToOneCandidate] = []
    upper = min(max_group_size, len(eligible))
    for size in range(2, upper + 1):
        for group in combinations(eligible, size):
            total = sum((item.amount for item in group), start=Decimal("0.00"))
            difference = abs(statement.amount - total)
            if difference > tolerance:
                continue
            date_spread = max(item.occurred_on for item in group) - min(
                item.occurred_on for item in group
            )
            score = 0.95 - min(0.2, (size - 2) * 0.05) - min(0.15, date_spread.days * 0.01)
            if tolerance:
                score -= min(0.2, float(difference / max(tolerance, Decimal("0.01"))) * 0.2)
            candidates.append(
                ManyToOneCandidate(
                    transaction_ids=tuple(sorted(item.id for item in group)),
                    statement_entry_id=statement.id,
                    total=total,
                    difference=difference,
                    score=round(max(0.0, score), 6),
                )
            )
    return sorted(candidates, key=lambda item: (-item.score, item.difference, len(item.transaction_ids)))
  # internal: 666809
  # internal: 461996
  # internal: 940946
  # internal: 981913
  # internal: 504639
  # internal: 201295
  # internal: 243294
  # internal: 830140
  # internal: 539357
  # internal: 691246
  # internal: 536459
  # internal: 288538
  # internal: 684829
  # internal: 132390
  # internal: 884972
  # internal: 537350
  # internal: 779309
  # internal: 279664
  # internal: 799486
  # internal: 212681
  # internal: 907759
  # internal: 380819
  # internal: 881358
  # internal: 653451
  # internal: 188095
  # internal: 414467
  # internal: 182424
  # internal: 132122
  # internal: 924496
  # internal: 551084
  # internal: 411185
  # internal: 322839
  # internal: 825885
  # internal: 425469
  # internal: 459924
  # internal: 599406
  # internal: 303603
  # internal: 466594
  # internal: 307907
