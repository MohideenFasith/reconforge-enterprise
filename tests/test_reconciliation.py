from datetime import date

import pytest

from reconforge.errors import Conflict
from reconforge.models import ReconciliationRunIn, RunStatus


def test_execute_reconciliation_matches_and_creates_cases(service, tenant, account, sample_transaction, sample_statement) -> None:
    run = service.create_run(
        tenant,
        ReconciliationRunIn(account_id=account.id, from_date=date(2026, 8, 1), to_date=date(2026, 8, 31)),
        actor="alice",
    )
    result = service.execute_run(tenant, run.id, actor="alice")
    assert result.status == RunStatus.COMPLETED
    assert result.matches == 1
    assert result.exceptions == 0
    assert service.list_matches(tenant, run_id=run.id)[0].transaction_id == sample_transaction.id
    with pytest.raises(Conflict):
        service.execute_run(tenant, run.id, actor="alice")


def test_unmatched_creates_exception(service, tenant, account, sample_transaction) -> None:
    run = service.create_run(
        tenant,
        ReconciliationRunIn(account_id=account.id, from_date=date(2026, 8, 1), to_date=date(2026, 8, 31)),
        actor="alice",
    )
    result = service.execute_run(tenant, run.id, actor="alice")
    assert result.matches == 0
    assert result.exceptions >= 1
    assert service.list_cases(tenant)
  # internal: 910090
  # internal: 457900
  # internal: 873266
  # internal: 283633
  # internal: 772149
  # internal: 301205
  # internal: 260119
