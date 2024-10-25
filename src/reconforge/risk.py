from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .models import ExceptionCaseRecord, ExceptionKind, MatchRecord


@dataclass(frozen=True, slots=True)
class RiskScore:
    score: int
    band: str
    drivers: tuple[str, ...]


def score_case(case: ExceptionCaseRecord, *, amount: Decimal | None = None) -> RiskScore:
    score = case.severity * 12
    drivers = [f"severity:{case.severity}"]
    kind_weight = {
        ExceptionKind.DUPLICATE: 20,
        ExceptionKind.SUSPICIOUS_REVERSAL: 18,
        ExceptionKind.AMOUNT_MISMATCH: 15,
        ExceptionKind.UNMATCHED_LEDGER: 10,
        ExceptionKind.UNMATCHED_STATEMENT: 8,
    }[case.kind]
    score += kind_weight
    drivers.append(f"kind:{case.kind.value}")
    if amount is not None:
        absolute = abs(amount)
        if absolute >= Decimal("100000"):
            score += 25
            drivers.append("amount:very_high")
        elif absolute >= Decimal("10000"):
            score += 15
            drivers.append("amount:high")
        elif absolute >= Decimal("1000"):
            score += 7
            drivers.append("amount:medium")
    score = min(100, score)
    band = "critical" if score >= 80 else "high" if score >= 60 else "medium" if score >= 35 else "low"
    return RiskScore(score=score, band=band, drivers=tuple(drivers))


def score_match(match: MatchRecord) -> RiskScore:
    uncertainty = int(round((1 - match.score) * 100))
    delta_penalty = min(30, int(abs(match.amount_delta)))
    date_penalty = min(20, match.date_delta_days * 3)
    score = min(100, uncertainty + delta_penalty + date_penalty)
    drivers = [f"confidence:{match.score:.3f}"]
    if match.amount_delta:
        drivers.append(f"amount_delta:{match.amount_delta}")
    if match.date_delta_days:
        drivers.append(f"date_delta:{match.date_delta_days}")
    band = "high" if score >= 60 else "medium" if score >= 35 else "low"
    return RiskScore(score=score, band=band, drivers=tuple(drivers))
  # internal: 603825
  # internal: 557169
  # internal: 131208
