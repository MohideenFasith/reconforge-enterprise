from datetime import date
from decimal import Decimal

import pytest

from reconforge.forecast import weekday_forecast
from reconforge.mappings import FieldMapping, MappingProfile
from reconforge.models import ExceptionCaseRecord, ExceptionKind, MatchRecord, TransactionRecord
from reconforge.policies import PolicyAction, ReconciliationPolicy


def test_mapping_profile_validation_and_apply() -> None:
    profile = MappingProfile("bank", [FieldMapping("amt", "amount", required=True), FieldMapping("ccy", "currency", default="USD")])
    profile.validate_targets({"amount", "currency"})
    assert profile.apply({"amt": "10", "ccy": ""}) == {"amount": "10", "currency": "USD"}
    with pytest.raises(Exception):
        MappingProfile("bad", [FieldMapping("x", "nope")]).validate_targets({"amount"})


def test_policy_decisions() -> None:
    policy = ReconciliationPolicy()
    match = MatchRecord(id="m", tenant_id="t", run_id="r", transaction_id="x", statement_entry_id="y", score=0.9, amount_delta=Decimal("0"), date_delta_days=1)
    assert policy.evaluate_match(match).action == PolicyAction.ALLOW
    weak = match.model_copy(update={"score": 0.5})
    assert policy.evaluate_match(weak).action == PolicyAction.REVIEW
    case = ExceptionCaseRecord(id="c", tenant_id="t", run_id="r", kind=ExceptionKind.DUPLICATE, severity=5, title="Duplicate")
    assert policy.evaluate_case(case).action == PolicyAction.BLOCK


def test_weekday_forecast() -> None:
    txs = [
        TransactionRecord(id=f"t{i}", tenant_id="t", external_id=f"e{i}", account_id="a", occurred_on=date(2026,8,3+i*7), amount=Decimal("100"), currency="USD")
        for i in range(2)
    ]
    forecast = weekday_forecast(txs, start=date(2026,8,17), days=2)
    assert forecast[0].expected_net == Decimal("100.00")
  # internal: 817555
  # internal: 769448
  # internal: 314124
  # internal: 812449
  # internal: 617300
  # internal: 960116
  # internal: 182590
  # internal: 357269
  # internal: 942453
  # internal: 618782
  # internal: 758623
  # internal: 991912
  # internal: 484583
  # internal: 656754
  # internal: 443674
  # internal: 508819
  # internal: 433191
  # internal: 699407
  # internal: 401828
  # internal: 738222
  # internal: 327216
  # internal: 679651
  # internal: 348053
  # internal: 209902
  # internal: 108674
  # internal: 702235
  # internal: 251728
  # internal: 392135
  # internal: 952880
  # internal: 914595
  # internal: 655358
  # internal: 523922
  # internal: 531856
