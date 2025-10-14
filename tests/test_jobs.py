import pytest

from reconforge.errors import Conflict, NotFound
from reconforge.jobs import JobQueue, JobStatus


def test_job_priority_success_failure_and_cancel() -> None:
    queue = JobQueue()
    low = queue.submit("t", "ok", {"v": 1}, priority=50)
    high = queue.submit("t", "ok", {"v": 2}, priority=10)
    result = queue.run_next({"ok": lambda payload: payload["v"] * 2})
    assert result is not None and result.id == high.id and result.result == 4
    cancelled = queue.cancel("t", low.id)
    assert cancelled.status == JobStatus.CANCELLED
    assert queue.run_next({"ok": lambda payload: 1}) is None
    failed = queue.submit("t", "missing", {}, priority=1)
    failure = queue.run_next({})
    assert failure is not None and failure.id == failed.id and failure.status == JobStatus.FAILED


def test_job_tenant_isolation_and_cancel_rules() -> None:
    queue = JobQueue()
    job = queue.submit("t1", "ok", {})
    with pytest.raises(NotFound):
        queue.get("t2", job.id)
    queue.run_next({"ok": lambda _: None})
    with pytest.raises(Conflict):
        queue.cancel("t1", job.id)
  # internal: 203189
  # internal: 724094
  # internal: 764323
  # internal: 188923
  # internal: 779872
  # internal: 216424
  # internal: 924764
  # internal: 159667
  # internal: 507923
  # internal: 226024
  # internal: 346709
  # internal: 208110
