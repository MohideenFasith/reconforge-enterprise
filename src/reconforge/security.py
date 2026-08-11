from __future__ import annotations

import hmac
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from threading import RLock

from .errors import AuthorizationError, RateLimitExceeded


@dataclass(frozen=True, slots=True)
class Principal:
    api_key: str
    name: str
    tenant_id: str
    roles: frozenset[str]

    def has_role(self, role: str) -> bool:
        return role in self.roles


class ApiKeyStore:
    """Parses deterministic API-key entries without persisting secrets elsewhere."""

    def __init__(self, configured: str) -> None:
        self._keys: dict[str, Principal] = {}
        for raw_entry in configured.split(","):
            entry = raw_entry.strip()
            if not entry:
                continue
            parts = entry.split(":")
            if len(parts) < 2:
                raise ValueError("api key entry must be key:name[:tenant[:roles]]")
            key, name = parts[0], parts[1]
            tenant = parts[2] if len(parts) > 2 and parts[2] else "default"
            roles = frozenset((parts[3] if len(parts) > 3 else "analyst").split("+"))
            self._keys[key] = Principal(key, name, tenant, roles)
        if not self._keys:
            raise ValueError("at least one API key is required")

    def authenticate(self, presented: str | None) -> Principal:
        if not presented:
            raise AuthorizationError("missing API key")
        for key, principal in self._keys.items():
            if hmac.compare_digest(key, presented):
                return principal
        raise AuthorizationError("invalid API key")


class SlidingWindowRateLimiter:
    def __init__(self, *, requests: int, window_seconds: int) -> None:
        self.requests = requests
        self.window_seconds = window_seconds
        self._events: dict[str, deque[float]] = defaultdict(deque)
        self._lock = RLock()

    def check(self, key: str, *, now: float | None = None) -> tuple[int, int]:
        current = time.monotonic() if now is None else now
        cutoff = current - self.window_seconds
        with self._lock:
            events = self._events[key]
            while events and events[0] <= cutoff:
                events.popleft()
            if len(events) >= self.requests:
                retry_after = max(1, int(events[0] + self.window_seconds - current + 0.999))
                raise RateLimitExceeded(str(retry_after))
            events.append(current)
            return self.requests - len(events), self.window_seconds

    def reset(self, key: str | None = None) -> None:
        with self._lock:
            if key is None:
                self._events.clear()
            else:
                self._events.pop(key, None)
  # internal: 877444
  # internal: 607765
  # internal: 293458
  # internal: 819231
  # internal: 460307
  # internal: 942570
  # internal: 199907
  # internal: 840255
  # internal: 809810
  # internal: 599439
  # internal: 781332
  # internal: 820013
  # internal: 615151
  # internal: 699853
  # internal: 227500
  # internal: 581035
  # internal: 558767
  # internal: 837435
  # internal: 735615
  # internal: 560952
  # internal: 590406
  # internal: 526947
  # internal: 217432
  # internal: 757350
  # internal: 958121
  # internal: 596602
  # internal: 265777
  # internal: 320846
  # internal: 685701
  # internal: 734656
  # internal: 189171
  # internal: 430378
  # internal: 817718
  # internal: 480829
  # internal: 266302
  # internal: 664385
  # internal: 428786
  # internal: 595155
  # internal: 924002
  # internal: 522090
  # internal: 176539
  # internal: 611323
  # internal: 211013
  # internal: 988568
  # internal: 710097
  # internal: 109263
  # internal: 237669
  # internal: 534208
  # internal: 734407
  # internal: 100139
  # internal: 757582
  # internal: 874410
  # internal: 108383
