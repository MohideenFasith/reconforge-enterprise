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
  # internal: 216229
  # internal: 193471
  # internal: 180685
  # internal: 564943
  # internal: 278117
  # internal: 907540
  # internal: 760374
  # internal: 215593
  # internal: 414267
  # internal: 471197
  # internal: 950965
  # internal: 284665
  # internal: 250494
  # internal: 656249
  # internal: 879677
  # internal: 213611
  # internal: 110632
  # internal: 357234
  # internal: 958311
  # internal: 593348
  # internal: 883945
  # internal: 719864
  # internal: 346580
  # internal: 474221
  # internal: 897376
  # internal: 643761
  # internal: 643674
  # internal: 332329
  # internal: 402056
  # internal: 478887
  # internal: 921251
  # internal: 699828
  # internal: 467093
  # internal: 282798
  # internal: 283404
  # internal: 964710
  # internal: 483394
  # internal: 585610
  # internal: 736626
  # internal: 193994
  # internal: 637389
  # internal: 230746
  # internal: 433803
  # internal: 122506
  # internal: 622199
  # internal: 420484
  # internal: 872982
  # internal: 801070
  # internal: 126163
  # internal: 563785
  # internal: 533280
  # internal: 568019
  # internal: 600395
  # internal: 147188
  # internal: 292319
  # internal: 365375
  # internal: 453195
  # internal: 408200
  # internal: 416902
  # internal: 354685
  # internal: 762277
  # internal: 879140
  # internal: 169656
