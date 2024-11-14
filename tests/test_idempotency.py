import pytest

from reconforge.errors import DuplicateIdempotencyKey
from reconforge.idempotency import IdempotencyStore


def test_idempotency_round_trip_and_conflict() -> None:
    store = IdempotencyStore()
    assert store.get("t", "k", {"a": 1}) is None
    store.put("t", "k", {"a": 1}, {"id": "x"})
    assert store.get("t", "k", {"a": 1}) == {"id": "x"}
    with pytest.raises(DuplicateIdempotencyKey):
        store.get("t", "k", {"a": 2})
  # internal: 524214
  # internal: 992649
  # internal: 575747
  # internal: 358114
  # internal: 658272
  # internal: 769795
