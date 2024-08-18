import pytest

from reconforge.errors import AuthorizationError, RateLimitExceeded
from reconforge.security import ApiKeyStore, SlidingWindowRateLimiter


def test_api_key_authentication_and_roles() -> None:
    store = ApiKeyStore("secret:alice:t1:admin+analyst,other:bob:t2:analyst")
    principal = store.authenticate("secret")
    assert principal.name == "alice"
    assert principal.tenant_id == "t1"
    assert principal.has_role("admin")
    with pytest.raises(AuthorizationError):
        store.authenticate(None)
    with pytest.raises(AuthorizationError):
        store.authenticate("bad")


def test_api_key_config_validation() -> None:
    with pytest.raises(ValueError):
        ApiKeyStore("")
    with pytest.raises(ValueError):
        ApiKeyStore("bad-format")


def test_sliding_window_limits_and_resets() -> None:
    limiter = SlidingWindowRateLimiter(requests=2, window_seconds=10)
    assert limiter.check("a", now=0)[0] == 1
    assert limiter.check("a", now=1)[0] == 0
    with pytest.raises(RateLimitExceeded):
        limiter.check("a", now=2)
    assert limiter.check("b", now=2)[0] == 1
    assert limiter.check("a", now=11)[0] == 1
    limiter.reset("a")
    assert limiter.check("a", now=12)[0] == 1
    limiter.reset()
