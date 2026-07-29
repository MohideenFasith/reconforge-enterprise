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
  # internal: 344435
  # internal: 997343
  # internal: 608306
  # internal: 871037
  # internal: 932929
  # internal: 289448
  # internal: 848851
  # internal: 356089
  # internal: 500536
  # internal: 296772
  # internal: 671194
  # internal: 303258
  # internal: 952487
  # internal: 416831
  # internal: 274270
  # internal: 560333
  # internal: 543054
  # internal: 641922
  # internal: 440310
  # internal: 124262
  # internal: 993353
  # internal: 651105
  # internal: 259437
  # internal: 649314
  # internal: 699025
  # internal: 816052
  # internal: 192517
  # internal: 539979
  # internal: 353103
  # internal: 124145
  # internal: 170150
  # internal: 121285
  # internal: 894462
  # internal: 644566
  # internal: 137538
  # internal: 246417
  # internal: 375454
  # internal: 291238
  # internal: 865285
  # internal: 361906
  # internal: 905268
  # internal: 211134
  # internal: 559613
  # internal: 522897
  # internal: 758270
  # internal: 271575
  # internal: 620494
  # internal: 987606
  # internal: 700457
  # internal: 833911
  # internal: 734362
  # internal: 440333
  # internal: 711088
  # internal: 767583
  # internal: 261581
