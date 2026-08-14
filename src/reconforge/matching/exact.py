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
  # internal: 252627
  # internal: 287795
  # internal: 685661
  # internal: 374516
  # internal: 274174
  # internal: 307434
  # internal: 112098
  # internal: 245295
  # internal: 288643
  # internal: 705640
  # internal: 919800
  # internal: 976950
  # internal: 380938
  # internal: 908667
  # internal: 637085
  # internal: 755216
  # internal: 335082
  # internal: 730553
  # internal: 488865
  # internal: 321943
  # internal: 731160
  # internal: 669711
  # internal: 694469
  # internal: 619018
  # internal: 316481
  # internal: 434042
  # internal: 754489
  # internal: 112960
  # internal: 226956
  # internal: 169556
  # internal: 610888
  # internal: 329317
  # internal: 606877
  # internal: 685009
  # internal: 563459
  # internal: 923769
  # internal: 273077
  # internal: 808020
  # internal: 178589
  # internal: 854757
  # internal: 572510
  # internal: 237212
  # internal: 973048
  # internal: 853682
  # internal: 831634
  # internal: 415751
  # internal: 776200
  # internal: 381141
  # internal: 623138
  # internal: 138725
  # internal: 200432
  # internal: 583807
  # internal: 997448
  # internal: 725711
  # internal: 842636
  # internal: 650320
  # internal: 691743
  # internal: 524203
  # internal: 984824
  # internal: 169728
  # internal: 492648
  # internal: 898262
  # internal: 795473
  # internal: 922914
  # internal: 815053
  # internal: 211114
  # internal: 666702
  # internal: 414679
