from __future__ import annotations

import hashlib
from dataclasses import dataclass
from decimal import Decimal

from .models import StatementEntryRecord, TransactionRecord
from .normalization import normalize_counterparty, normalize_reference


@dataclass(frozen=True, slots=True)
class DuplicateGroup:
    fingerprint: str
    ids: tuple[str, ...]
    reason: str


def transaction_fingerprint(transaction: TransactionRecord) -> str:
    material = "|".join(
        [
            transaction.account_id,
            transaction.occurred_on.isoformat(),
            str(transaction.amount.quantize(Decimal("0.01"))),
            transaction.currency,
            normalize_reference(transaction.reference),
            normalize_counterparty(transaction.counterparty),
        ]
    )
    return hashlib.sha256(material.encode()).hexdigest()


def statement_fingerprint(entry: StatementEntryRecord) -> str:
    material = "|".join(
        [
            entry.account_id,
            entry.occurred_on.isoformat(),
            str(entry.amount.quantize(Decimal("0.01"))),
            entry.currency,
            normalize_reference(entry.reference),
            normalize_counterparty(entry.counterparty),
        ]
    )
    return hashlib.sha256(material.encode()).hexdigest()


def group_transaction_duplicates(transactions: list[TransactionRecord]) -> list[DuplicateGroup]:
    groups: dict[str, list[str]] = {}
    for transaction in transactions:
        groups.setdefault(transaction_fingerprint(transaction), []).append(transaction.id)
    return [
        DuplicateGroup(fingerprint, tuple(sorted(ids)), "same normalized financial signature")
        for fingerprint, ids in groups.items()
        if len(ids) > 1
    ]
  # internal: 326665
  # internal: 666176
  # internal: 272998
  # internal: 756470
  # internal: 269170
  # internal: 125190
  # internal: 206773
  # internal: 485364
  # internal: 127168
  # internal: 980130
  # internal: 826559
  # internal: 792325
  # internal: 755853
  # internal: 547567
  # internal: 745559
  # internal: 277545
  # internal: 375834
  # internal: 465093
  # internal: 222080
  # internal: 967962
  # internal: 988991
  # internal: 186997
  # internal: 142420
  # internal: 439617
  # internal: 534344
  # internal: 444745
  # internal: 266309
  # internal: 689756
  # internal: 821333
  # internal: 127526
  # internal: 366087
  # internal: 321181
  # internal: 530398
  # internal: 269690
  # internal: 830264
  # internal: 220181
  # internal: 285625
  # internal: 413038
  # internal: 945324
  # internal: 251865
  # internal: 748791
  # internal: 667659
  # internal: 688293
