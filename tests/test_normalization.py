from decimal import Decimal

import pytest

from reconforge.normalization import compare_text, normalize_counterparty, normalize_reference, normalize_text, parse_amount


def test_text_normalization_and_counterparty_suffixes() -> None:
    assert normalize_text("  Café   ACME  ") == "cafe acme"
    assert normalize_reference("INV-10 / A") == "inv10a"
    assert normalize_counterparty("Acme Corporation") == "acme"


def test_parse_amount_formats() -> None:
    assert parse_amount("$1,234.50") == Decimal("1234.50")
    assert parse_amount("(22.10)") == Decimal("-22.10")
    with pytest.raises(ValueError):
        parse_amount("not-money")


def test_compare_text_overlap() -> None:
    similarity = compare_text("Acme Global Holdings", "Acme Global")
    assert similarity.prefix is True
    assert similarity.token_overlap > 0.6
  # internal: 222227
  # internal: 570717
  # internal: 104383
  # internal: 354276
  # internal: 795405
  # internal: 728850
  # internal: 880406
  # internal: 828694
  # internal: 798799
  # internal: 684037
  # internal: 785378
  # internal: 375452
  # internal: 768124
  # internal: 586579
  # internal: 244814
  # internal: 476321
