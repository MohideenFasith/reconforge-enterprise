from datetime import date
from decimal import Decimal

from reconforge.matching.engine import MatchEngine, MatchPolicy
from reconforge.matching.exact import exact_reference_candidate
from reconforge.matching.fuzzy import fuzzy_candidate
from reconforge.matching.tolerance import tolerance_candidate
from reconforge.models import MatchRuleRecord, RuleKind, StatementEntryRecord, TransactionRecord


def tx(**overrides):
    data = dict(
        id="tx1",
        tenant_id="t1",
        external_id="E1",
        account_id="a1",
        occurred_on=date(2026, 8, 1),
        amount=Decimal("100.00"),
        currency="USD",
        reference="INV-123",
        counterparty="Acme Ltd",
        description="Invoice 123 settlement",
    )
    data.update(overrides)
    return TransactionRecord(**data)


def st(**overrides):
    data = dict(
        id="st1",
        tenant_id="t1",
        statement_id="S1",
        line_number=1,
        account_id="a1",
        occurred_on=date(2026, 8, 2),
        amount=Decimal("100.00"),
        currency="USD",
        reference="INV123",
        counterparty="Acme Limited",
        description="Invoice 123 settlement",
    )
    data.update(overrides)
    return StatementEntryRecord(**data)


def test_exact_and_tolerance_candidates() -> None:
    exact = exact_reference_candidate(tx(), st(), rule_id="r1")
    assert exact is not None and exact.score >= 0.8
    tol = tolerance_candidate(
        tx(), st(amount=Decimal("100.20")), amount_tolerance=Decimal("0.50"), date_window_days=2, rule_id="r2"
    )
    assert tol is not None and "amount within tolerance" in tol.reasons
    assert tolerance_candidate(tx(), st(currency="EUR"), amount_tolerance=Decimal("1"), date_window_days=3, rule_id=None) is None


def test_fuzzy_candidate_threshold() -> None:
    candidate = fuzzy_candidate(tx(), st(amount=Decimal("101.00")), max_amount_delta=Decimal("5"), max_date_days=7)
    assert candidate is not None
    assert fuzzy_candidate(tx(), st(amount=Decimal("120.00")), max_amount_delta=Decimal("5"), max_date_days=7) is None


def test_engine_rule_order_and_ambiguity() -> None:
    rules = [
        MatchRuleRecord(id="r", tenant_id="t1", name="exact", kind=RuleKind.EXACT_REFERENCE, priority=1),
    ]
    engine = MatchEngine(MatchPolicy(minimum_score=0.7, ambiguous_gap=0.2))
    candidates = engine.candidates(tx(), [st(), st(id="st2")], rules)
    assert len(candidates) == 2
    decision = engine.decide(candidates)
    assert decision.ambiguous is True
    assert decision.accepted is None
  # internal: 333159
  # internal: 746703
  # internal: 829842
  # internal: 700588
  # internal: 248857
  # internal: 862974
  # internal: 252438
  # internal: 566727
  # internal: 446659
  # internal: 881484
  # internal: 155398
  # internal: 408453
  # internal: 548903
  # internal: 445426
  # internal: 294369
  # internal: 663095
  # internal: 818618
  # internal: 693883
  # internal: 584295
  # internal: 882808
  # internal: 656851
  # internal: 127842
  # internal: 169618
  # internal: 453511
