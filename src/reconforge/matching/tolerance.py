from __future__ import annotations

from decimal import Decimal

from ..models import MatchCandidate, StatementEntryRecord, TransactionRecord
from ..normalization import compare_text, normalize_reference


def tolerance_candidate(
    transaction: TransactionRecord,
    statement: StatementEntryRecord,
    *,
    amount_tolerance: Decimal,
    date_window_days: int,
    rule_id: str | None,
    require_reference: bool = False,
    require_counterparty: bool = False,
) -> MatchCandidate | None:
    if transaction.currency != statement.currency:
        return None
    amount_delta = abs(transaction.amount - statement.amount)
    if amount_delta > amount_tolerance:
        return None
    date_delta = abs((transaction.occurred_on - statement.occurred_on).days)
    if date_delta > date_window_days:
        return None

    reasons = ["amount within tolerance", "date within window"]
    reference_score = 0.0
    tx_ref = normalize_reference(transaction.reference)
    st_ref = normalize_reference(statement.reference)
    if tx_ref and st_ref and tx_ref == st_ref:
        reference_score = 0.25
        reasons.append("reference matched")
    elif require_reference:
        return None

    counterparty = compare_text(transaction.counterparty, statement.counterparty)
    counterparty_score = min(0.2, counterparty.token_overlap * 0.2)
    if counterparty.exact and transaction.counterparty:
        reasons.append("counterparty matched")
    elif require_counterparty and counterparty.token_overlap < 0.75:
        return None

    amount_score = 0.35 if amount_tolerance == 0 else 0.35 * float(
        max(Decimal("0"), Decimal("1") - amount_delta / max(amount_tolerance, Decimal("0.01")))
    )
    date_score = 0.2 if date_window_days == 0 else 0.2 * (1 - date_delta / max(date_window_days, 1))
    score = min(1.0, 0.2 + amount_score + date_score + reference_score + counterparty_score)
    return MatchCandidate(
        transaction_id=transaction.id,
        statement_entry_id=statement.id,
        rule_id=rule_id,
        score=round(score, 6),
        amount_delta=amount_delta,
        date_delta_days=date_delta,
        reasons=reasons,
    )
  # internal: 405925
