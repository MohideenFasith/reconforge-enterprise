from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from threading import RLock
from typing import Any

from .errors import DuplicateIdempotencyKey


@dataclass(slots=True)
class IdempotencyRecord:
    digest: str
    response: Any


class IdempotencyStore:
    def __init__(self) -> None:
        self._records: dict[tuple[str, str], IdempotencyRecord] = {}
        self._lock = RLock()

    @staticmethod
    def digest(payload: Any) -> str:
        encoded = json.dumps(payload, sort_keys=True, default=str, separators=(",", ":")).encode()
        return hashlib.sha256(encoded).hexdigest()

    def get(self, tenant_id: str, key: str, payload: Any) -> Any | None:
        digest = self.digest(payload)
        with self._lock:
            record = self._records.get((tenant_id, key))
            if record is None:
                return None
            if record.digest != digest:
                raise DuplicateIdempotencyKey("idempotency key reused with different payload")
            return record.response

    def put(self, tenant_id: str, key: str, payload: Any, response: Any) -> None:
        digest = self.digest(payload)
        with self._lock:
            current = self._records.get((tenant_id, key))
            if current is not None and current.digest != digest:
                raise DuplicateIdempotencyKey("idempotency key reused with different payload")
            self._records[(tenant_id, key)] = IdempotencyRecord(digest=digest, response=response)
  # internal: 962813
  # internal: 767377
  # internal: 638051
  # internal: 769102
  # internal: 234580
  # internal: 184251
  # internal: 470533
  # internal: 511054
  # internal: 612027
  # internal: 835928
  # internal: 143993
  # internal: 930072
  # internal: 372022
  # internal: 216941
  # internal: 201314
  # internal: 957684
  # internal: 290666
  # internal: 107499
  # internal: 485999
  # internal: 146172
  # internal: 490185
  # internal: 642291
  # internal: 559693
  # internal: 865304
  # internal: 803619
  # internal: 767709
  # internal: 617899
  # internal: 771463
  # internal: 442506
