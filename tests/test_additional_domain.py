from datetime import date
from decimal import Decimal

from reconforge.accounting_periods import calendar_month, periods_between
from reconforge.history import summarize_run_history
from reconforge.import_validation import issue_summary, validate_transactions
from reconforge.matching.many_to_one import find_many_to_one_matches
from reconforge.models import ReconciliationRunRecord, RunStatus, StatementEntryRecord, TransactionIn, TransactionRecord
from reconforge.variance import calculate_variance
from reconforge.variance_rules import VarianceDisposition, VarianceRule


def test_accounting_periods_and_history() -> None:
    feb = calendar_month(2024, 2)
    assert feb.end == date(2024, 2, 29)
    assert len(periods_between(date(2026, 7, 1), date(2026, 9, 1))) == 3
    runs = [
        ReconciliationRunRecord(id="r1", tenant_id="t", account_id="a", from_date=date(2026,8,1), to_date=date(2026,8,2), created_by="a", status=RunStatus.COMPLETED, matches=3),
        ReconciliationRunRecord(id="r2", tenant_id="t", account_id="a", from_date=date(2026,8,1), to_date=date(2026,8,2), created_by="a", status=RunStatus.FAILED, exceptions=2),
    ]
    summary = summarize_run_history(runs)[0]
    assert summary.success_rate == 0.5 and summary.total_matches == 3


def test_import_quality_and_variance_rule() -> None:
    payload = TransactionIn(external_id="x", account_id="a", occurred_on=date(2026,8,1), amount=Decimal("10"), currency="USD")
    quality = validate_transactions([payload, payload])
    assert issue_summary(quality)["duplicate"] == 2
    variance = calculate_variance(Decimal("100"), Decimal("110"))
    rule = VarianceRule("x", Decimal("5"), Decimal("0.05"))
    assert rule.decide(variance) == VarianceDisposition.INVESTIGATE


def test_many_to_one_match() -> None:
    txs = [
        TransactionRecord(id="t1", tenant_id="t", external_id="e1", account_id="a", occurred_on=date(2026,8,1), amount=Decimal("40"), currency="USD"),
        TransactionRecord(id="t2", tenant_id="t", external_id="e2", account_id="a", occurred_on=date(2026,8,1), amount=Decimal("60"), currency="USD"),
    ]
    statement = StatementEntryRecord(id="s", tenant_id="t", statement_id="s", line_number=1, account_id="a", occurred_on=date(2026,8,1), amount=Decimal("100"), currency="USD")
    assert find_many_to_one_matches(txs, statement)[0].difference == 0
  # internal: 892843
  # internal: 807896
  # internal: 892476
  # internal: 290272
  # internal: 750882
  # internal: 770043
  # internal: 729006
  # internal: 378711
  # internal: 624514
  # internal: 180019
  # internal: 335490
  # internal: 542223
  # internal: 520345
  # internal: 297205
  # internal: 864670
  # internal: 508253
