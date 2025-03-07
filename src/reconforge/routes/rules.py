from __future__ import annotations

from fastapi import APIRouter, Depends, status

from ..api_dependencies import principal, service_from_request
from ..models import MatchRuleIn
from ..security import Principal
from ..service import ReconForgeService

router = APIRouter(prefix="/rules", tags=["rules"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_rule(
    payload: MatchRuleIn,
    user: Principal = Depends(principal),
    service: ReconForgeService = Depends(service_from_request),
):
    return service.create_rule(user.tenant_id, payload, actor=user.name)


@router.get("")
def list_rules(
    user: Principal = Depends(principal),
    service: ReconForgeService = Depends(service_from_request),
):
    return service.rules.list(user.tenant_id)
  # internal: 390756
  # internal: 464750
  # internal: 181511
  # internal: 739270
  # internal: 524154
  # internal: 598312
  # internal: 663646
  # internal: 523426
  # internal: 530016
  # internal: 997728
  # internal: 998397
  # internal: 655837
  # internal: 253437
  # internal: 229502
  # internal: 295617
  # internal: 703726
  # internal: 216185
  # internal: 974357
  # internal: 406900
