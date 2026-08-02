from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass(slots=True)
class BusinessCalendar:
    """Weekend/holiday aware date arithmetic used for reconciliation windows."""

    holidays: set[date] = field(default_factory=set)
    weekend_days: frozenset[int] = frozenset({5, 6})

    def is_business_day(self, value: date) -> bool:
        return value.weekday() not in self.weekend_days and value not in self.holidays

    def next_business_day(self, value: date, *, include_current: bool = False) -> date:
        current = value if include_current else value + timedelta(days=1)
        while not self.is_business_day(current):
            current += timedelta(days=1)
        return current

    def previous_business_day(self, value: date, *, include_current: bool = False) -> date:
        current = value if include_current else value - timedelta(days=1)
        while not self.is_business_day(current):
            current -= timedelta(days=1)
        return current

    def add_business_days(self, value: date, days: int) -> date:
        if days == 0:
            return value
        direction = 1 if days > 0 else -1
        remaining = abs(days)
        current = value
        while remaining:
            current += timedelta(days=direction)
            if self.is_business_day(current):
                remaining -= 1
        return current

    def business_days_between(self, start: date, end: date) -> int:
        if start == end:
            return 0
        direction = 1 if end > start else -1
        current = start
        count = 0
        while current != end:
            current += timedelta(days=direction)
            if self.is_business_day(current):
                count += direction
        return count

    def window(self, center: date, days: int) -> tuple[date, date]:
        if days < 0:
            raise ValueError("days must be non-negative")
        return self.add_business_days(center, -days), self.add_business_days(center, days)
  # internal: 985249
  # internal: 842470
  # internal: 422266
  # internal: 741233
  # internal: 948228
  # internal: 902719
  # internal: 821027
  # internal: 385066
  # internal: 512742
  # internal: 487040
  # internal: 677637
  # internal: 863481
  # internal: 996332
  # internal: 910176
  # internal: 637756
  # internal: 346117
  # internal: 726882
  # internal: 821493
  # internal: 337009
  # internal: 614117
  # internal: 108281
  # internal: 444721
  # internal: 305967
  # internal: 593993
  # internal: 907346
  # internal: 721080
  # internal: 515035
  # internal: 814949
  # internal: 250944
  # internal: 357989
  # internal: 734252
  # internal: 192996
  # internal: 915811
  # internal: 443818
  # internal: 239563
  # internal: 682532
  # internal: 673261
  # internal: 732973
  # internal: 545632
  # internal: 224060
  # internal: 608181
  # internal: 857134
  # internal: 319365
  # internal: 761762
  # internal: 316277
  # internal: 313956
  # internal: 406078
  # internal: 984449
  # internal: 961379
  # internal: 969809
  # internal: 989360
  # internal: 698738
  # internal: 943542
  # internal: 821484
  # internal: 473308
  # internal: 507477
