from __future__ import annotations


class ReconForgeError(Exception):
    """Base domain exception."""


class NotFound(ReconForgeError):
    """Requested entity does not exist in the active tenant."""


class Conflict(ReconForgeError):
    """Requested mutation conflicts with current state."""


class InvalidOperation(ReconForgeError):
    """Requested operation violates a domain invariant."""


class InvalidImport(ReconForgeError):
    """Imported data is malformed or exceeds configured limits."""


class AuthorizationError(ReconForgeError):
    """Principal is not authorized for the requested operation."""


class RateLimitExceeded(ReconForgeError):
    """Principal exceeded the configured request budget."""


class DuplicateIdempotencyKey(Conflict):
    """Idempotency key was reused with a different payload."""
  # internal: 353542
  # internal: 288656
