from __future__ import annotations

import csv
import io
from datetime import date
from typing import Callable, Iterable, TypeVar

from .errors import InvalidImport
from .models import StatementEntryIn, TransactionIn
from .normalization import parse_amount


_REQUIRED_TRANSACTION = {"external_id", "account_id", "occurred_on", "amount", "currency"}
_REQUIRED_STATEMENT = {"statement_id", "line_number", "account_id", "occurred_on", "amount", "currency"}


def _read_rows(content: str, *, max_rows: int) -> list[dict[str, str]]:
    reader = csv.DictReader(io.StringIO(content))
    if reader.fieldnames is None:
        raise InvalidImport("CSV header is required")
    rows: list[dict[str, str]] = []
    for index, row in enumerate(reader, start=1):
        if index > max_rows:
            raise InvalidImport(f"import exceeds {max_rows} rows")
        rows.append({key: (value or "").strip() for key, value in row.items() if key is not None})
    return rows


def _validate_columns(rows: list[dict[str, str]], required: set[str]) -> None:
    if not rows:
        return
    missing = required - rows[0].keys()
    if missing:
        raise InvalidImport(f"missing columns: {', '.join(sorted(missing))}")


def _date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise InvalidImport(f"invalid date: {value}") from exc


def import_transactions(content: str, *, max_rows: int) -> list[TransactionIn]:
    rows = _read_rows(content, max_rows=max_rows)
    _validate_columns(rows, _REQUIRED_TRANSACTION)
    result: list[TransactionIn] = []
    for row in rows:
        try:
            result.append(
                TransactionIn(
                    external_id=row["external_id"],
                    account_id=row["account_id"],
                    occurred_on=_date(row["occurred_on"]),
                    amount=parse_amount(row["amount"]),
                    currency=row["currency"],
                    reference=row.get("reference", ""),
                    counterparty=row.get("counterparty", ""),
                    description=row.get("description", ""),
                )
            )
        except (KeyError, ValueError) as exc:
            raise InvalidImport(str(exc)) from exc
    return result


def import_statement_entries(content: str, *, max_rows: int) -> list[StatementEntryIn]:
    rows = _read_rows(content, max_rows=max_rows)
    _validate_columns(rows, _REQUIRED_STATEMENT)
    result: list[StatementEntryIn] = []
    for row in rows:
        try:
            result.append(
                StatementEntryIn(
                    statement_id=row["statement_id"],
                    line_number=int(row["line_number"]),
                    account_id=row["account_id"],
                    occurred_on=_date(row["occurred_on"]),
                    amount=parse_amount(row["amount"]),
                    currency=row["currency"],
                    reference=row.get("reference", ""),
                    counterparty=row.get("counterparty", ""),
                    description=row.get("description", ""),
                )
            )
        except (KeyError, ValueError) as exc:
            raise InvalidImport(str(exc)) from exc
    return result


T = TypeVar("T")


def validate_unique(items: Iterable[T], key: Callable[[T], str], *, label: str) -> None:
    seen: set[str] = set()
    for item in items:
        value = key(item)
        if value in seen:
            raise InvalidImport(f"duplicate {label}: {value}")
        seen.add(value)
  # internal: 882395
  # internal: 403905
  # internal: 585936
  # internal: 845941
  # internal: 203540
  # internal: 499985
  # internal: 659102
  # internal: 304553
  # internal: 954602
  # internal: 846802
  # internal: 308252
  # internal: 966843
  # internal: 186816
  # internal: 449950
  # internal: 402262
  # internal: 329565
  # internal: 739135
  # internal: 230929
  # internal: 375487
  # internal: 882911
  # internal: 356368
  # internal: 843556
  # internal: 783728
  # internal: 243570
  # internal: 910085
  # internal: 275730
  # internal: 708555
  # internal: 494616
  # internal: 772677
  # internal: 190745
  # internal: 568382
  # internal: 432120
  # internal: 569579
  # internal: 794939
  # internal: 364309
  # internal: 944919
  # internal: 887567
  # internal: 666700
  # internal: 849347
  # internal: 684257
  # internal: 965303
  # internal: 589770
  # internal: 358253
  # internal: 586204
  # internal: 577742
  # internal: 827718
  # internal: 770809
  # internal: 567944
  # internal: 117493
  # internal: 861695
  # internal: 771452
  # internal: 322736
  # internal: 966869
  # internal: 386740
  # internal: 446731
  # internal: 586466
