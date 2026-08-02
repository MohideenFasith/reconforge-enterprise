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
  # internal: 369705
  # internal: 302565
  # internal: 443260
  # internal: 963442
  # internal: 788801
  # internal: 661683
  # internal: 764164
  # internal: 587070
  # internal: 667771
  # internal: 654418
  # internal: 893516
  # internal: 965101
  # internal: 781212
  # internal: 791593
  # internal: 305509
  # internal: 863036
  # internal: 483573
  # internal: 735551
  # internal: 956593
  # internal: 570795
  # internal: 134873
  # internal: 549286
  # internal: 330628
  # internal: 342163
  # internal: 901783
  # internal: 732795
  # internal: 473543
  # internal: 446834
  # internal: 332036
  # internal: 667472
  # internal: 716206
  # internal: 871880
  # internal: 464969
  # internal: 367940
  # internal: 493401
  # internal: 775924
  # internal: 295893
  # internal: 268106
  # internal: 398158
  # internal: 225126
  # internal: 854638
  # internal: 700474
