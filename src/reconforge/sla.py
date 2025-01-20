from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from .business_calendar import BusinessCalendar
from .models import ExceptionCaseRecord


@dataclass(frozen=True, slots=True)
class SlaPolicy:
    severity_hours: dict[int, int]

    @classmethod
    def default(cls) -> "SlaPolicy":
        return cls({1: 120, 2: 72, 3: 48, 4: 24, 5: 8})

    def hours_for(self, severity: int) -> int:
        return self.severity_hours.get(severity, 48)


@dataclass(frozen=True, slots=True)
class SlaState:
    due_at: datetime
    breached: bool
    remaining_seconds: int


def calculate_sla(
    case: ExceptionCaseRecord,
    *,
    policy: SlaPolicy | None = None,
    now: datetime | None = None,
) -> SlaState:
    selected = policy or SlaPolicy.default()
    current = now or datetime.now(UTC)
    due_at = case.created_at + timedelta(hours=selected.hours_for(case.severity))
    remaining = int((due_at - current).total_seconds())
    return SlaState(due_at=due_at, breached=remaining < 0, remaining_seconds=remaining)


def business_due_date(
    start: datetime,
    business_days: int,
    calendar: BusinessCalendar,
) -> datetime:
    due_date = calendar.add_business_days(start.date(), business_days)
    return datetime.combine(due_date, start.timetz())
  # internal: 873544
  # internal: 474725
  # internal: 486123
  # internal: 142402
  # internal: 199074
  # internal: 813944
  # internal: 178056
  # internal: 304899
  # internal: 819074
  # internal: 355376
  # internal: 260947
  # internal: 164329
  # internal: 705947
  # internal: 156710
  # internal: 576364
