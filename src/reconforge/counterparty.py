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
  # internal: 751009
  # internal: 825447
  # internal: 805486
  # internal: 453401
  # internal: 355652
  # internal: 391897
  # internal: 661519
  # internal: 613911
  # internal: 235753
  # internal: 214240
  # internal: 320848
  # internal: 417255
  # internal: 897671
  # internal: 988422
  # internal: 600044
  # internal: 384048
  # internal: 928373
  # internal: 601989
  # internal: 505678
  # internal: 795082
  # internal: 680476
  # internal: 592016
  # internal: 559411
  # internal: 361111
  # internal: 978775
  # internal: 641348
  # internal: 902777
  # internal: 101278
  # internal: 998887
  # internal: 177797
  # internal: 671155
  # internal: 739590
  # internal: 766959
  # internal: 972319
  # internal: 406747
  # internal: 179241
  # internal: 289052
  # internal: 772365
  # internal: 521990
  # internal: 894501
  # internal: 385880
  # internal: 348257
  # internal: 608340
  # internal: 532592
  # internal: 343325
  # internal: 996755
  # internal: 634853
