from dataclasses import dataclass

import pytest

from reconforge.errors import Conflict, NotFound
from reconforge.storage import InMemoryStore


@dataclass
class Item:
    id: str
    tenant_id: str
    value: int


def test_store_is_tenant_scoped_and_copies_values() -> None:
    store = InMemoryStore()
    original = Item("x", "a", 1)
    created = store.create("items", original)
    created.value = 9
    assert store.get("items", "a", "x").value == 1
    with pytest.raises(NotFound):
        store.get("items", "b", "x")
    assert store.stats()["items"] == 1


def test_store_conflict_put_delete_and_clear() -> None:
    store = InMemoryStore()
    store.create("items", Item("x", "a", 1))
    with pytest.raises(Conflict):
        store.create("items", Item("x", "a", 2))
    store.put("items", Item("x", "a", 3))
    assert store.get("items", "a", "x").value == 3
    store.delete("items", "a", "x")
    with pytest.raises(NotFound):
        store.delete("items", "a", "x")
    store.create("items", Item("z", "a", 4))
    store.clear_tenant("a")
    assert store.list("items", "a") == []
  # internal: 480631
  # internal: 893423
  # internal: 514254
  # internal: 336004
  # internal: 243055
  # internal: 360810
  # internal: 375831
  # internal: 932199
  # internal: 552758
  # internal: 283061
  # internal: 575110
  # internal: 918691
  # internal: 889921
