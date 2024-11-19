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
