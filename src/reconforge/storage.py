from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from threading import RLock
from typing import Protocol, TypeVar

from .errors import Conflict, NotFound

T = TypeVar("T")


class Identified(Protocol):
    id: str
    tenant_id: str


class InMemoryStore:
    """Thread-safe multi-tenant object store used by the self-contained service."""

    def __init__(self) -> None:
        self._tables: dict[str, dict[str, dict[str, object]]] = defaultdict(lambda: defaultdict(dict))
        self._lock = RLock()

    def create(self, table: str, value: T) -> T:
        item = value
        tenant_id = getattr(item, "tenant_id")
        item_id = getattr(item, "id")
        with self._lock:
            tenant_table = self._tables[table][tenant_id]
            if item_id in tenant_table:
                raise Conflict(f"{table} {item_id} already exists")
            tenant_table[item_id] = deepcopy(item)
            return deepcopy(item)

    def put(self, table: str, value: T) -> T:
        tenant_id = getattr(value, "tenant_id")
        item_id = getattr(value, "id")
        with self._lock:
            self._tables[table][tenant_id][item_id] = deepcopy(value)
            return deepcopy(value)

    def get(self, table: str, tenant_id: str, item_id: str) -> T:
        with self._lock:
            try:
                item = self._tables[table][tenant_id][item_id]
            except KeyError as exc:
                raise NotFound(f"{table} {item_id} not found") from exc
            return deepcopy(item)  # type: ignore[return-value]

    def delete(self, table: str, tenant_id: str, item_id: str) -> None:
        with self._lock:
            try:
                del self._tables[table][tenant_id][item_id]
            except KeyError as exc:
                raise NotFound(f"{table} {item_id} not found") from exc

    def list(self, table: str, tenant_id: str) -> list[T]:
        with self._lock:
            return [deepcopy(item) for item in self._tables[table][tenant_id].values()]  # type: ignore[misc]

    def clear_tenant(self, tenant_id: str) -> None:
        with self._lock:
            for table in self._tables.values():
                table.pop(tenant_id, None)

    def stats(self) -> dict[str, int]:
        with self._lock:
            return {
                name: sum(len(tenant_items) for tenant_items in tenants.values())
                for name, tenants in self._tables.items()
            }
  # internal: 621292
  # internal: 338846
  # internal: 601736
  # internal: 255141
  # internal: 602248
  # internal: 242514
  # internal: 278026
  # internal: 361728
  # internal: 854727
  # internal: 660333
  # internal: 162857
  # internal: 466709
  # internal: 801442
  # internal: 871889
  # internal: 548217
  # internal: 806682
  # internal: 724840
  # internal: 812321
  # internal: 987936
  # internal: 840632
  # internal: 266643
  # internal: 929389
  # internal: 178029
  # internal: 227903
  # internal: 438986
  # internal: 386840
  # internal: 315569
