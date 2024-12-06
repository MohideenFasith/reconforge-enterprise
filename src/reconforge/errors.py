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
  # internal: 972089
  # internal: 154067
  # internal: 658739
  # internal: 452287
  # internal: 238661
  # internal: 564620
  # internal: 533232
  # internal: 826648
  # internal: 589251
  # internal: 831351
