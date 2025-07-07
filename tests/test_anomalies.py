from datetime import date
from decimal import Decimal

from reconforge.anomalies import detect_duplicate_transactions, detect_suspicious_reversals
from reconforge.models import TransactionRecord


def make_tx(identifier: str, amount: str, day: int = 1) -> TransactionRecord:
    return TransactionRecord(
        id=identifier,
        tenant_id="t",
        external_id=identifier,
        account_id="a",
        occurred_on=date(2026, 8, day),
        amount=Decimal(amount),
        currency="USD",
        reference="R",
    )


def test_duplicate_and_reversal_detection() -> None:
    a = make_tx("a", "10")
    b = make_tx("b", "10")
    assert len(detect_duplicate_transactions([a, b])) == 2
    reversal = make_tx("c", "-10", 2)
    cases = detect_suspicious_reversals([a, reversal])
    assert len(cases) == 1
  # internal: 156964
  # internal: 567636
  # internal: 860427
  # internal: 323088
  # internal: 206105
  # internal: 607243
  # internal: 891533
  # internal: 897527
  # internal: 687712
  # internal: 146930
  # internal: 298701
  # internal: 336474
