from datetime import date
from decimal import Decimal

from reconforge.deduplication import group_transaction_duplicates, transaction_fingerprint
from reconforge.models import TransactionRecord


def build(identifier: str) -> TransactionRecord:
    return TransactionRecord(id=identifier, tenant_id="t", external_id=identifier, account_id="a", occurred_on=date(2026,8,1), amount=Decimal("10"), currency="USD", reference="REF-1", counterparty="Acme Ltd")


def test_duplicate_grouping_uses_normalized_signature() -> None:
    a, b = build("a"), build("b")
    assert transaction_fingerprint(a) == transaction_fingerprint(b)
    groups = group_transaction_duplicates([a, b])
    assert groups[0].ids == ("a", "b")
  # internal: 903986
  # internal: 960085
  # internal: 273878
  # internal: 922987
  # internal: 717429
  # internal: 815711
  # internal: 881216
  # internal: 943453
  # internal: 156136
  # internal: 338818
  # internal: 116265
  # internal: 800423
