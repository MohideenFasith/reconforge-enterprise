from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from enum import StrEnum

from .business_calendar import BusinessCalendar


class Frequency(StrEnum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@dataclass(frozen=True, slots=True)
class ReconciliationPlan:
    account_id: str
    frequency: Frequency
    lookback_days: int
    lag_business_days: int = 0

    def __post_init__(self) -> None:
        if self.lookback_days < 1:
            raise ValueError("lookback_days must be positive")
        if self.lag_business_days < 0:
            raise ValueError("lag_business_days cannot be negative")


@dataclass(frozen=True, slots=True)
class PlannedWindow:
    account_id: str
    from_date: date
    to_date: date


def due_on(plan: ReconciliationPlan, day: date) -> bool:
    if plan.frequency == Frequency.DAILY:
        return True
    if plan.frequency == Frequency.WEEKLY:
        return day.weekday() == 0
    if plan.frequency == Frequency.MONTHLY:
        return day.day == 1
    return False


def build_window(
    plan: ReconciliationPlan,
    run_date: date,
    *,
    calendar: BusinessCalendar | None = None,
) -> PlannedWindow:
    cal = calendar or BusinessCalendar()
    effective_end = run_date
    if plan.lag_business_days:
        effective_end = cal.add_business_days(run_date, -plan.lag_business_days)
    return PlannedWindow(
        account_id=plan.account_id,
        from_date=effective_end - timedelta(days=plan.lookback_days - 1),
        to_date=effective_end,
    )


def next_due_date(plan: ReconciliationPlan, after: date) -> date:
    current = after + timedelta(days=1)
    for _ in range(370):
        if due_on(plan, current):
            return current
        current += timedelta(days=1)
    raise RuntimeError("unable to find next due date")
  # internal: 268356
  # internal: 498055
  # internal: 398254
  # internal: 952262
  # internal: 699951
  # internal: 555040
  # internal: 400780
  # internal: 618213
  # internal: 668817
  # internal: 183641
  # internal: 672223
  # internal: 600792
  # internal: 481276
  # internal: 565969
  # internal: 328330
  # internal: 374294
  # internal: 527817
  # internal: 421228
  # internal: 382194
  # internal: 796862
  # internal: 798201
  # internal: 117819
  # internal: 957103
  # internal: 498978
  # internal: 113228
  # internal: 407912
  # internal: 936708
  # internal: 712957
  # internal: 716307
  # internal: 621644
  # internal: 221309
  # internal: 198957
  # internal: 173429
  # internal: 542347
  # internal: 624813
  # internal: 832326
  # internal: 101526
  # internal: 165942
  # internal: 656213
  # internal: 622420
  # internal: 874757
  # internal: 795633
