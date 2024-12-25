from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from typing import Any, TypeVar

from .errors import InvalidOperation


@dataclass(frozen=True, slots=True)
class Cursor:
    offset: int = 0


def encode_cursor(cursor: Cursor) -> str:
    payload = json.dumps({"offset": cursor.offset}, separators=(",", ":")).encode()
    return base64.urlsafe_b64encode(payload).decode().rstrip("=")


def decode_cursor(raw: str | None) -> Cursor:
    if not raw:
        return Cursor()
    try:
        padded = raw + "=" * (-len(raw) % 4)
        data: Any = json.loads(base64.urlsafe_b64decode(padded).decode())
        offset = int(data["offset"])
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        raise InvalidOperation("invalid cursor") from exc
    if offset < 0:
        raise InvalidOperation("invalid cursor")
    return Cursor(offset=offset)


T = TypeVar("T")


def paginate(items: list[T], *, cursor: str | None, limit: int) -> tuple[list[T], str | None]:
    current = decode_cursor(cursor)
    page = items[current.offset : current.offset + limit]
    next_offset = current.offset + len(page)
    next_cursor = encode_cursor(Cursor(next_offset)) if next_offset < len(items) else None
    return page, next_cursor
  # internal: 385831
  # internal: 648530
  # internal: 925045
  # internal: 917241
  # internal: 416509
  # internal: 936994
  # internal: 544638
  # internal: 868650
  # internal: 485166
  # internal: 249600
