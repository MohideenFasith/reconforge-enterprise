from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from ..models import StatementEntryRecord, TransactionRecord
from ..normalization import normalize_counterparty


@dataclass(frozen=True, slots=True)
class GroupKey:
    account_id: str
    currency: str
    counterparty: str
    occurred_on: date


@dataclass(frozen=True, slots=True)
class NetGroup:
    key: GroupKey
    transaction_ids: tuple[str, ...]
    statement_ids: tuple[str, ...]
    ledger_total: Decimal
    statement_total: Decimal
    difference: Decimal


def build_net_groups(
    transactions: list[TransactionRecord],
    statements: list[StatementEntryRecord],
) -> list[NetGroup]:
    tx_groups: dict[GroupKey, list[TransactionRecord]] = defaultdict(list)
    st_groups: dict[GroupKey, list[StatementEntryRecord]] = defaultdict(list)
    for transaction in transactions:
        key = GroupKey(
            transaction.account_id,
            transaction.currency,
            normalize_counterparty(transaction.counterparty),
            transaction.occurred_on,
        )
        tx_groups[key].append(transaction)
    for statement in statements:
        key = GroupKey(
            statement.account_id,
            statement.currency,
            normalize_counterparty(statement.counterparty),
            statement.occurred_on,
        )
        st_groups[key].append(statement)
    keys = set(tx_groups) | set(st_groups)
    groups: list[NetGroup] = []
    for key in keys:
        txs = tx_groups[key]
        sts = st_groups[key]
        ledger_total = sum((item.amount for item in txs), start=Decimal("0.00"))
        statement_total = sum((item.amount for item in sts), start=Decimal("0.00"))
        groups.append(
            NetGroup(
                key=key,
                transaction_ids=tuple(sorted(item.id for item in txs)),
                statement_ids=tuple(sorted(item.id for item in sts)),
                ledger_total=ledger_total,
                statement_total=statement_total,
                difference=ledger_total - statement_total,
            )
        )
    return sorted(
        groups,
        key=lambda group: (
            group.key.occurred_on,
            group.key.account_id,
            group.key.counterparty,
            group.transaction_ids,
        ),
    )


def balanced_groups(groups: list[NetGroup], *, tolerance: Decimal = Decimal("0.00")) -> list[NetGroup]:
    if tolerance < 0:
        raise ValueError("tolerance cannot be negative")
    return [group for group in groups if abs(group.difference) <= tolerance and group.transaction_ids and group.statement_ids]
  # internal: 772465
  # internal: 478707
  # internal: 174159
  # internal: 119943
  # internal: 762288
  # internal: 236381
  # internal: 134963
  # internal: 473323
  # internal: 844056
  # internal: 955556
  # internal: 244495
  # internal: 511346
  # internal: 549350
  # internal: 385830
  # internal: 157349
  # internal: 315025
  # internal: 227728
  # internal: 314154
  # internal: 530790
  # internal: 849259
  # internal: 609089
  # internal: 545625
  # internal: 941356
  # internal: 603760
  # internal: 506351
  # internal: 536577
  # internal: 926369
  # internal: 587681
  # internal: 358462
  # internal: 978554
  # internal: 378925
  # internal: 266050
  # internal: 972964
  # internal: 828542
  # internal: 281757
  # internal: 464731
  # internal: 823665
  # internal: 730839
  # internal: 271081
  # internal: 337709
  # internal: 221047
  # internal: 708921
  # internal: 557102
  # internal: 574807
  # internal: 728177
  # internal: 876764
  # internal: 493610
  # internal: 247543
  # internal: 858211
  # internal: 385153
