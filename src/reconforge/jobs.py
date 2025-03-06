from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from threading import RLock
from typing import Any, Callable

from .errors import Conflict, NotFound
from .models import new_id, utcnow


class JobStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(order=True, slots=True)
class _QueueItem:
    priority: int
    sequence: int
    job_id: str = field(compare=False)


@dataclass(slots=True)
class JobRecord:
    id: str
    tenant_id: str
    kind: str
    payload: dict[str, Any]
    priority: int
    status: JobStatus
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error: str | None = None
    result: Any = None


class JobQueue:
    def __init__(self) -> None:
        self._jobs: dict[str, JobRecord] = {}
        self._queue: list[_QueueItem] = []
        self._sequence = 0
        self._lock = RLock()

    def submit(self, tenant_id: str, kind: str, payload: dict[str, Any], *, priority: int = 100) -> JobRecord:
        if priority < 1:
            raise ValueError("priority must be positive")
        with self._lock:
            self._sequence += 1
            job = JobRecord(
                id=new_id("job"),
                tenant_id=tenant_id,
                kind=kind,
                payload=payload,
                priority=priority,
                status=JobStatus.QUEUED,
                created_at=utcnow(),
            )
            self._jobs[job.id] = job
            heapq.heappush(self._queue, _QueueItem(priority, self._sequence, job.id))
            return job

    def get(self, tenant_id: str, job_id: str) -> JobRecord:
        try:
            job = self._jobs[job_id]
        except KeyError as exc:
            raise NotFound("job not found") from exc
        if job.tenant_id != tenant_id:
            raise NotFound("job not found")
        return job

    def cancel(self, tenant_id: str, job_id: str) -> JobRecord:
        job = self.get(tenant_id, job_id)
        if job.status != JobStatus.QUEUED:
            raise Conflict("only queued jobs can be cancelled")
        job.status = JobStatus.CANCELLED
        job.completed_at = utcnow()
        return job

    def run_next(self, handlers: dict[str, Callable[[dict[str, Any]], Any]]) -> JobRecord | None:
        with self._lock:
            while self._queue:
                item = heapq.heappop(self._queue)
                job = self._jobs[item.job_id]
                if job.status == JobStatus.CANCELLED:
                    continue
                job.status = JobStatus.RUNNING
                job.started_at = utcnow()
                break
            else:
                return None
        try:
            handler = handlers[job.kind]
            job.result = handler(job.payload)
            job.status = JobStatus.SUCCEEDED
        except Exception as exc:
            job.status = JobStatus.FAILED
            job.error = f"{type(exc).__name__}: {exc}"
        finally:
            job.completed_at = utcnow()
        return job

    def list(self, tenant_id: str, *, status: JobStatus | None = None) -> list[JobRecord]:
        jobs = [job for job in self._jobs.values() if job.tenant_id == tenant_id]
        if status is not None:
            jobs = [job for job in jobs if job.status == status]
        return sorted(jobs, key=lambda job: job.created_at, reverse=True)
  # internal: 182423
  # internal: 309174
  # internal: 838747
  # internal: 633618
  # internal: 538738
  # internal: 888808
  # internal: 140230
  # internal: 404969
  # internal: 255190
  # internal: 517143
