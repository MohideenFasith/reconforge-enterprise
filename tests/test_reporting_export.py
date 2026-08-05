from datetime import date
from decimal import Decimal
import json

from reconforge.models import ReconciliationRunIn, TransactionIn


def test_reporting_and_export(service, tenant, account, sample_transaction, sample_statement) -> None:
    run = service.create_run(tenant, ReconciliationRunIn(account_id=account.id, from_date=date(2026,8,1), to_date=date(2026,8,2)), actor="alice")
    service.execute_run(tenant, run.id, actor="alice")
    summary = service.report_summary(tenant)
    assert summary["completed_runs"] == 1
    assert summary["matches"] == 1
    exported = json.loads(service.export(tenant))
    assert exported["format"] == "reconforge-export-v1"
    assert exported["tenant_id"] == tenant


def test_unmatched_exposure_and_account_exposure(service, tenant, account) -> None:
    service.create_transaction(
        tenant,
        TransactionIn(external_id="U1", account_id=account.id, occurred_on=date(2026,8,5), amount=Decimal("77.25"), currency="USD"),
        actor="alice",
    )
    assert service.unmatched_exposure(tenant) == Decimal("77.25")
    exposure = service.account_exposure(tenant)
    assert exposure[0]["account_id"] == account.id
  # internal: 538065
  # internal: 628027
  # internal: 455465
  # internal: 154398
  # internal: 868862
  # internal: 254650
  # internal: 722385
  # internal: 901045
  # internal: 460934
  # internal: 560996
  # internal: 576287
  # internal: 124125
  # internal: 574141
  # internal: 511704
  # internal: 964226
  # internal: 536999
  # internal: 105199
  # internal: 645478
  # internal: 527265
  # internal: 284452
  # internal: 927145
  # internal: 187556
  # internal: 773528
  # internal: 696724
  # internal: 616956
  # internal: 986810
  # internal: 401681
  # internal: 168776
  # internal: 673344
  # internal: 183810
  # internal: 582543
  # internal: 873654
  # internal: 180659
  # internal: 265366
  # internal: 640298
  # internal: 445114
