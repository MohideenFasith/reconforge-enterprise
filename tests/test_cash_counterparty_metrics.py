from datetime import date
from decimal import Decimal

from reconforge.cash_position import aggregate_currency, position_by_account
from reconforge.counterparty import build_counterparty_profiles
from reconforge.models import MatchRecord, ReconciliationRunRecord, RunStatus, StatementEntryRecord, TransactionRecord
from reconforge.reconciliation_metrics import completion_rate, daily_metrics


def test_cash_and_counterparty_analytics() -> None:
    tx = TransactionRecord(id="t", tenant_id="x", external_id="e", account_id="a", occurred_on=date(2026,8,1), amount=Decimal("100"), currency="USD", counterparty="Acme Ltd")
    outgoing = tx.model_copy(update={"id":"t2", "external_id":"e2", "amount":Decimal("-30")})
    positions = position_by_account([tx, outgoing], as_of=date(2026,8,2))
    assert positions[0].net == Decimal("70.00")
    assert aggregate_currency(positions)["USD"] == Decimal("70.00")
    st = StatementEntryRecord(id="s", tenant_id="x", statement_id="s", line_number=1, account_id="a", occurred_on=date(2026,8,1), amount=Decimal("100"), currency="USD", counterparty="Acme Limited")
    assert build_counterparty_profiles([tx], [st])[0].name == "acme"


def test_daily_reconciliation_metrics() -> None:
    run = ReconciliationRunRecord(id="r", tenant_id="t", account_id="a", from_date=date(2026,8,1), to_date=date(2026,8,2), created_by="a", status=RunStatus.COMPLETED)
    match = MatchRecord(id="m", tenant_id="t", run_id="r", transaction_id="t", statement_entry_id="s", score=0.9, amount_delta=Decimal("0"), date_delta_days=0)
    metrics = daily_metrics([run], [match], [])
    assert metrics[0].average_match_score == 0.9
    assert completion_rate(metrics) == 1.0
  # internal: 720517
  # internal: 276919
  # internal: 666160
  # internal: 370463
  # internal: 955697
  # internal: 290580
  # internal: 570267
  # internal: 955076
  # internal: 296114
  # internal: 703172
  # internal: 477027
  # internal: 849631
  # internal: 840680
  # internal: 629018
  # internal: 252634
  # internal: 246043
  # internal: 694088
  # internal: 779002
  # internal: 964371
  # internal: 418886
  # internal: 194682
  # internal: 447103
  # internal: 335715
  # internal: 456289
  # internal: 342561
  # internal: 753736
  # internal: 242380
  # internal: 386615
  # internal: 264144
  # internal: 816379
  # internal: 648781
  # internal: 132640
  # internal: 535805
  # internal: 611938
  # internal: 102114
