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
