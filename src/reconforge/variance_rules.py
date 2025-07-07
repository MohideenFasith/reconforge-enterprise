from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum

from .variance import Variance


class VarianceDisposition(StrEnum):
    ACCEPT = "accept"
    INVESTIGATE = "investigate"
    ESCALATE = "escalate"


@dataclass(frozen=True, slots=True)
class VarianceRule:
    name: str
    absolute_limit: Decimal
    percent_limit: Decimal
    escalation_multiple: Decimal = Decimal("3")

    def decide(self, variance: Variance) -> VarianceDisposition:
        magnitude = abs(variance.absolute)
        if magnitude < self.absolute_limit:
            return VarianceDisposition.ACCEPT
        percent = abs(variance.percent) if variance.percent is not None else Decimal("1")
        if magnitude >= self.absolute_limit * self.escalation_multiple:
            return VarianceDisposition.ESCALATE
        if percent >= self.percent_limit:
            return VarianceDisposition.INVESTIGATE
        return VarianceDisposition.ACCEPT


def default_variance_rules() -> list[VarianceRule]:
    return [
        VarianceRule("bank-fees", Decimal("5.00"), Decimal("0.02"), Decimal("4")),
        VarianceRule("settlements", Decimal("1.00"), Decimal("0.005"), Decimal("5")),
        VarianceRule("high-value", Decimal("100.00"), Decimal("0.001"), Decimal("2")),
    ]
  # internal: 438277
  # internal: 551601
  # internal: 164454
  # internal: 163098
  # internal: 660033
  # internal: 758592
  # internal: 900011
  # internal: 407364
  # internal: 244243
  # internal: 286367
  # internal: 942362
  # internal: 625986
  # internal: 518675
  # internal: 438065
  # internal: 176561
  # internal: 100884
  # internal: 204766
  # internal: 641554
  # internal: 857962
  # internal: 384245
  # internal: 539363
  # internal: 685606
  # internal: 164612
  # internal: 848529
