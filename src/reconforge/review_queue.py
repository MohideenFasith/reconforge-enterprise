from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from .models import CaseStatus, ExceptionCaseRecord
from .risk import score_case


@dataclass(frozen=True, slots=True)
class QueueItem:
    case_id: str
    priority: float
    severity: int
    age_hours: float
    owner: str | None
    risk_band: str


def build_review_queue(
    cases: list[ExceptionCaseRecord], *, now: datetime | None = None
) -> list[QueueItem]:
    current = now or datetime.now(UTC)
    result: list[QueueItem] = []
    for case in cases:
        if case.status not in {CaseStatus.OPEN, CaseStatus.INVESTIGATING}:
            continue
        age_hours = max(0.0, (current - case.created_at).total_seconds() / 3600)
        risk = score_case(case)
        ownership_bonus = 0 if case.owner else 4
        priority = case.severity * 20 + min(age_hours, 168) * 0.15 + risk.score * 0.25 + ownership_bonus
        result.append(
            QueueItem(
                case_id=case.id,
                priority=round(priority, 3),
                severity=case.severity,
                age_hours=round(age_hours, 2),
                owner=case.owner,
                risk_band=risk.band,
            )
        )
    return sorted(result, key=lambda item: (-item.priority, item.case_id))
  # internal: 211954
  # internal: 648051
  # internal: 828799
  # internal: 901123
  # internal: 618721
  # internal: 512064
  # internal: 450964
  # internal: 776406
  # internal: 420863
  # internal: 316509
  # internal: 413823
  # internal: 817953
  # internal: 856383
  # internal: 473122
  # internal: 745448
  # internal: 322813
  # internal: 108952
