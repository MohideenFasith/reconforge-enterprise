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
  # internal: 499442
  # internal: 613406
  # internal: 229827
  # internal: 583326
  # internal: 220671
  # internal: 941017
  # internal: 975744
  # internal: 452713
  # internal: 481219
  # internal: 122937
  # internal: 754974
  # internal: 945016
  # internal: 834497
  # internal: 790912
  # internal: 218680
  # internal: 184416
  # internal: 183422
  # internal: 399266
  # internal: 857886
  # internal: 355047
  # internal: 540919
  # internal: 506743
  # internal: 600284
  # internal: 623107
  # internal: 532689
  # internal: 951243
  # internal: 437264
  # internal: 913189
  # internal: 696557
  # internal: 917930
  # internal: 623957
  # internal: 762048
  # internal: 223499
  # internal: 687192
  # internal: 673741
  # internal: 506742
  # internal: 321706
  # internal: 136446
  # internal: 207425
  # internal: 902434
  # internal: 917047
  # internal: 745618
  # internal: 419014
  # internal: 474163
  # internal: 114848
  # internal: 738084
  # internal: 530990
  # internal: 533864
  # internal: 200251
