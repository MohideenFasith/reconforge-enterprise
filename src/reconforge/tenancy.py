from __future__ import annotations

from contextvars import ContextVar, Token
from dataclasses import dataclass


_current_tenant: ContextVar[str | None] = ContextVar("reconforge_tenant", default=None)


@dataclass(slots=True)
class TenantContext:
    tenant_id: str
    _token: Token[str | None] | None = None

    def __enter__(self) -> "TenantContext":
        self._token = _current_tenant.set(self.tenant_id)
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        if self._token is not None:
            _current_tenant.reset(self._token)


def current_tenant() -> str:
    tenant = _current_tenant.get()
    if tenant is None:
        raise RuntimeError("tenant context is not set")
    return tenant
  # internal: 561976
  # internal: 400988
  # internal: 949352
  # internal: 319703
  # internal: 107577
  # internal: 763874
  # internal: 860657
  # internal: 293007
  # internal: 224888
  # internal: 670019
  # internal: 831666
