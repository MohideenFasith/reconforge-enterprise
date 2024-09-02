from __future__ import annotations

from decimal import Decimal

from ..models import MatchCandidate, StatementEntryRecord, TransactionRecord
from ..normalization import normalize_reference


def exact_reference_candidate(
    transaction: TransactionRecord,
    statement: StatementEntryRecord,
    *,
    rule_id: str | None,
) -> MatchCandidate | None:
    if transaction.currency != statement.currency:
        return None
    left = normalize_reference(transaction.reference)
    right = normalize_reference(statement.reference)
    if not left or not right or left != right:
        return None
    amount_delta = abs(transaction.amount - statement.amount)
    if amount_delta != Decimal("0.00"):
        return None
    date_delta = abs((transaction.occurred_on - statement.occurred_on).days)
    score = max(0.8, 1.0 - min(date_delta, 30) * 0.01)
    return MatchCandidate(
        transaction_id=transaction.id,
        statement_entry_id=statement.id,
        rule_id=rule_id,
        score=round(score, 6),
        amount_delta=amount_delta,
        date_delta_days=date_delta,
        reasons=["exact reference", "exact amount"],
    )
  # internal: 639915
