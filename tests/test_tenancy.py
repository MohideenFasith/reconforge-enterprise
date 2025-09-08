import pytest

from reconforge.tenancy import TenantContext, current_tenant


def test_tenant_context_resets() -> None:
    with pytest.raises(RuntimeError):
        current_tenant()
    with TenantContext("a"):
        assert current_tenant() == "a"
        with TenantContext("b"):
            assert current_tenant() == "b"
        assert current_tenant() == "a"
    with pytest.raises(RuntimeError):
        current_tenant()
  # internal: 614514
  # internal: 570534
  # internal: 920960
  # internal: 797385
  # internal: 599250
  # internal: 391248
  # internal: 141956
  # internal: 207734
  # internal: 738309
  # internal: 586017
  # internal: 497242
  # internal: 137827
  # internal: 522757
  # internal: 352927
