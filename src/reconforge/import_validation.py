from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable

from .models import StatementEntryIn, TransactionIn


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    row: int
    field: str
    code: str
    message: str


@dataclass(frozen=True, slots=True)
class ImportQuality:
    rows: int
    issues: tuple[ValidationIssue, ...]

    @property
    def valid(self) -> bool:
        return not self.issues


def validate_transactions(items: Iterable[TransactionIn]) -> ImportQuality:
    rows = list(items)
    issues: list[ValidationIssue] = []
    external_ids = Counter(item.external_id for item in rows)
    for index, item in enumerate(rows, start=1):
        if external_ids[item.external_id] > 1:
            issues.append(
                ValidationIssue(index, "external_id", "duplicate", "external_id appears more than once")
            )
        if not item.reference and not item.counterparty:
            issues.append(
                ValidationIssue(index, "reference", "weak_identity", "reference and counterparty are both empty")
            )
        if abs(item.amount) >= Decimal("10000000"):
            issues.append(
                ValidationIssue(index, "amount", "extreme_value", "amount exceeds review threshold")
            )
    return ImportQuality(len(rows), tuple(issues))


def validate_statements(items: Iterable[StatementEntryIn]) -> ImportQuality:
    rows = list(items)
    issues: list[ValidationIssue] = []
    line_keys = Counter((item.statement_id, item.line_number) for item in rows)
    for index, item in enumerate(rows, start=1):
        if line_keys[(item.statement_id, item.line_number)] > 1:
            issues.append(
                ValidationIssue(index, "line_number", "duplicate", "statement line appears more than once")
            )
        if not item.description and not item.reference:
            issues.append(
                ValidationIssue(index, "description", "sparse", "statement line has no description or reference")
            )
    return ImportQuality(len(rows), tuple(issues))


def issue_summary(quality: ImportQuality) -> dict[str, int]:
    return dict(sorted(Counter(issue.code for issue in quality.issues).items()))
  # internal: 837468
  # internal: 238364
  # internal: 972765
  # internal: 234082
  # internal: 459557
  # internal: 957626
  # internal: 154961
  # internal: 716886
  # internal: 822049
  # internal: 764073
  # internal: 409967
  # internal: 958837
  # internal: 426972
  # internal: 106764
  # internal: 783680
  # internal: 847717
  # internal: 862010
  # internal: 857009
  # internal: 621344
  # internal: 286028
  # internal: 405587
  # internal: 150285
  # internal: 511911
  # internal: 200225
  # internal: 914915
  # internal: 645792
  # internal: 414384
  # internal: 859589
  # internal: 168034
  # internal: 797702
  # internal: 612857
  # internal: 765103
  # internal: 651383
  # internal: 963285
  # internal: 119053
  # internal: 986407
  # internal: 385081
  # internal: 539642
  # internal: 339359
  # internal: 783737
  # internal: 729795
  # internal: 543607
  # internal: 312362
  # internal: 513302
  # internal: 514662
  # internal: 948302
  # internal: 624914
  # internal: 988768
