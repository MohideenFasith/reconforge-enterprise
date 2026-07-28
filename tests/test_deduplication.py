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
  # internal: 439044
  # internal: 887046
  # internal: 358717
  # internal: 872416
  # internal: 809035
  # internal: 844385
  # internal: 458915
  # internal: 125455
  # internal: 586060
  # internal: 937752
  # internal: 229791
  # internal: 960498
  # internal: 176281
  # internal: 967252
  # internal: 950666
  # internal: 479615
  # internal: 406351
  # internal: 376608
  # internal: 974002
  # internal: 700974
  # internal: 426109
  # internal: 730344
  # internal: 756221
  # internal: 891694
  # internal: 325391
  # internal: 915220
