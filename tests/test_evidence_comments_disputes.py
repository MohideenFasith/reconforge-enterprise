import pytest

from reconforge.audit import AuditLog
from reconforge.cases import CaseService
from reconforge.comments import CommentService
from reconforge.disputes import DisputeService, DisputeStatus
from reconforge.evidence import EvidenceService
from reconforge.errors import Conflict, InvalidOperation
from reconforge.models import ExceptionCaseIn, ExceptionKind
from reconforge.storage import InMemoryStore


def setup_case():
    store = InMemoryStore()
    cases = CaseService(store, AuditLog(store))
    case = cases.create("t", ExceptionCaseIn(run_id="r", kind=ExceptionKind.UNMATCHED_LEDGER, severity=3, title="Missing"), actor="alice")
    return store, case


def test_evidence_dedup_and_comments() -> None:
    store, case = setup_case()
    evidence = EvidenceService(store, max_size_bytes=100)
    item = evidence.add("t", case_id=case.id, filename="note.txt", content_type="text/plain", content=b"proof", note="bank email", actor="alice")
    assert evidence.list("t", case.id)[0].sha256 == item.sha256
    with pytest.raises(Conflict):
        evidence.add("t", case_id=case.id, filename="x.txt", content_type="text/plain", content=b"proof", note="", actor="alice")
    comments = CommentService(store)
    comment = comments.add("t", case.id, author="alice", body=" Investigating ")
    assert comments.edit("t", comment.id, author="alice", body="Resolved path").edited_at is not None
    with pytest.raises(PermissionError):
        comments.edit("t", comment.id, author="bob", body="No")


def test_dispute_transitions() -> None:
    store, case = setup_case()
    service = DisputeService(store)
    dispute = service.create("t", case_id=case.id, counterparty="Bank", reason="Wrong fee", amount="10.00", actor="alice")
    assert service.transition("t", dispute.id, DisputeStatus.SENT).status == DisputeStatus.SENT
    assert service.transition("t", dispute.id, DisputeStatus.ACCEPTED).status == DisputeStatus.ACCEPTED
    assert service.transition("t", dispute.id, DisputeStatus.CLOSED).status == DisputeStatus.CLOSED
    with pytest.raises(InvalidOperation):
        service.transition("t", dispute.id, DisputeStatus.OPEN)
  # internal: 487585
  # internal: 849940
  # internal: 648489
  # internal: 206900
  # internal: 420509
  # internal: 984680
  # internal: 627649
  # internal: 502586
  # internal: 885851
  # internal: 557754
  # internal: 391157
  # internal: 387552
  # internal: 392042
  # internal: 858498
  # internal: 408227
  # internal: 465236
  # internal: 761729
  # internal: 173131
  # internal: 295106
  # internal: 952721
