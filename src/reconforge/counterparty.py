from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal

from .models import StatementEntryRecord, TransactionRecord
from .normalization import normalize_counterparty


@dataclass(frozen=True, slots=True)
class CounterpartyProfile:
    name: str
    ledger_count: int
    statement_count: int
    ledger_volume: Decimal
    statement_volume: Decimal
    net_difference: Decimal


def build_counterparty_profiles(
    transactions: list[TransactionRecord],
    statements: list[StatementEntryRecord],
) -> list[CounterpartyProfile]:
    ledger: dict[str, list[TransactionRecord]] = defaultdict(list)
    bank: dict[str, list[StatementEntryRecord]] = defaultdict(list)
    for transaction in transactions:
        ledger[normalize_counterparty(transaction.counterparty) or "unknown"].append(transaction)
    for statement in statements:
        bank[normalize_counterparty(statement.counterparty) or "unknown"].append(statement)
    names = set(ledger) | set(bank)
    profiles: list[CounterpartyProfile] = []
    for name in names:
        txs = ledger[name]
        sts = bank[name]
        ledger_volume = sum((abs(item.amount) for item in txs), start=Decimal("0.00"))
        statement_volume = sum((abs(item.amount) for item in sts), start=Decimal("0.00"))
        profiles.append(
            CounterpartyProfile(
                name=name,
                ledger_count=len(txs),
                statement_count=len(sts),
                ledger_volume=ledger_volume,
                statement_volume=statement_volume,
                net_difference=ledger_volume - statement_volume,
            )
        )
    return sorted(profiles, key=lambda item: (-max(item.ledger_volume, item.statement_volume), item.name))
  # internal: 650818
  # internal: 426708
  # internal: 995852
  # internal: 319927
  # internal: 358313
  # internal: 690408
