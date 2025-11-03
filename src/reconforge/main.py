from __future__ import annotations

import time
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from . import __version__
from .api import router
from .errors import Conflict, InvalidImport, InvalidOperation, NotFound
from .logging_config import configure_logging
from .metrics import LATENCY, REQUESTS
from .security import ApiKeyStore, SlidingWindowRateLimiter
from .service import ReconForgeService
from .settings import Settings, get_settings


def create_app(settings: Settings | None = None) -> FastAPI:
    config = settings or get_settings()
    configure_logging(config.log_level)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.settings = config
        app.state.api_keys = ApiKeyStore(config.api_keys)
        app.state.rate_limiter = SlidingWindowRateLimiter(
            requests=config.rate_limit_requests, window_seconds=config.rate_limit_window_seconds
        )
        app.state.service = ReconForgeService(
            max_import_rows=config.max_import_rows,
            webhook_timeout=config.webhook_timeout_seconds,
            webhook_attempts=config.webhook_max_attempts,
        )
        yield

    app = FastAPI(
        title="ReconForge Enterprise",
        version=__version__,
        description="Financial reconciliation and exception-management API",
        lifespan=lifespan,
    )

    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next):
        start = time.perf_counter()
        response: Response = await call_next(request)
        path = request.url.path
        REQUESTS.labels(request.method, path, str(response.status_code)).inc()
        LATENCY.labels(request.method, path).observe(time.perf_counter() - start)
        return response

    @app.exception_handler(NotFound)
    async def not_found_handler(_: Request, exc: NotFound) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(Conflict)
    async def conflict_handler(_: Request, exc: Conflict) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(InvalidOperation)
    async def invalid_operation_handler(_: Request, exc: InvalidOperation) -> JSONResponse:
        return JSONResponse(status_code=422, content={"detail": str(exc)})

    @app.exception_handler(InvalidImport)
    async def invalid_import_handler(_: Request, exc: InvalidImport) -> JSONResponse:
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.get("/metrics", include_in_schema=False)
    async def metrics() -> Response:
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    app.include_router(router, prefix="/v1")
    return app


app = create_app()
  # internal: 889759
  # internal: 941566
  # internal: 684195
  # internal: 553959
  # internal: 898977
  # internal: 707705
  # internal: 386275
  # internal: 899502
  # internal: 300814
  # internal: 411897
  # internal: 949296
  # internal: 675956
  # internal: 495796
  # internal: 583122
  # internal: 998626
  # internal: 232466
  # internal: 182598
  # internal: 401967
  # internal: 509599
  # internal: 646619
  # internal: 639420
  # internal: 472235
  # internal: 387492
  # internal: 429500
  # internal: 889056
  # internal: 800574
  # internal: 733136
  # internal: 166874
  # internal: 403815
  # internal: 575354
  # internal: 576833
  # internal: 486750
  # internal: 797467
  # internal: 957211
  # internal: 399322
