from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .models import MatchRecord


@dataclass(frozen=True, slots=True)
class SampleDecision:
    match_id: str
    selected: bool
    reason: str


def _stable_fraction(value: str) -> float:
    digest = hashlib.sha256(value.encode()).digest()
    integer = int.from_bytes(digest[:8], "big")
    return integer / float(2**64 - 1)


def select_quality_sample(
    matches: list[MatchRecord],
    *,
    base_rate: float = 0.05,
    low_confidence_threshold: float = 0.82,
) -> list[SampleDecision]:
    if not 0 <= base_rate <= 1:
        raise ValueError("base_rate must be between 0 and 1")
    decisions: list[SampleDecision] = []
    for match in matches:
        if match.score < low_confidence_threshold:
            decisions.append(SampleDecision(match.id, True, "low confidence"))
            continue
        if match.amount_delta:
            decisions.append(SampleDecision(match.id, True, "non-zero amount delta"))
            continue
        selected = _stable_fraction(match.id) < base_rate
        decisions.append(SampleDecision(match.id, selected, "random control sample" if selected else "not selected"))
    return decisions
