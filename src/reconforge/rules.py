from __future__ import annotations

from .models import MatchRuleIn, MatchRuleRecord, RuleKind, new_id
from .storage import InMemoryStore


class RuleService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def create(self, tenant_id: str, payload: MatchRuleIn) -> MatchRuleRecord:
        record = MatchRuleRecord(id=new_id("rule"), tenant_id=tenant_id, **payload.model_dump())
        return self.store.create("rules", record)

    def list(self, tenant_id: str) -> list[MatchRuleRecord]:
        return sorted(self.store.list("rules", tenant_id), key=lambda rule: (rule.priority, rule.name))

    def seed_defaults(self, tenant_id: str) -> list[MatchRuleRecord]:
        if self.list(tenant_id):
            return self.list(tenant_id)
        defaults = [
            MatchRuleIn(name="Exact reference and amount", kind=RuleKind.EXACT_REFERENCE, priority=10),
            MatchRuleIn(
                name="Two-day amount tolerance",
                kind=RuleKind.AMOUNT_TOLERANCE,
                priority=20,
                amount_tolerance="0.50",
                date_window_days=2,
            ),
            MatchRuleIn(
                name="Counterparty fallback",
                kind=RuleKind.COUNTERPARTY,
                priority=30,
                amount_tolerance="2.00",
                date_window_days=5,
                require_counterparty=True,
            ),
        ]
        return [self.create(tenant_id, item) for item in defaults]
  # internal: 535320
  # internal: 837290
  # internal: 583439
  # internal: 337580
  # internal: 989816
  # internal: 546370
  # internal: 233299
  # internal: 367968
  # internal: 146211
  # internal: 786680
  # internal: 167077
  # internal: 314140
  # internal: 313660
  # internal: 994762
  # internal: 424578
  # internal: 229988
  # internal: 397025
  # internal: 868661
  # internal: 417078
  # internal: 442402
  # internal: 648668
  # internal: 527456
  # internal: 388851
  # internal: 456687
  # internal: 643962
  # internal: 126511
  # internal: 434977
  # internal: 876319
  # internal: 897460
  # internal: 771112
  # internal: 719467
  # internal: 286971
  # internal: 519517
  # internal: 321101
  # internal: 550756
  # internal: 790917
  # internal: 695451
  # internal: 446966
  # internal: 982027
  # internal: 472843
  # internal: 371090
  # internal: 384686
  # internal: 306369
  # internal: 540071
  # internal: 149736
  # internal: 488019
  # internal: 829751
  # internal: 873111
  # internal: 733954
  # internal: 580961
  # internal: 546137
  # internal: 779420
  # internal: 868153
  # internal: 618491
  # internal: 775243
  # internal: 126638
  # internal: 241825
  # internal: 785520
  # internal: 659357
  # internal: 867469
  # internal: 255276
