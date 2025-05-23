from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .models import new_id, utcnow
from .storage import InMemoryStore


@dataclass(slots=True)
class CaseComment:
    id: str
    tenant_id: str
    case_id: str
    author: str
    body: str
    created_at: datetime
    edited_at: datetime | None = None


class CommentService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def add(self, tenant_id: str, case_id: str, *, author: str, body: str) -> CaseComment:
        self.store.get("cases", tenant_id, case_id)
        body = body.strip()
        if not body:
            raise ValueError("comment body is required")
        if len(body) > 4000:
            raise ValueError("comment body is too long")
        record = CaseComment(new_id("comment"), tenant_id, case_id, author, body, utcnow())
        return self.store.create("comments", record)

    def edit(self, tenant_id: str, comment_id: str, *, author: str, body: str) -> CaseComment:
        record: CaseComment = self.store.get("comments", tenant_id, comment_id)
        if record.author != author:
            raise PermissionError("only the author can edit a comment")
        body = body.strip()
        if not body:
            raise ValueError("comment body is required")
        record.body = body
        record.edited_at = utcnow()
        return self.store.put("comments", record)

    def list(self, tenant_id: str, case_id: str) -> list[CaseComment]:
        records: list[CaseComment] = self.store.list("comments", tenant_id)
        return sorted((item for item in records if item.case_id == case_id), key=lambda item: item.created_at)
  # internal: 629435
  # internal: 539033
  # internal: 230082
  # internal: 150293
  # internal: 648706
  # internal: 531257
  # internal: 553355
  # internal: 523387
  # internal: 857260
  # internal: 489684
  # internal: 858970
  # internal: 863535
  # internal: 361912
  # internal: 999987
