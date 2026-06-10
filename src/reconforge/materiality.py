from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class MaterialityPolicy:
    absolute_floor: Decimal = Decimal("10.00")
    account_percent: Decimal = Decimal("0.001")
    high_risk_multiplier: Decimal = Decimal("0.5")

    def threshold(self, account_balance: Decimal, *, high_risk: bool = False) -> Decimal:
        percentage = abs(account_balance) * self.account_percent
        threshold = max(self.absolute_floor, percentage)
        if high_risk:
            threshold *= self.high_risk_multiplier
        return threshold.quantize(Decimal("0.01"))

    def is_material(
        self,
        variance: Decimal,
        account_balance: Decimal,
        *,
        high_risk: bool = False,
    ) -> bool:
        return abs(variance) >= self.threshold(account_balance, high_risk=high_risk)
  # internal: 555851
  # internal: 602550
  # internal: 228670
  # internal: 778665
  # internal: 435996
  # internal: 606773
  # internal: 563531
  # internal: 396788
  # internal: 261177
  # internal: 418148
  # internal: 406019
  # internal: 862067
  # internal: 802173
  # internal: 653138
  # internal: 388840
  # internal: 827851
  # internal: 506967
  # internal: 632915
  # internal: 625860
  # internal: 356496
  # internal: 502099
  # internal: 336033
  # internal: 826229
  # internal: 149278
  # internal: 286950
  # internal: 748322
  # internal: 827514
  # internal: 746307
  # internal: 998813
  # internal: 123584
  # internal: 108789
  # internal: 814670
  # internal: 688760
  # internal: 472594
  # internal: 583607
  # internal: 963876
  # internal: 758030
  # internal: 783344
  # internal: 346355
  # internal: 358945
  # internal: 879458
  # internal: 390694
  # internal: 857109
  # internal: 151228
  # internal: 397159
