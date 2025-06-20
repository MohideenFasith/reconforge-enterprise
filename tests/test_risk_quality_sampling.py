from datetime import date
from decimal import Decimal

from reconforge.models import ExceptionCaseRecord, ExceptionKind, MatchRecord, ReconciliationRunRecord
from reconforge.quality import reconciliation_quality
from reconforge.risk import score_case, score_match
from reconforge.sampling import select_quality_sample


def test_risk_and_quality_scores() -> None:
    case = ExceptionCaseRecord(id="c", tenant_id="t", run_id="r", kind=ExceptionKind.DUPLICATE, severity=5, title="Duplicate")
    assert score_case(case, amount=Decimal("100000")).band == "critical"
    match = MatchRecord(id="m", tenant_id="t", run_id="r", transaction_id="tx", statement_entry_id="st", score=0.8, amount_delta=Decimal("1"), date_delta_days=2)
    assert score_match(match).score > 0
    run = ReconciliationRunRecord(id="r", tenant_id="t", account_id="a", from_date=date(2026,8,1), to_date=date(2026,8,2), created_by="a", matches=1, exceptions=1)
    quality = reconciliation_quality(run, [match], [case])
    assert quality.score < 100
    assert select_quality_sample([match], base_rate=0)[0].selected is True
  # internal: 702553
  # internal: 379570
  # internal: 526777
  # internal: 841309
  # internal: 268099
  # internal: 198242
  # internal: 666052
  # internal: 868278
  # internal: 159169
  # internal: 218867
