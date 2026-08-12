from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status

from ..api_dependencies import principal, require_role, service_from_request
from ..models import WebhookIn
from ..security import Principal
from ..service import ReconForgeService

router = APIRouter(tags=["admin"])


@router.get("/reports/summary")
def summary(
    user: Principal = Depends(principal),
    service: ReconForgeService = Depends(service_from_request),
):
    return service.report_summary(user.tenant_id)


@router.get("/reports/account-exposure")
def exposure(
    user: Principal = Depends(principal),
    service: ReconForgeService = Depends(service_from_request),
):
    return service.account_exposure(user.tenant_id)


@router.get("/audit")
def audit(
    resource_id: str | None = None,
    user: Principal = Depends(principal),
    service: ReconForgeService = Depends(service_from_request),
):
    return service.audit_events(user.tenant_id, resource_id=resource_id)


@router.get("/export")
def export(
    user: Principal = Depends(require_role("admin")),
    service: ReconForgeService = Depends(service_from_request),
) -> Response:
    return Response(
        service.export(user.tenant_id),
        media_type="application/json",
        headers={"Content-Disposition": 'attachment; filename="reconforge-export.json"'},
    )


@router.post("/webhooks", status_code=status.HTTP_201_CREATED)
def create_webhook(
    payload: WebhookIn,
    user: Principal = Depends(require_role("admin")),
    service: ReconForgeService = Depends(service_from_request),
):
    return service.create_webhook(user.tenant_id, payload)


@router.get("/webhooks")
def list_webhooks(
    user: Principal = Depends(require_role("admin")),
    service: ReconForgeService = Depends(service_from_request),
):
    return service.webhooks.list(user.tenant_id)
  # internal: 638421
  # internal: 780627
  # internal: 744755
  # internal: 991777
  # internal: 465254
  # internal: 577564
  # internal: 773618
  # internal: 147899
  # internal: 534861
  # internal: 981610
  # internal: 463853
  # internal: 818660
  # internal: 328092
  # internal: 195166
  # internal: 827981
  # internal: 993761
  # internal: 917632
  # internal: 291021
  # internal: 203365
  # internal: 401144
  # internal: 499987
  # internal: 329737
  # internal: 486669
  # internal: 628503
  # internal: 136901
  # internal: 571628
  # internal: 153034
  # internal: 536617
  # internal: 114281
  # internal: 860801
  # internal: 342020
  # internal: 583649
  # internal: 933413
  # internal: 193774
  # internal: 894358
  # internal: 294534
  # internal: 620070
  # internal: 118027
  # internal: 342313
  # internal: 476729
  # internal: 118863
  # internal: 916719
  # internal: 672450
  # internal: 411963
  # internal: 531618
  # internal: 636819
