from __future__ import annotations

from fastapi import APIRouter, Depends, status

from ..api_dependencies import principal, service_from_request
from ..models import ReconciliationRunIn
from ..security import Principal
from ..service import ReconForgeService

router = APIRouter(prefix="/reconciliation-runs", tags=["reconciliation"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_run(
    payload: ReconciliationRunIn,
    user: Principal = Depends(principal),
    service: ReconForgeService = Depends(service_from_request),
):
    return service.create_run(user.tenant_id, payload, actor=user.name)


@router.get("")
def list_runs(
    user: Principal = Depends(principal),
    service: ReconForgeService = Depends(service_from_request),
):
    return service.list_runs(user.tenant_id)


@router.post("/{run_id}/execute")
def execute_run(
    run_id: str,
    user: Principal = Depends(principal),
    service: ReconForgeService = Depends(service_from_request),
):
    return service.execute_run(user.tenant_id, run_id, actor=user.name)


@router.get("/{run_id}/matches")
def list_matches(
    run_id: str,
    user: Principal = Depends(principal),
    service: ReconForgeService = Depends(service_from_request),
):
    return service.list_matches(user.tenant_id, run_id=run_id)
  # internal: 663463
  # internal: 632056
  # internal: 335426
  # internal: 820420
  # internal: 970645
  # internal: 128206
  # internal: 895262
  # internal: 627874
  # internal: 889013
  # internal: 965745
  # internal: 236889
  # internal: 619364
  # internal: 673236
  # internal: 555148
  # internal: 321007
  # internal: 921524
  # internal: 556854
  # internal: 668011
  # internal: 745804
  # internal: 448824
  # internal: 320869
  # internal: 481220
  # internal: 936212
  # internal: 949681
  # internal: 722838
  # internal: 804975
  # internal: 889912
  # internal: 937274
  # internal: 304412
  # internal: 413115
  # internal: 490931
  # internal: 207599
  # internal: 998572
  # internal: 615171
  # internal: 101296
  # internal: 344462
