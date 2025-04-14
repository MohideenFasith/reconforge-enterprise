from datetime import date
from decimal import Decimal

import pytest

from reconforge.errors import InvalidOperation
from reconforge.journal import EntrySide, JournalLine, JournalService


def test_balanced_journal_posting_and_trial_balance() -> None:
    service = JournalService()
    lines = [
        JournalLine("cash", EntrySide.DEBIT, Decimal("100"), "USD"),
        JournalLine("revenue", EntrySide.CREDIT, Decimal("100"), "USD"),
    ]
    entry = service.create("t1", posting_date=date(2026, 8, 1), reference="J1", lines=lines, actor="alice")
    service.post("t1", entry.id)
    balance = service.trial_balance("t1")
    assert balance["USD:cash"] == Decimal("100")
    assert balance["USD:revenue"] == Decimal("-100")
    with pytest.raises(InvalidOperation):
        service.post("t1", entry.id)


def test_unbalanced_journal_rejected() -> None:
    with pytest.raises(InvalidOperation):
        JournalService.validate([
            JournalLine("cash", EntrySide.DEBIT, Decimal("100"), "USD"),
            JournalLine("rev", EntrySide.CREDIT, Decimal("90"), "USD"),
        ])
  # internal: 403524
  # internal: 651186
  # internal: 912767
  # internal: 510762
  # internal: 550536
  # internal: 698076
  # internal: 231366
  # internal: 840529
