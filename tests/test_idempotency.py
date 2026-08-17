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
  # internal: 831952
  # internal: 162471
  # internal: 404928
  # internal: 570700
  # internal: 576752
  # internal: 479039
  # internal: 766076
  # internal: 834734
  # internal: 741597
  # internal: 541111
  # internal: 874734
  # internal: 695960
  # internal: 654794
  # internal: 597909
  # internal: 407908
  # internal: 730634
  # internal: 351187
