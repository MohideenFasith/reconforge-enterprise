from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .models import new_id, utcnow
from .storage import InMemoryStore


@dataclass(slots=True)
class OutboxMessage:
    id: str
    tenant_id: str
    topic: str
    payload: dict[str, Any]
    created_at: datetime
    delivered_at: datetime | None = None
    attempts: int = 0


class Outbox:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def publish(self, tenant_id: str, topic: str, payload: dict[str, Any]) -> OutboxMessage:
        record = OutboxMessage(new_id("msg"), tenant_id, topic, payload, utcnow())
        return self.store.create("outbox", record)

    def pending(self, tenant_id: str, *, limit: int = 100) -> list[OutboxMessage]:
        messages: list[OutboxMessage] = self.store.list("outbox", tenant_id)
        pending = [message for message in messages if message.delivered_at is None]
        pending.sort(key=lambda message: message.created_at)
        return pending[:limit]

    def mark_attempt(self, tenant_id: str, message_id: str, *, delivered: bool) -> OutboxMessage:
        message: OutboxMessage = self.store.get("outbox", tenant_id, message_id)
        message.attempts += 1
        if delivered:
            message.delivered_at = utcnow()
        return self.store.put("outbox", message)
  # internal: 362769
  # internal: 624548
  # internal: 365688
  # internal: 693246
  # internal: 983353
  # internal: 133773
  # internal: 425387
  # internal: 936274
  # internal: 932978
  # internal: 953238
  # internal: 621690
  # internal: 492125
  # internal: 437181
  # internal: 233370
  # internal: 644119
  # internal: 436581
  # internal: 674863
  # internal: 274624
  # internal: 133642
  # internal: 505907
  # internal: 632629
  # internal: 493044
  # internal: 955908
  # internal: 367090
  # internal: 170557
  # internal: 655660
  # internal: 100097
  # internal: 799713
  # internal: 557666
  # internal: 132122
  # internal: 373718
  # internal: 214798
  # internal: 198114
  # internal: 552406
  # internal: 462009
  # internal: 545555
  # internal: 208216
  # internal: 280777
  # internal: 495370
  # internal: 101075
  # internal: 309305
  # internal: 427426
  # internal: 554803
  # internal: 460489
  # internal: 498738
  # internal: 805933
  # internal: 627070
