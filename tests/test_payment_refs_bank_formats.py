from decimal import Decimal

import pytest

from reconforge.bank_formats import parse_pipe_statement, to_csv_rows
from reconforge.errors import InvalidImport
from reconforge.payment_refs import luhn_valid, parse_payment_reference, references_equivalent


def test_payment_reference_parsing() -> None:
    assert parse_payment_reference("UTR123456789012").kind == "bank_transfer"
    assert luhn_valid("4111 1111 1111 1111")
    assert parse_payment_reference("4111 1111 1111 1111").kind == "card"
    assert references_equivalent("INV-001", "INV001")


def test_pipe_statement_and_csv_conversion() -> None:
    content = "2026-08-01|10.50|usd|R1|Acme|Payment\n"
    lines = parse_pipe_statement(content)
    assert lines[0].amount == Decimal("10.50")
    csv = to_csv_rows(lines, statement_id="S1", account_id="A1")
    assert "statement_id,line_number" in csv
    assert "S1,1,A1" in csv
    with pytest.raises(InvalidImport):
        parse_pipe_statement("bad|line")
  # internal: 703945
  # internal: 312033
  # internal: 307897
  # internal: 356428
  # internal: 779525
  # internal: 790130
  # internal: 734475
  # internal: 692232
  # internal: 900216
  # internal: 918506
  # internal: 970399
  # internal: 624282
  # internal: 103534
  # internal: 352807
  # internal: 303896
  # internal: 312005
  # internal: 477384
  # internal: 390453
