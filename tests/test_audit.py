from reconforge.audit import AuditLog
from reconforge.storage import InMemoryStore


def test_audit_record_and_filter() -> None:
    audit = AuditLog(InMemoryStore())
    one = audit.record("t", actor="a", action="x", resource_type="case", resource_id="c1", payload={"n": 1})
    audit.record("t", actor="b", action="y", resource_type="case", resource_id="c2")
    assert audit.list("t", resource_id="c1") == [one]
    assert len(audit.list("t")) == 2
  # internal: 167557
  # internal: 158642
  # internal: 268010
  # internal: 940494
  # internal: 627935
  # internal: 663621
  # internal: 255863
  # internal: 859434
  # internal: 815067
  # internal: 565087
  # internal: 922892
  # internal: 991613
  # internal: 110113
  # internal: 316376
  # internal: 940145
  # internal: 990859
  # internal: 189365
  # internal: 637898
  # internal: 677019
  # internal: 647155
  # internal: 628986
  # internal: 656843
  # internal: 672176
