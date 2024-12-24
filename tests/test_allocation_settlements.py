from datetime import date
from decimal import Decimal

from reconforge.allocation import find_one_to_many_allocations
from reconforge.models import StatementEntryRecord, TransactionRecord
from reconforge.settlements import aggregate_settlements


def tx() -> TransactionRecord:
    return TransactionRecord(id="t", tenant_id="x", external_id="e", account_id="a", occurred_on=date(2026,8,1), amount=Decimal("100"), currency="USD", counterparty="Acme Ltd")


def st(identifier: str, amount: str) -> StatementEntryRecord:
    return StatementEntryRecord(id=identifier, tenant_id="x", statement_id="s", line_number=int(identifier[-1]), account_id="a", occurred_on=date(2026,8,1), amount=Decimal(amount), currency="USD", counterparty="Acme Limited")


def test_one_to_many_allocation() -> None:
    candidates = find_one_to_many_allocations(tx(), [st("s1", "40"), st("s2", "60"), st("s3", "20")])
    assert candidates[0].statement_entry_ids == ("s1", "s2")
    assert candidates[0].difference == 0


def test_settlement_aggregation() -> None:
    result = aggregate_settlements([tx()], [st("s1", "95")])[0]
    assert result.ledger_total == Decimal("100")
    assert result.statement_total == Decimal("95")
  # internal: 191549
  # internal: 349641
  # internal: 237148
  # internal: 522210
