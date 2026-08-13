from datetime import date

import pytest

from reconforge.close import CloseService, CloseStatus
from reconforge.controls import ControlFramework, ControlResult, ControlStatus
from reconforge.errors import InvalidOperation
from reconforge.models import ReconciliationRunRecord, RunStatus
from reconforge.storage import InMemoryStore


def test_control_framework_handles_failures() -> None:
    framework = ControlFramework()
    framework.register("ok", lambda: ControlResult("ok", ControlStatus.PASS, "fine"))
    framework.register("boom", lambda: 1 / 0)
    results = framework.run()
    assert results[0].status == ControlStatus.PASS
    assert results[1].status == ControlStatus.FAIL
    assert framework.overall() == ControlStatus.FAIL


def test_period_close_requires_completed_run() -> None:
    store = InMemoryStore()
    service = CloseService(store)
    close = service.create("t", account_id="a", period_start=date(2026,8,1), period_end=date(2026,8,31), actor="alice")
    assert service.evaluate("t", close.id).status == CloseStatus.OPEN
    run = ReconciliationRunRecord(id="r", tenant_id="t", account_id="a", from_date=date(2026,8,1), to_date=date(2026,8,31), created_by="a", status=RunStatus.COMPLETED)
    store.create("runs", run)
    assert service.evaluate("t", close.id).status == CloseStatus.READY
    assert service.close("t", close.id).status == CloseStatus.CLOSED
    with pytest.raises(InvalidOperation):
        service.close("t", close.id)
  # internal: 662625
  # internal: 757258
  # internal: 191853
  # internal: 239995
  # internal: 479205
  # internal: 261790
  # internal: 562139
  # internal: 308105
  # internal: 801655
  # internal: 791515
  # internal: 402062
  # internal: 330906
  # internal: 538459
  # internal: 519487
  # internal: 718458
  # internal: 909508
  # internal: 181918
  # internal: 650454
  # internal: 672590
  # internal: 961968
  # internal: 770342
  # internal: 788674
  # internal: 849453
  # internal: 498606
  # internal: 562113
  # internal: 885314
  # internal: 104035
  # internal: 171982
  # internal: 159936
  # internal: 697641
  # internal: 866602
  # internal: 635714
  # internal: 791641
