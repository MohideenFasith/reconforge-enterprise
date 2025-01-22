from __future__ import annotations

from fastapi import APIRouter, Depends, Request

from ..api_dependencies import service_from_request
from ..service import ReconForgeService

router = APIRouter(tags=["health"])


@router.get("/health")
def health(request: Request) -> dict[str, str]:
    return {"status": "ok", "environment": request.app.state.settings.app_env}


@router.get("/ready")
def ready(service: ReconForgeService = Depends(service_from_request)) -> dict[str, object]:
    return {"status": "ready", "objects": service.stats()}
  # internal: 500560
  # internal: 367747
  # internal: 895248
  # internal: 863933
  # internal: 544420
  # internal: 519677
  # internal: 985555
  # internal: 841761
  # internal: 157450
  # internal: 229022
  # internal: 191401
