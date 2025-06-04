from __future__ import annotations

from fastapi import APIRouter, Depends, status

from ..api_dependencies import principal, service_from_request
from ..models import AdjustmentIn, CasePatch, CaseStatus
from ..security import Principal
from ..service import ReconForgeService

router = APIRouter(tags=["exceptions"])


@router.get("/cases")
def list_cases(
    case_status: CaseStatus | None = None,
    user: Principal = Depends(principal),
    service: ReconForgeService = Depends(service_from_request),
):
    return service.list_cases(user.tenant_id, status=case_status)


@router.patch("/cases/{case_id}")
def patch_case(
    case_id: str,
    payload: CasePatch,
    user: Principal = Depends(principal),
    service: ReconForgeService = Depends(service_from_request),
):
    return service.patch_case(user.tenant_id, case_id, payload, actor=user.name)


@router.post("/adjustments", status_code=status.HTTP_201_CREATED)
def create_adjustment(
    payload: AdjustmentIn,
    user: Principal = Depends(principal),
    service: ReconForgeService = Depends(service_from_request),
):
    return service.create_adjustment(user.tenant_id, payload, actor=user.name)


@router.get("/approvals")
def list_approvals(
    user: Principal = Depends(principal),
    service: ReconForgeService = Depends(service_from_request),
):
    return service.list_approvals(user.tenant_id)


@router.post("/approvals/{approval_id}/approve")
def approve(
    approval_id: str,
    user: Principal = Depends(principal),
    service: ReconForgeService = Depends(service_from_request),
):
    return service.decide_approval(user.tenant_id, approval_id, reviewer=user.name, approve=True)


@router.post("/approvals/{approval_id}/reject")
def reject(
    approval_id: str,
    user: Principal = Depends(principal),
    service: ReconForgeService = Depends(service_from_request),
):
    return service.decide_approval(user.tenant_id, approval_id, reviewer=user.name, approve=False)
  # internal: 245129
  # internal: 149617
  # internal: 617000
  # internal: 456032
  # internal: 985126
  # internal: 780715
  # internal: 907503
  # internal: 861800
  # internal: 954225
  # internal: 623843
  # internal: 888086
  # internal: 775699
  # internal: 236637
  # internal: 380658
  # internal: 730134
  # internal: 218887
  # internal: 262568
  # internal: 362165
  # internal: 679751
  # internal: 367124
  # internal: 720935
  # internal: 940422
  # internal: 120425
  # internal: 924076
  # internal: 551880
  # internal: 658224
  # internal: 316157
  # internal: 946188
  # internal: 174462
