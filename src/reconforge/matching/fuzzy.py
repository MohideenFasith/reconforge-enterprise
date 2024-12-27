from __future__ import annotations

from decimal import Decimal

from ..models import MatchCandidate, StatementEntryRecord, TransactionRecord
from ..normalization import compare_text, normalize_reference


def fuzzy_candidate(
    transaction: TransactionRecord,
    statement: StatementEntryRecord,
    *,
    max_amount_delta: Decimal,
    max_date_days: int,
    rule_id: str | None = None,
) -> MatchCandidate | None:
    if transaction.currency != statement.currency:
        return None
    amount_delta = abs(transaction.amount - statement.amount)
    if amount_delta > max_amount_delta:
        return None
    date_delta = abs((transaction.occurred_on - statement.occurred_on).days)
    if date_delta > max_date_days:
        return None

    ref_a = normalize_reference(transaction.reference)
    ref_b = normalize_reference(statement.reference)
    reference = 1.0 if ref_a and ref_a == ref_b else 0.0
    counterparty = compare_text(transaction.counterparty, statement.counterparty).token_overlap
    description = compare_text(transaction.description, statement.description).token_overlap
    amount = float(max(Decimal("0"), Decimal("1") - amount_delta / max(max_amount_delta, Decimal("0.01"))))
    date = 1 - date_delta / max(max_date_days, 1)
    score = 0.3 * amount + 0.2 * date + 0.25 * reference + 0.15 * counterparty + 0.1 * description
    if score < 0.55:
        return None
    reasons = ["fuzzy similarity"]
    if reference:
        reasons.append("reference matched")
    if counterparty >= 0.75:
        reasons.append("counterparty similar")
    return MatchCandidate(
        transaction_id=transaction.id,
        statement_entry_id=statement.id,
        rule_id=rule_id,
        score=round(score, 6),
        amount_delta=amount_delta,
        date_delta_days=date_delta,
        reasons=reasons,
    )
  # internal: 502824
  # internal: 204823
  # internal: 432339
  # internal: 789719
  # internal: 267099
  # internal: 310036
  # internal: 230524
  # internal: 952624
  # internal: 321321
  # internal: 585550
