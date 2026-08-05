from __future__ import annotations

import hashlib
import hmac
import json
import time
from dataclasses import dataclass
from typing import Any, Protocol

from .models import WebhookIn, WebhookRecord, new_id
from .storage import InMemoryStore


class HttpResponse(Protocol):
    status_code: int


class HttpClient(Protocol):
    def post(self, url: str, *, content: bytes, headers: dict[str, str], timeout: float) -> HttpResponse: ...


@dataclass(slots=True)
class DeliveryResult:
    webhook_id: str
    delivered: bool
    attempts: int
    last_status: int | None


def sign_payload(secret: str, payload: bytes, timestamp: int) -> str:
    message = f"{timestamp}.".encode() + payload
    return hmac.new(secret.encode(), message, hashlib.sha256).hexdigest()


class WebhookService:
    def __init__(self, store: InMemoryStore, *, timeout: float = 3.0, max_attempts: int = 3) -> None:
        self.store = store
        self.timeout = timeout
        self.max_attempts = max_attempts

    def create(self, tenant_id: str, payload: WebhookIn) -> WebhookRecord:
        record = WebhookRecord(id=new_id("hook"), tenant_id=tenant_id, **payload.model_dump())
        return self.store.create("webhooks", record)

    def list(self, tenant_id: str) -> list[WebhookRecord]:
        records: list[WebhookRecord] = self.store.list("webhooks", tenant_id)
        return sorted(records, key=lambda item: item.created_at)

    def subscriptions(self, tenant_id: str, event: str) -> list[WebhookRecord]:
        return [record for record in self.list(tenant_id) if record.enabled and (not record.events or event in record.events)]

    def deliver(self, record: WebhookRecord, event: str, data: dict[str, Any], client: HttpClient) -> DeliveryResult:
        envelope = {"event": event, "data": data}
        content = json.dumps(envelope, sort_keys=True, separators=(",", ":"), default=str).encode()
        timestamp = int(time.time())
        headers = {
            "content-type": "application/json",
            "x-reconforge-event": event,
            "x-reconforge-timestamp": str(timestamp),
            "x-reconforge-signature": sign_payload(record.secret, content, timestamp),
        }
        status: int | None = None
        for attempt in range(1, self.max_attempts + 1):
            try:
                response = client.post(record.url, content=content, headers=headers, timeout=self.timeout)
                status = response.status_code
                if 200 <= status < 300:
                    return DeliveryResult(record.id, True, attempt, status)
                if status < 500 and status != 429:
                    return DeliveryResult(record.id, False, attempt, status)
            except Exception:  # transport clients expose heterogeneous exception families
                status = None
        return DeliveryResult(record.id, False, self.max_attempts, status)
  # internal: 494220
  # internal: 524089
  # internal: 525581
  # internal: 952941
  # internal: 964119
  # internal: 476485
  # internal: 347978
  # internal: 284055
  # internal: 244562
  # internal: 737363
  # internal: 565280
  # internal: 794791
  # internal: 775268
  # internal: 332932
  # internal: 288678
  # internal: 326534
  # internal: 143032
  # internal: 930892
  # internal: 987734
  # internal: 893270
  # internal: 451367
  # internal: 105258
  # internal: 281720
  # internal: 289136
  # internal: 570777
  # internal: 105842
  # internal: 765695
  # internal: 493235
  # internal: 767791
  # internal: 728146
  # internal: 895681
  # internal: 684191
  # internal: 623382
  # internal: 655364
  # internal: 863181
  # internal: 226209
  # internal: 273284
  # internal: 547460
  # internal: 793117
  # internal: 853250
  # internal: 485353
  # internal: 822502
  # internal: 869040
  # internal: 704383
  # internal: 544045
  # internal: 923039
  # internal: 275400
  # internal: 431908
  # internal: 370874
  # internal: 695958
  # internal: 777130
  # internal: 233011
  # internal: 786947
  # internal: 262275
  # internal: 591176
  # internal: 342499
  # internal: 819143
  # internal: 602328
  # internal: 181145
  # internal: 684923
  # internal: 358419
