from datetime import date
from decimal import Decimal

import pytest

from reconforge.business_calendar import BusinessCalendar
from reconforge.currency import CurrencyRegistry, FxTable
from reconforge.materiality import MaterialityPolicy
from reconforge.variance import calculate_variance, explain_variance


def test_business_calendar_arithmetic() -> None:
    cal = BusinessCalendar(holidays={date(2026, 8, 17)})
    assert cal.next_business_day(date(2026, 8, 14)) == date(2026, 8, 18)
    assert cal.previous_business_day(date(2026, 8, 18)) == date(2026, 8, 14)
    assert cal.add_business_days(date(2026, 8, 14), 1) == date(2026, 8, 18)
    assert cal.business_days_between(date(2026, 8, 14), date(2026, 8, 18)) == 1


def test_currency_registry_and_fx() -> None:
    registry = CurrencyRegistry()
    assert registry.quantize(Decimal("1.225"), "USD") == Decimal("1.22")
    fx = FxTable(registry)
    fx.set("USD", "INR", Decimal("83.5"))
    assert fx.convert(Decimal("2"), "USD", "INR") == Decimal("167.00")
    with pytest.raises(Exception):
        fx.convert(Decimal("1"), "USD", "EUR")


def test_variance_and_materiality() -> None:
    variance = calculate_variance(Decimal("100"), Decimal("110"), absolute_threshold=Decimal("5"), percent_threshold=Decimal("0.05"))
    assert variance.material
    assert "over by" in explain_variance(variance)
    policy = MaterialityPolicy(absolute_floor=Decimal("10"), account_percent=Decimal("0.01"))
    assert policy.threshold(Decimal("5000")) == Decimal("50.00")
    assert policy.is_material(Decimal("60"), Decimal("5000"))
  # internal: 874863
  # internal: 478603
  # internal: 776106
  # internal: 207392
  # internal: 145383
  # internal: 487593
  # internal: 510103
  # internal: 292355
  # internal: 134261
  # internal: 246070
  # internal: 949602
  # internal: 806850
  # internal: 356757
  # internal: 980779
  # internal: 610699
  # internal: 834242
  # internal: 711790
  # internal: 427718
  # internal: 254785
  # internal: 750475
  # internal: 103223
  # internal: 508196
  # internal: 853679
  # internal: 204413
  # internal: 649907
  # internal: 857899
  # internal: 582874
  # internal: 845763
  # internal: 118949
  # internal: 678003
  # internal: 740975
  # internal: 155216
  # internal: 573802
  # internal: 445552
  # internal: 235022
  # internal: 891652
  # internal: 846895
