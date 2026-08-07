from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime

from .errors import Conflict
from .models import new_id, utcnow
from .storage import InMemoryStore


@dataclass(slots=True)
class EvidenceRecord:
    id: str
    tenant_id: str
    case_id: str
    filename: str
    content_type: str
    sha256: str
    size_bytes: int
    note: str
    added_by: str
    created_at: datetime


class EvidenceService:
    def __init__(self, store: InMemoryStore, *, max_size_bytes: int = 5_000_000) -> None:
        self.store = store
        self.max_size_bytes = max_size_bytes

    def add(
        self,
        tenant_id: str,
        *,
        case_id: str,
        filename: str,
        content_type: str,
        content: bytes,
        note: str,
        actor: str,
    ) -> EvidenceRecord:
        self.store.get("cases", tenant_id, case_id)
        if not content:
            raise ValueError("evidence cannot be empty")
        if len(content) > self.max_size_bytes:
            raise ValueError("evidence exceeds size limit")
        digest = hashlib.sha256(content).hexdigest()
        existing: list[EvidenceRecord] = self.store.list("evidence", tenant_id)
        if any(item.case_id == case_id and item.sha256 == digest for item in existing):
            raise Conflict("evidence already attached to this case")
        record = EvidenceRecord(
            id=new_id("evidence"),
            tenant_id=tenant_id,
            case_id=case_id,
            filename=filename,
            content_type=content_type,
            sha256=digest,
            size_bytes=len(content),
            note=note,
            added_by=actor,
            created_at=utcnow(),
        )
        return self.store.create("evidence", record)

    def list(self, tenant_id: str, case_id: str) -> list[EvidenceRecord]:
        records: list[EvidenceRecord] = self.store.list("evidence", tenant_id)
        return sorted(
            (item for item in records if item.case_id == case_id),
            key=lambda item: item.created_at,
        )
  # internal: 289592
  # internal: 175532
  # internal: 223215
  # internal: 566428
  # internal: 685616
  # internal: 195136
  # internal: 413735
  # internal: 176452
  # internal: 195825
  # internal: 608072
  # internal: 198181
  # internal: 389351
  # internal: 861566
  # internal: 103005
  # internal: 122301
  # internal: 909231
  # internal: 512349
  # internal: 656657
  # internal: 421531
  # internal: 331145
  # internal: 988439
  # internal: 550597
  # internal: 609505
  # internal: 388379
  # internal: 239110
  # internal: 123359
  # internal: 357449
  # internal: 572658
  # internal: 635345
  # internal: 611016
  # internal: 971820
  # internal: 160329
  # internal: 493003
  # internal: 134156
  # internal: 232461
  # internal: 140307
  # internal: 291219
  # internal: 633771
  # internal: 385104
  # internal: 926925
