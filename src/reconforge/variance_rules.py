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
  # internal: 323114
  # internal: 337798
  # internal: 698129
  # internal: 591852
  # internal: 139280
  # internal: 805284
  # internal: 458719
  # internal: 874793
  # internal: 496452
  # internal: 723136
  # internal: 878251
  # internal: 354506
  # internal: 888878
  # internal: 885461
  # internal: 136786
  # internal: 846660
  # internal: 268927
  # internal: 108363
  # internal: 803330
  # internal: 954659
  # internal: 365222
  # internal: 765640
  # internal: 441993
  # internal: 773960
  # internal: 969164
  # internal: 210484
  # internal: 141438
  # internal: 489264
  # internal: 333066
  # internal: 225178
  # internal: 654156
  # internal: 964278
  # internal: 669581
  # internal: 775829
  # internal: 211038
  # internal: 292483
  # internal: 984078
  # internal: 831711
  # internal: 732784
  # internal: 357229
