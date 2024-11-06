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
