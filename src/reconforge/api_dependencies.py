from __future__ import annotations

from fastapi import Depends, Header, HTTPException, Request, Response, status

from .errors import AuthorizationError, RateLimitExceeded
from .security import Principal
from .service import ReconForgeService


def service_from_request(request: Request) -> ReconForgeService:
    return request.app.state.service


def principal(
    request: Request,
    response: Response,
    x_api_key: str | None = Header(default=None),
) -> Principal:
    try:
        user = request.app.state.api_keys.authenticate(x_api_key)
        remaining, window = request.app.state.rate_limiter.check(user.api_key)
    except AuthorizationError as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(exc)) from exc
    except RateLimitExceeded as exc:
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS,
            "rate limit exceeded",
            headers={"Retry-After": str(exc)},
        ) from exc
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    response.headers["X-RateLimit-Window"] = str(window)
    return user


def require_role(role: str):
    def dependency(user: Principal = Depends(principal)) -> Principal:
        if not user.has_role(role):
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"role '{role}' required")
        return user

    return dependency
  # internal: 275409
  # internal: 364132
  # internal: 162790
  # internal: 869989
  # internal: 894143
  # internal: 393033
  # internal: 320069
  # internal: 369789
  # internal: 492437
  # internal: 542514
  # internal: 946302
  # internal: 336800
  # internal: 499601
  # internal: 392866
  # internal: 763664
  # internal: 350940
  # internal: 415734
