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
