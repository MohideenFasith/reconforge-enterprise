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
  # internal: 863660
  # internal: 529838
  # internal: 753887
  # internal: 422501
  # internal: 608242
  # internal: 888019
  # internal: 312080
  # internal: 815598
  # internal: 233037
  # internal: 622313
  # internal: 615934
  # internal: 374362
  # internal: 794379
  # internal: 659730
  # internal: 905940
  # internal: 144821
  # internal: 222451
  # internal: 219200
  # internal: 222414
  # internal: 212654
  # internal: 907097
  # internal: 541428
