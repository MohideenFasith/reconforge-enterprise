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
