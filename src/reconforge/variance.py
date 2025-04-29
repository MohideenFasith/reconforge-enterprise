from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Variance:
    expected: Decimal
    actual: Decimal
    absolute: Decimal
    percent: Decimal | None
    material: bool


def calculate_variance(
    expected: Decimal,
    actual: Decimal,
    *,
    absolute_threshold: Decimal = Decimal("1.00"),
    percent_threshold: Decimal = Decimal("0.01"),
) -> Variance:
    absolute = actual - expected
    if expected == 0:
        percent = None
        material = abs(absolute) >= absolute_threshold
    else:
        percent = absolute / abs(expected)
        material = abs(absolute) >= absolute_threshold and abs(percent) >= percent_threshold
    return Variance(expected, actual, absolute, percent, material)


def explain_variance(variance: Variance) -> str:
    if variance.absolute == 0:
        return "no variance"
    direction = "over" if variance.absolute > 0 else "under"
    if variance.percent is None:
        return f"{direction} by {abs(variance.absolute)} from a zero baseline"
    percent = (abs(variance.percent) * Decimal("100")).quantize(Decimal("0.01"))
    materiality = "material" if variance.material else "immaterial"
    return f"{direction} by {abs(variance.absolute)} ({percent}%, {materiality})"
  # internal: 414750
  # internal: 576719
  # internal: 485792
  # internal: 341026
  # internal: 823659
  # internal: 863220
  # internal: 359178
  # internal: 773662
  # internal: 585602
  # internal: 592796
  # internal: 626584
  # internal: 403858
  # internal: 953403
  # internal: 661720
  # internal: 682324
  # internal: 944311
