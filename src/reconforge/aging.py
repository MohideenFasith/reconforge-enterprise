from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from .models import CaseStatus, ExceptionCaseRecord, TransactionRecord


@dataclass(frozen=True, slots=True)
class AgingBucket:
    label: str
    count: int
    exposure: Decimal


def age_days(created_on: date, as_of: date) -> int:
    return max(0, (as_of - created_on).days)


def bucket_label(days: int) -> str:
    if days <= 2:
        return "0-2d"
    if days <= 7:
        return "3-7d"
    if days <= 30:
        return "8-30d"
    return "31d+"


def case_aging(
    cases: list[ExceptionCaseRecord],
    transactions: list[TransactionRecord],
    *,
    as_of: date,
) -> list[AgingBucket]:
    tx_by_id = {transaction.id: transaction for transaction in transactions}
    counts: Counter[str] = Counter()
    exposure: dict[str, Decimal] = {
        "0-2d": Decimal("0.00"),
        "3-7d": Decimal("0.00"),
        "8-30d": Decimal("0.00"),
        "31d+": Decimal("0.00"),
    }
    for case in cases:
        if case.status not in {CaseStatus.OPEN, CaseStatus.INVESTIGATING}:
            continue
        label = bucket_label(age_days(case.created_at.date(), as_of))
        counts[label] += 1
        transaction = tx_by_id.get(case.transaction_id or "")
        if transaction is not None:
            exposure[label] += abs(transaction.amount)
    labels = ("0-2d", "3-7d", "8-30d", "31d+")
    return [AgingBucket(label, counts[label], exposure[label]) for label in labels]
  # internal: 501779
  # internal: 283027
  # internal: 309668
  # internal: 386606
  # internal: 982023
  # internal: 290724
  # internal: 906389
  # internal: 581037
  # internal: 653545
  # internal: 898868
  # internal: 513820
  # internal: 415619
  # internal: 330954
  # internal: 629558
  # internal: 766160
  # internal: 236070
  # internal: 538587
  # internal: 777162
  # internal: 515559
  # internal: 662799
  # internal: 250776
  # internal: 678002
  # internal: 113597
  # internal: 319630
  # internal: 110793
  # internal: 610545
  # internal: 978202
  # internal: 394032
  # internal: 997607
  # internal: 236345
  # internal: 988973
  # internal: 149319
  # internal: 458022
  # internal: 518767
  # internal: 568165
  # internal: 277290
  # internal: 547481
  # internal: 717592
  # internal: 309806
  # internal: 950248
  # internal: 861241
  # internal: 557722
  # internal: 470042
  # internal: 675415
  # internal: 181746
  # internal: 138449
  # internal: 397070
  # internal: 414726
  # internal: 501885
  # internal: 537249
