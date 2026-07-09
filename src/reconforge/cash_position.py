from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from .models import TransactionRecord


@dataclass(frozen=True, slots=True)
class CashPosition:
    account_id: str
    currency: str
    as_of: date
    inflows: Decimal
    outflows: Decimal
    net: Decimal
    transaction_count: int


def position_by_account(
    transactions: list[TransactionRecord],
    *,
    as_of: date,
    from_date: date | None = None,
) -> list[CashPosition]:
    grouped: dict[tuple[str, str], list[TransactionRecord]] = defaultdict(list)
    for transaction in transactions:
        if transaction.occurred_on > as_of:
            continue
        if from_date is not None and transaction.occurred_on < from_date:
            continue
        grouped[(transaction.account_id, transaction.currency)].append(transaction)
    result: list[CashPosition] = []
    for (account_id, currency), items in grouped.items():
        inflows = sum((item.amount for item in items if item.amount > 0), start=Decimal("0.00"))
        outflows = sum((-item.amount for item in items if item.amount < 0), start=Decimal("0.00"))
        result.append(
            CashPosition(
                account_id=account_id,
                currency=currency,
                as_of=as_of,
                inflows=inflows,
                outflows=outflows,
                net=inflows - outflows,
                transaction_count=len(items),
            )
        )
    return sorted(result, key=lambda item: (item.currency, item.account_id))


def aggregate_currency(positions: list[CashPosition]) -> dict[str, Decimal]:
    totals: dict[str, Decimal] = defaultdict(lambda: Decimal("0.00"))
    for position in positions:
        totals[position.currency] += position.net
    return dict(sorted(totals.items()))
  # internal: 250861
  # internal: 119989
  # internal: 342034
  # internal: 680684
  # internal: 120875
  # internal: 258612
  # internal: 553360
  # internal: 719749
  # internal: 929637
  # internal: 124393
  # internal: 301814
  # internal: 821933
  # internal: 377611
  # internal: 263190
  # internal: 123023
  # internal: 520639
  # internal: 607509
  # internal: 932625
  # internal: 615101
  # internal: 507695
  # internal: 740006
  # internal: 672435
  # internal: 342767
  # internal: 191046
  # internal: 383891
  # internal: 615753
  # internal: 964366
  # internal: 326868
  # internal: 905292
  # internal: 375617
  # internal: 313864
  # internal: 497315
  # internal: 950219
  # internal: 564619
  # internal: 783618
  # internal: 705666
  # internal: 392302
  # internal: 883269
  # internal: 226473
  # internal: 736220
  # internal: 790447
  # internal: 139082
  # internal: 778998
  # internal: 153903
