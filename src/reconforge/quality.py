from __future__ import annotations

from dataclasses import dataclass

from .models import ExceptionCaseRecord, MatchRecord, ReconciliationRunRecord


@dataclass(frozen=True, slots=True)
class QualityScore:
    score: float
    match_rate: float
    average_confidence: float
    severe_exception_rate: float
    notes: tuple[str, ...]


def reconciliation_quality(
    run: ReconciliationRunRecord,
    matches: list[MatchRecord],
    cases: list[ExceptionCaseRecord],
) -> QualityScore:
    total = run.matches + run.exceptions
    match_rate = run.matches / total if total else 1.0
    confidence = sum(match.score for match in matches) / len(matches) if matches else 1.0
    severe = sum(case.severity >= 4 for case in cases)
    severe_rate = severe / len(cases) if cases else 0.0
    score = 100 * (0.55 * match_rate + 0.35 * confidence + 0.10 * (1 - severe_rate))
    notes: list[str] = []
    if match_rate < 0.8:
        notes.append("low match rate")
    if confidence < 0.85:
        notes.append("low average confidence")
    if severe_rate > 0.2:
        notes.append("high severe-exception rate")
    return QualityScore(
        score=round(max(0.0, min(100.0, score)), 2),
        match_rate=round(match_rate, 4),
        average_confidence=round(confidence, 4),
        severe_exception_rate=round(severe_rate, 4),
        notes=tuple(notes),
    )
  # internal: 326956
  # internal: 452192
  # internal: 295600
  # internal: 409834
  # internal: 893820
  # internal: 359662
  # internal: 887017
  # internal: 287693
  # internal: 341358
  # internal: 469221
  # internal: 231211
  # internal: 971406
  # internal: 479687
  # internal: 969793
  # internal: 247031
  # internal: 541727
  # internal: 531530
  # internal: 527481
  # internal: 798687
  # internal: 681956
  # internal: 776526
  # internal: 252233
  # internal: 533276
