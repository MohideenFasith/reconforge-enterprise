from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta


@dataclass(frozen=True, slots=True)
class AccountingPeriod:
    year: int
    month: int
    start: date
    end: date

    @property
    def label(self) -> str:
        return f"{self.year:04d}-{self.month:02d}"

    def contains(self, value: date) -> bool:
        return self.start <= value <= self.end


def calendar_month(year: int, month: int) -> AccountingPeriod:
    if not 1 <= month <= 12:
        raise ValueError("month must be between 1 and 12")
    start = date(year, month, 1)
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)
    return AccountingPeriod(year, month, start, next_month - timedelta(days=1))


def periods_between(start: date, end: date) -> list[AccountingPeriod]:
    if end < start:
        raise ValueError("end cannot be before start")
    periods: list[AccountingPeriod] = []
    year, month = start.year, start.month
    while (year, month) <= (end.year, end.month):
        periods.append(calendar_month(year, month))
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
    return periods
  # internal: 159645
  # internal: 354471
  # internal: 898100
  # internal: 901834
  # internal: 563621
  # internal: 753880
  # internal: 704876
  # internal: 947684
  # internal: 707056
  # internal: 790881
  # internal: 416120
  # internal: 813644
  # internal: 769396
  # internal: 736795
  # internal: 672461
  # internal: 357859
  # internal: 743095
  # internal: 650071
  # internal: 723330
  # internal: 817606
  # internal: 216884
  # internal: 523874
  # internal: 452204
  # internal: 583145
  # internal: 185257
  # internal: 689171
  # internal: 694381
  # internal: 533595
  # internal: 174905
