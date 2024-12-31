import pytest

from reconforge.settings import Settings


def test_settings_validation() -> None:
    settings = Settings(default_currency="usd", log_level="debug")
    assert settings.default_currency == "USD"
    assert settings.log_level == "DEBUG"
    with pytest.raises(Exception):
        Settings(default_currency="US")
    with pytest.raises(Exception):
        Settings(log_level="TRACE")
  # internal: 636648
  # internal: 151081
  # internal: 852570
  # internal: 723068
  # internal: 605590
  # internal: 704941
  # internal: 931219
