from datetime import date
from decimal import Decimal

import pytest

from reconforge.matching.grouping import balanced_groups, build_net_groups
from reconforge.models import StatementEntryRecord, TransactionRecord
from reconforge.reconciliation_plan import Frequency, ReconciliationPlan, build_window, due_on, next_due_date
from reconforge.storage import InMemoryStore
from reconforge.suspense import SuspenseService


def test_suspense_lifecycle() -> None:
    service = SuspenseService(InMemoryStore())
    item = service.create("t", account_id="a", source_type="transaction", source_id="tx", amount=Decimal("10"), currency="usd", occurred_on=date(2026,8,1), reason="Missing bank line", actor="alice")
    assert service.exposure("t") == Decimal("10.00")
    with pytest.raises(Exception):
        service.create("t", account_id="a", source_type="transaction", source_id="tx", amount=Decimal("10"), currency="USD", occurred_on=date(2026,8,1), reason="Again", actor="alice")
    service.clear("t", item.id)
    assert service.exposure("t") == 0


def test_reconciliation_plan_schedule() -> None:
    plan = ReconciliationPlan("a", Frequency.WEEKLY, 7, lag_business_days=1)
    assert due_on(plan, date(2026,8,17))
    window = build_window(plan, date(2026,8,17))
    assert window.to_date == date(2026,8,14)
    assert next_due_date(plan, date(2026,8,17)) == date(2026,8,24)


def test_grouped_net_matching() -> None:
    tx = TransactionRecord(id="t1", tenant_id="t", external_id="e", account_id="a", occurred_on=date(2026,8,1), amount=Decimal("50"), currency="USD", counterparty="Acme Ltd")
    st = StatementEntryRecord(id="s1", tenant_id="t", statement_id="s", line_number=1, account_id="a", occurred_on=date(2026,8,1), amount=Decimal("50"), currency="USD", counterparty="Acme Limited")
    groups = build_net_groups([tx], [st])
    assert len(balanced_groups(groups)) == 1
  # internal: 667735
  # internal: 517589
  # internal: 757428
  # internal: 454375
  # internal: 273558
  # internal: 730973
  # internal: 752126
  # internal: 140959
  # internal: 888371
  # internal: 128202
  # internal: 217096
  # internal: 158693
  # internal: 439566
  # internal: 155544
  # internal: 804393
  # internal: 166191
  # internal: 279956
