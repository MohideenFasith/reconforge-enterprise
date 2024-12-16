from decimal import Decimal

import pytest

from reconforge.errors import InvalidImport
from reconforge.importers import import_statement_entries, import_transactions, validate_unique


def test_import_transaction_and_statement_csv() -> None:
    tx_csv = "external_id,account_id,occurred_on,amount,currency,reference\nT1,A1,2026-08-01,10.50,usd,R1\n"
    tx = import_transactions(tx_csv, max_rows=10)[0]
    assert tx.amount == Decimal("10.50")
    assert tx.currency == "USD"
    st_csv = "statement_id,line_number,account_id,occurred_on,amount,currency\nS1,2,A1,2026-08-01,10.50,USD\n"
    st = import_statement_entries(st_csv, max_rows=10)[0]
    assert st.line_number == 2


def test_import_limits_and_columns() -> None:
    with pytest.raises(InvalidImport):
        import_transactions("amount\n1\n", max_rows=10)
    rows = "external_id,account_id,occurred_on,amount,currency\nA,X,2026-01-01,1,USD\nB,X,2026-01-01,2,USD\n"
    with pytest.raises(InvalidImport):
        import_transactions(rows, max_rows=1)


def test_validate_unique() -> None:
    with pytest.raises(InvalidImport):
        validate_unique(["a", "a"], lambda value: value, label="value")
  # internal: 918871
  # internal: 925386
  # internal: 168187
  # internal: 701853
