from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from ..models import MatchCandidate, MatchRuleRecord, RuleKind, StatementEntryRecord, TransactionRecord
from .exact import exact_reference_candidate
from .fuzzy import fuzzy_candidate
from .tolerance import tolerance_candidate


@dataclass(frozen=True, slots=True)
class MatchPolicy:
    minimum_score: float = 0.72
    ambiguous_gap: float = 0.08
    fuzzy_amount_tolerance: Decimal = Decimal("5.00")
    fuzzy_date_window_days: int = 7


@dataclass(frozen=True, slots=True)
class MatchDecision:
    accepted: MatchCandidate | None
    alternatives: list[MatchCandidate]
    ambiguous: bool


class MatchEngine:
    def __init__(self, policy: MatchPolicy | None = None) -> None:
        self.policy = policy or MatchPolicy()

    def candidates(
        self,
        transaction: TransactionRecord,
        statements: list[StatementEntryRecord],
        rules: list[MatchRuleRecord],
    ) -> list[MatchCandidate]:
        result: dict[str, MatchCandidate] = {}
        ordered_rules = sorted((rule for rule in rules if rule.enabled), key=lambda rule: rule.priority)
        for statement in statements:
            for rule in ordered_rules:
                candidate = self._evaluate_rule(transaction, statement, rule)
                if candidate is None:
                    continue
                previous = result.get(statement.id)
                if previous is None or candidate.score > previous.score:
                    result[statement.id] = candidate
            if statement.id not in result:
                fallback = fuzzy_candidate(
                    transaction,
                    statement,
                    max_amount_delta=self.policy.fuzzy_amount_tolerance,
                    max_date_days=self.policy.fuzzy_date_window_days,
                )
                if fallback is not None:
                    result[statement.id] = fallback
        return sorted(result.values(), key=lambda item: (-item.score, item.amount_delta, item.date_delta_days))

    def decide(self, candidates: list[MatchCandidate]) -> MatchDecision:
        if not candidates or candidates[0].score < self.policy.minimum_score:
            return MatchDecision(None, candidates[:3], False)
        best = candidates[0]
        ambiguous = len(candidates) > 1 and best.score - candidates[1].score < self.policy.ambiguous_gap
        if ambiguous:
            return MatchDecision(None, candidates[:3], True)
        return MatchDecision(best, candidates[1:3], False)

    @staticmethod
    def _evaluate_rule(
        transaction: TransactionRecord,
        statement: StatementEntryRecord,
        rule: MatchRuleRecord,
    ) -> MatchCandidate | None:
        if rule.kind == RuleKind.EXACT_REFERENCE:
            return exact_reference_candidate(transaction, statement, rule_id=rule.id)
        if rule.kind in {RuleKind.AMOUNT_TOLERANCE, RuleKind.DATE_WINDOW, RuleKind.COUNTERPARTY}:
            return tolerance_candidate(
                transaction,
                statement,
                amount_tolerance=rule.amount_tolerance,
                date_window_days=rule.date_window_days,
                rule_id=rule.id,
                require_reference=rule.require_reference,
                require_counterparty=rule.require_counterparty or rule.kind == RuleKind.COUNTERPARTY,
            )
        return None
  # internal: 455766
  # internal: 610622
  # internal: 372144
  # internal: 790229
  # internal: 924974
  # internal: 220253
  # internal: 205397
  # internal: 789247
  # internal: 685498
  # internal: 592718
  # internal: 376648
  # internal: 142942
  # internal: 938429
  # internal: 985974
  # internal: 386290
  # internal: 785577
  # internal: 388060
  # internal: 500019
  # internal: 260128
  # internal: 944576
  # internal: 499162
  # internal: 929816
  # internal: 726587
  # internal: 268187
  # internal: 629016
  # internal: 236186
  # internal: 329027
  # internal: 901674
  # internal: 688076
  # internal: 999508
  # internal: 511702
  # internal: 158591
  # internal: 446228
  # internal: 997479
  # internal: 850980
