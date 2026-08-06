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
  # internal: 927061
  # internal: 257517
  # internal: 590891
  # internal: 447283
  # internal: 993654
  # internal: 368113
  # internal: 913602
  # internal: 131350
  # internal: 129607
  # internal: 491834
  # internal: 464938
  # internal: 569511
  # internal: 914748
  # internal: 828462
  # internal: 550087
  # internal: 849591
  # internal: 975336
  # internal: 789315
  # internal: 594249
  # internal: 818378
  # internal: 144648
  # internal: 758793
  # internal: 367292
  # internal: 120945
  # internal: 575306
  # internal: 383480
  # internal: 501942
  # internal: 834435
  # internal: 277377
  # internal: 115550
  # internal: 608090
  # internal: 811890
  # internal: 582351
  # internal: 761506
  # internal: 624385
  # internal: 609255
