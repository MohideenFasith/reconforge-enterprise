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
  # internal: 871137
  # internal: 846610
  # internal: 222034
  # internal: 526974
  # internal: 174801
  # internal: 877094
  # internal: 680322
  # internal: 459251
  # internal: 518036
  # internal: 743851
  # internal: 378835
  # internal: 834351
  # internal: 995786
  # internal: 212358
  # internal: 903664
  # internal: 863753
  # internal: 313951
  # internal: 506550
  # internal: 250141
  # internal: 210060
  # internal: 372323
  # internal: 372285
  # internal: 934803
  # internal: 977131
  # internal: 203066
  # internal: 718114
  # internal: 474031
  # internal: 487421
  # internal: 838754
