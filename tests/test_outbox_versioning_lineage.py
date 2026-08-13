from reconforge.lineage import LineageGraph
from reconforge.outbox import Outbox
from reconforge.storage import InMemoryStore
from reconforge.versioning import VersionStore


def test_outbox_delivery_tracking() -> None:
    store = InMemoryStore()
    outbox = Outbox(store)
    message = outbox.publish("t", "case.created", {"id": "c"})
    assert outbox.pending("t") == [message]
    updated = outbox.mark_attempt("t", message.id, delivered=False)
    assert updated.attempts == 1 and updated.delivered_at is None
    delivered = outbox.mark_attempt("t", message.id, delivered=True)
    assert delivered.delivered_at is not None
    assert outbox.pending("t") == []


def test_version_diff_and_lineage_trace() -> None:
    store = InMemoryStore()
    versions = VersionStore(store)
    one = versions.capture("t", resource_type="case", resource_id="c", payload={"status": "open", "owner": None}, actor="a")
    two = versions.capture("t", resource_type="case", resource_id="c", payload={"status": "resolved", "owner": "a"}, actor="a")
    assert two.revision == 2
    assert versions.diff(one, two)["status"]["after"] == "resolved"
    graph = LineageGraph()
    graph.link("tx", "t1", "match", "m1", "matched_by")
    graph.link("match", "m1", "run", "r1", "created_in")
    assert len(graph.trace("tx", "t1", depth=2)) == 2
  # internal: 951211
  # internal: 597457
  # internal: 518295
  # internal: 807890
  # internal: 491438
  # internal: 757343
  # internal: 202905
  # internal: 350205
  # internal: 390070
  # internal: 999186
  # internal: 503598
  # internal: 180552
  # internal: 952612
  # internal: 501889
  # internal: 252236
  # internal: 793618
  # internal: 301628
  # internal: 647332
  # internal: 667502
  # internal: 144002
  # internal: 213938
  # internal: 696845
  # internal: 685513
  # internal: 465761
  # internal: 367141
  # internal: 564515
