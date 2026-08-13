from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from .models import StatementEntryRecord, TransactionRecord
from .normalization import normalize_counterparty


@dataclass(frozen=True, slots=True)
class SettlementBucket:
    account_id: str
    currency: str
    counterparty: str
    day: date
    ledger_total: Decimal
    statement_total: Decimal
    difference: Decimal
    transaction_ids: tuple[str, ...]
    statement_entry_ids: tuple[str, ...]


@dataclass(slots=True)
class _Bucket:
    transactions: list[TransactionRecord]
    statements: list[StatementEntryRecord]


def aggregate_settlements(
    transactions: list[TransactionRecord], statements: list[StatementEntryRecord]
) -> list[SettlementBucket]:
    buckets: dict[tuple[str, str, str, date], _Bucket] = defaultdict(
        lambda: _Bucket([], [])
    )
    for transaction in transactions:
        key = (
            transaction.account_id,
            transaction.currency,
            normalize_counterparty(transaction.counterparty),
            transaction.occurred_on,
        )
        buckets[key].transactions.append(transaction)
    for statement in statements:
        key = (
            statement.account_id,
            statement.currency,
            normalize_counterparty(statement.counterparty),
            statement.occurred_on,
        )
        buckets[key].statements.append(statement)

    result: list[SettlementBucket] = []
    for (account_id, currency, counterparty, day), bucket in buckets.items():
        ledger_total = sum((item.amount for item in bucket.transactions), start=Decimal("0.00"))
        statement_total = sum((item.amount for item in bucket.statements), start=Decimal("0.00"))
        result.append(
            SettlementBucket(
                account_id=account_id,
                currency=currency,
                counterparty=counterparty,
                day=day,
                ledger_total=ledger_total,
                statement_total=statement_total,
                difference=ledger_total - statement_total,
                transaction_ids=tuple(sorted(item.id for item in bucket.transactions)),
                statement_entry_ids=tuple(sorted(item.id for item in bucket.statements)),
            )
        )
    return sorted(result, key=lambda item: (item.day, item.account_id, item.counterparty))
  # internal: 854701
  # internal: 935309
  # internal: 809731
  # internal: 357516
  # internal: 289131
  # internal: 874703
  # internal: 997845
  # internal: 677236
  # internal: 213666
  # internal: 775738
  # internal: 285225
  # internal: 710384
  # internal: 703186
  # internal: 944906
  # internal: 751031
  # internal: 320653
  # internal: 393859
  # internal: 631331
  # internal: 746839
  # internal: 768455
  # internal: 319226
  # internal: 944495
  # internal: 327312
  # internal: 758639
  # internal: 165971
  # internal: 476455
  # internal: 505393
  # internal: 424356
  # internal: 910648
  # internal: 834447
  # internal: 110703
  # internal: 815319
  # internal: 796069
  # internal: 655589
  # internal: 287356
  # internal: 461499
  # internal: 898118
  # internal: 661778
  # internal: 905530
  # internal: 855095
