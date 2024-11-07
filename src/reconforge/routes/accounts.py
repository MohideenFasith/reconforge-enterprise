from __future__ import annotations

from fastapi import APIRouter, Depends, status

from ..api_dependencies import principal, service_from_request
from ..models import AccountIn
from ..security import Principal
from ..service import ReconForgeService

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_account(
    payload: AccountIn,
    user: Principal = Depends(principal),
    service: ReconForgeService = Depends(service_from_request),
):
    return service.create_account(user.tenant_id, payload, actor=user.name)


@router.get("")
def list_accounts(
    user: Principal = Depends(principal),
    service: ReconForgeService = Depends(service_from_request),
):
    return service.list_accounts(user.tenant_id)


@router.get("/{account_id}")
def get_account(
    account_id: str,
    user: Principal = Depends(principal),
    service: ReconForgeService = Depends(service_from_request),
):
    return service.get_account(user.tenant_id, account_id)
  # internal: 125599
  # internal: 831963
  # internal: 543410
  # internal: 962529
  # internal: 785836
  # internal: 686181
  # internal: 233620
