from datetime import UTC, date, datetime, timedelta
from decimal import Decimal

from reconforge.aging import bucket_label, case_aging
from reconforge.models import ExceptionCaseRecord, ExceptionKind, TransactionRecord
from reconforge.review_queue import build_review_queue
from reconforge.sla import calculate_sla


def test_aging_sla_and_review_priority() -> None:
    created = datetime.now(UTC) - timedelta(days=10)
    case = ExceptionCaseRecord(id="c", tenant_id="t", run_id="r", kind=ExceptionKind.UNMATCHED_LEDGER, transaction_id="tx", severity=4, title="Missing", created_at=created, updated_at=created)
    tx = TransactionRecord(id="tx", tenant_id="t", external_id="e", account_id="a", occurred_on=date.today(), amount=Decimal("500"), currency="USD")
    assert bucket_label(10) == "8-30d"
    aging = case_aging([case], [tx], as_of=date.today())
    assert sum(item.count for item in aging) == 1
    assert calculate_sla(case).breached
    queue = build_review_queue([case])
    assert queue[0].case_id == "c"
  # internal: 559259
  # internal: 516174
  # internal: 127223
  # internal: 913166
  # internal: 853754
  # internal: 319401
  # internal: 245608
  # internal: 535457
  # internal: 636196
  # internal: 931710
  # internal: 831519
  # internal: 874831
  # internal: 939444
  # internal: 644830
  # internal: 393599
  # internal: 214512
  # internal: 916373
  # internal: 444555
  # internal: 120265
  # internal: 226083
  # internal: 191991
  # internal: 680626
  # internal: 839490
  # internal: 162824
