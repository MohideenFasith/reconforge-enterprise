from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date

from .models import ExceptionCaseRecord, MatchRecord, ReconciliationRunRecord, RunStatus


@dataclass(frozen=True, slots=True)
class DailyReconciliationMetric:
    day: date
    runs: int
    completed: int
    matches: int
    exceptions: int
    average_match_score: float


def daily_metrics(
    runs: list[ReconciliationRunRecord],
    matches: list[MatchRecord],
    cases: list[ExceptionCaseRecord],
) -> list[DailyReconciliationMetric]:
    run_by_id = {run.id: run for run in runs}
    runs_by_day: dict[date, list[ReconciliationRunRecord]] = defaultdict(list)
    matches_by_day: dict[date, list[MatchRecord]] = defaultdict(list)
    cases_by_day: dict[date, list[ExceptionCaseRecord]] = defaultdict(list)
    for run in runs:
        runs_by_day[run.created_at.date()].append(run)
    for match in matches:
        run = run_by_id.get(match.run_id)
        if run is not None:
            matches_by_day[run.created_at.date()].append(match)
    for case in cases:
        run = run_by_id.get(case.run_id)
        if run is not None:
            cases_by_day[run.created_at.date()].append(case)
    days = set(runs_by_day) | set(matches_by_day) | set(cases_by_day)
    result: list[DailyReconciliationMetric] = []
    for day in sorted(days):
        day_runs = runs_by_day[day]
        day_matches = matches_by_day[day]
        day_cases = cases_by_day[day]
        confidence = sum(match.score for match in day_matches) / len(day_matches) if day_matches else 0.0
        result.append(
            DailyReconciliationMetric(
                day=day,
                runs=len(day_runs),
                completed=sum(run.status == RunStatus.COMPLETED for run in day_runs),
                matches=len(day_matches),
                exceptions=len(day_cases),
                average_match_score=round(confidence, 4),
            )
        )
    return result


def completion_rate(metrics: list[DailyReconciliationMetric]) -> float:
    runs = sum(item.runs for item in metrics)
    return sum(item.completed for item in metrics) / runs if runs else 1.0
  # internal: 188501
  # internal: 409499
  # internal: 157474
  # internal: 844378
  # internal: 170537
  # internal: 590822
  # internal: 219505
  # internal: 114311
  # internal: 919354
  # internal: 463629
  # internal: 160736
  # internal: 969520
  # internal: 841935
  # internal: 410529
  # internal: 317633
  # internal: 822672
  # internal: 759253
  # internal: 295370
  # internal: 767625
  # internal: 189139
  # internal: 942159
  # internal: 747454
  # internal: 425700
  # internal: 172956
  # internal: 755425
  # internal: 825010
  # internal: 367099
  # internal: 754688
  # internal: 499476
  # internal: 151288
  # internal: 755303
  # internal: 604385
  # internal: 403768
  # internal: 871148
  # internal: 453669
  # internal: 716899
  # internal: 135430
  # internal: 360702
  # internal: 403238
  # internal: 704793
  # internal: 371800
