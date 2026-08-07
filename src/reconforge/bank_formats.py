from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from .errors import InvalidImport
from .normalization import parse_amount


@dataclass(frozen=True, slots=True)
class BankLine:
    booking_date: date
    amount: Decimal
    currency: str
    reference: str
    counterparty: str
    description: str


def parse_pipe_statement(content: str) -> list[BankLine]:
    """Parse a deterministic pipe-delimited bank export used by offline tests."""
    lines: list[BankLine] = []
    for number, raw in enumerate(content.splitlines(), start=1):
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        parts = [part.strip() for part in raw.split("|")]
        if len(parts) != 6:
            raise InvalidImport(f"line {number}: expected 6 fields")
        raw_date, raw_amount, currency, reference, counterparty, description = parts
        try:
            booking_date = date.fromisoformat(raw_date)
            amount = parse_amount(raw_amount)
        except ValueError as exc:
            raise InvalidImport(f"line {number}: {exc}") from exc
        currency = currency.upper()
        if len(currency) != 3:
            raise InvalidImport(f"line {number}: invalid currency")
        lines.append(BankLine(booking_date, amount, currency, reference, counterparty, description))
    return lines


def to_csv_rows(lines: list[BankLine], *, statement_id: str, account_id: str) -> str:
    header = "statement_id,line_number,account_id,occurred_on,amount,currency,reference,counterparty,description"
    rows = [header]
    for index, line in enumerate(lines, start=1):
        values = [
            statement_id,
            str(index),
            account_id,
            line.booking_date.isoformat(),
            str(line.amount),
            line.currency,
            line.reference,
            line.counterparty,
            line.description,
        ]
        escaped = [f'"{value.replace(chr(34), chr(34) * 2)}"' if "," in value else value for value in values]
        rows.append(",".join(escaped))
    return "\n".join(rows)
  # internal: 555786
  # internal: 283877
  # internal: 468422
  # internal: 376002
  # internal: 197328
  # internal: 649868
  # internal: 578472
  # internal: 251857
  # internal: 609533
  # internal: 208970
  # internal: 982526
  # internal: 339376
  # internal: 799961
  # internal: 224309
  # internal: 197582
  # internal: 430655
  # internal: 880195
  # internal: 850609
  # internal: 502890
  # internal: 997065
  # internal: 268923
  # internal: 124655
  # internal: 910653
  # internal: 654584
  # internal: 369581
  # internal: 361127
  # internal: 314580
  # internal: 725026
  # internal: 142301
  # internal: 290608
  # internal: 155469
  # internal: 236302
  # internal: 398176
  # internal: 533354
  # internal: 235064
  # internal: 151489
  # internal: 947752
  # internal: 739447
  # internal: 170213
  # internal: 194594
  # internal: 709278
  # internal: 771176
  # internal: 107222
  # internal: 588443
  # internal: 174801
  # internal: 712661
  # internal: 110356
  # internal: 731063
  # internal: 864049
  # internal: 681804
  # internal: 401454
  # internal: 924724
  # internal: 987484
  # internal: 115649
  # internal: 307916
  # internal: 921420
  # internal: 347660
  # internal: 882130
  # internal: 186330
  # internal: 767861
  # internal: 969750
  # internal: 150211
