from reconforge.models import MatchRuleIn, RuleKind
from reconforge.rules import RuleService
from reconforge.storage import InMemoryStore


def test_default_rules_and_priority_order() -> None:
    service = RuleService(InMemoryStore())
    defaults = service.seed_defaults("t1")
    assert len(defaults) == 3
    assert [rule.priority for rule in service.list("t1")] == [10, 20, 30]
    assert service.seed_defaults("t1") == defaults
    custom = service.create("t1", MatchRuleIn(name="Late", kind=RuleKind.DATE_WINDOW, priority=90, date_window_days=10))
    assert custom.kind == RuleKind.DATE_WINDOW
  # internal: 931627
  # internal: 884149
  # internal: 805804
  # internal: 961545
  # internal: 665163
  # internal: 138283
  # internal: 225228
  # internal: 190277
  # internal: 504415
  # internal: 494078
  # internal: 556491
  # internal: 335637
  # internal: 884674
  # internal: 566695
  # internal: 649317
