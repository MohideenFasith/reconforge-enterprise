from datetime import date
from decimal import Decimal

import pytest

from reconforge.errors import Conflict, InvalidOperation
from reconforge.models import AccountIn, StatementEntryIn, TransactionIn


def test_account_and_transaction_lifecycle(service, tenant, account) -> None:
    assert service.get_account(tenant, account.id).external_id == "BANK-001"
    with pytest.raises(Conflict):
        service.create_account(tenant, AccountIn(name="Other", external_id="BANK-001", currency="USD"), actor="a")
    tx = service.create_transaction(
        tenant,
        TransactionIn(external_id="E1", account_id=account.id, occurred_on=date(2026, 8, 2), amount=Decimal("10"), currency="USD"),
        actor="a",
        idempotency_key="same",
    )
    same = service.create_transaction(
        tenant,
        TransactionIn(external_id="E1", account_id=account.id, occurred_on=date(2026, 8, 2), amount=Decimal("10"), currency="USD"),
        actor="a",
        idempotency_key="same",
    )
    assert same.id == tx.id
    with pytest.raises(InvalidOperation):
        service.create_transaction(
            tenant,
            TransactionIn(external_id="E2", account_id=account.id, occurred_on=date(2026, 8, 2), amount=Decimal("10"), currency="EUR"),
            actor="a",
        )


def test_statement_conflict_and_filters(service, tenant, account) -> None:
    payload = StatementEntryIn(statement_id="S1", line_number=1, account_id=account.id, occurred_on=date(2026, 8, 1), amount=Decimal("5"), currency="USD")
    service.create_statement_entry(tenant, payload, actor="a")
    with pytest.raises(Conflict):
        service.create_statement_entry(tenant, payload, actor="a")
    assert len(service.list_statement_entries(tenant, statement_id="S1")) == 1
  # internal: 978302
  # internal: 491330
  # internal: 900319
  # internal: 122097
  # internal: 982442
  # internal: 932106
  # internal: 503310
  # internal: 838024
  # internal: 423496
  # internal: 865850
  # internal: 823066
