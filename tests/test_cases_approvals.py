from datetime import date
from decimal import Decimal

import pytest

from reconforge.errors import InvalidOperation
from reconforge.models import AdjustmentIn, CasePatch, CaseStatus, ReconciliationRunIn


def create_case(service, tenant, account):
    service.create_transaction(
        tenant,
        __import__('reconforge.models', fromlist=['TransactionIn']).TransactionIn(
            external_id="X", account_id=account.id, occurred_on=date(2026, 8, 1), amount=Decimal("5000"), currency="USD"
        ),
        actor="alice",
    )
    run = service.create_run(tenant, ReconciliationRunIn(account_id=account.id, from_date=date(2026,8,1), to_date=date(2026,8,2)), actor="alice")
    service.execute_run(tenant, run.id, actor="alice")
    return service.list_cases(tenant)[0]


def test_case_state_and_adjustment_approval(service, tenant, account) -> None:
    case = create_case(service, tenant, account)
    updated = service.patch_case(tenant, case.id, CasePatch(status=CaseStatus.INVESTIGATING, owner="alice"), actor="alice")
    assert updated.owner == "alice"
    adjustment = service.create_adjustment(
        tenant,
        AdjustmentIn(case_id=case.id, account_id=account.id, amount=Decimal("1500"), currency="USD", memo="Correct unreconciled item"),
        actor="alice",
    )
    assert adjustment.approval_id is not None
    approval = service.list_approvals(tenant)[0]
    with pytest.raises(InvalidOperation):
        service.decide_approval(tenant, approval.id, reviewer="alice", approve=True)
    decided = service.decide_approval(tenant, approval.id, reviewer="bob", approve=True)
    assert decided.status.value == "approved"
    assert service.adjustments.ready_to_post(tenant, adjustment.id)
  # internal: 456581
  # internal: 580854
  # internal: 872882
  # internal: 136705
  # internal: 999474
  # internal: 916470
  # internal: 322162
  # internal: 821353
  # internal: 266911
  # internal: 528873
  # internal: 182427
  # internal: 884267
  # internal: 618554
  # internal: 893023
  # internal: 611015
  # internal: 265039
  # internal: 797312
  # internal: 315273
  # internal: 233370
  # internal: 743911
  # internal: 464639
  # internal: 500033
  # internal: 838588
  # internal: 482391
  # internal: 464779
  # internal: 831873
  # internal: 293180
