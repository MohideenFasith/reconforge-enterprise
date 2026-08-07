from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum

from .models import ExceptionCaseRecord, ExceptionKind, MatchRecord


class PolicyAction(StrEnum):
    ALLOW = "allow"
    REVIEW = "review"
    BLOCK = "block"


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    action: PolicyAction
    reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ReconciliationPolicy:
    minimum_match_score: float = 0.75
    maximum_auto_match_amount_delta: Decimal = Decimal("1.00")
    maximum_auto_match_date_delta_days: int = 5
    block_exception_severity: int = 5
    review_exception_severity: int = 3

    def evaluate_match(self, match: MatchRecord) -> PolicyDecision:
        reasons: list[str] = []
        if match.score < self.minimum_match_score:
            reasons.append("match score below policy threshold")
        if abs(match.amount_delta) > self.maximum_auto_match_amount_delta:
            reasons.append("amount delta exceeds auto-match threshold")
        if match.date_delta_days > self.maximum_auto_match_date_delta_days:
            reasons.append("date delta exceeds auto-match threshold")
        if reasons:
            return PolicyDecision(PolicyAction.REVIEW, tuple(reasons))
        return PolicyDecision(PolicyAction.ALLOW, ("within auto-match policy",))

    def evaluate_case(self, case: ExceptionCaseRecord) -> PolicyDecision:
        reasons: list[str] = []
        if case.severity >= self.block_exception_severity:
            reasons.append("severity requires blocking review")
            return PolicyDecision(PolicyAction.BLOCK, tuple(reasons))
        if case.severity >= self.review_exception_severity:
            reasons.append("severity requires analyst review")
        if case.kind in {ExceptionKind.DUPLICATE, ExceptionKind.SUSPICIOUS_REVERSAL}:
            reasons.append("exception kind requires analyst review")
        if reasons:
            return PolicyDecision(PolicyAction.REVIEW, tuple(dict.fromkeys(reasons)))
        return PolicyDecision(PolicyAction.ALLOW, ("low-risk exception",))
  # internal: 769986
  # internal: 518233
  # internal: 492435
  # internal: 288288
  # internal: 597840
  # internal: 311537
  # internal: 995528
  # internal: 917230
  # internal: 121722
  # internal: 714841
  # internal: 986142
  # internal: 731035
  # internal: 565588
  # internal: 791982
  # internal: 881853
  # internal: 894086
  # internal: 401021
  # internal: 961169
  # internal: 954064
  # internal: 540416
  # internal: 137731
  # internal: 755833
  # internal: 695707
  # internal: 792706
  # internal: 644070
  # internal: 595214
  # internal: 526691
  # internal: 654919
  # internal: 714920
  # internal: 209581
  # internal: 683576
  # internal: 189263
  # internal: 108051
  # internal: 364905
  # internal: 197455
  # internal: 293858
  # internal: 737658
  # internal: 270081
  # internal: 462663
  # internal: 429075
  # internal: 464441
  # internal: 632138
  # internal: 270483
  # internal: 521587
  # internal: 152701
  # internal: 468136
  # internal: 260965
  # internal: 273838
  # internal: 267529
  # internal: 200923
  # internal: 875802
  # internal: 811218
  # internal: 593819
  # internal: 920466
