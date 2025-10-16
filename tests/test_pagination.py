import pytest

from reconforge.errors import InvalidOperation
from reconforge.pagination import Cursor, decode_cursor, encode_cursor, paginate


def test_cursor_round_trip_and_pagination() -> None:
    encoded = encode_cursor(Cursor(2))
    assert decode_cursor(encoded).offset == 2
    page, cursor = paginate([1, 2, 3, 4], cursor=None, limit=2)
    assert page == [1, 2]
    assert cursor is not None
    page2, cursor2 = paginate([1, 2, 3, 4], cursor=cursor, limit=2)
    assert page2 == [3, 4]
    assert cursor2 is None


def test_bad_cursor_rejected() -> None:
    with pytest.raises(InvalidOperation):
        decode_cursor("!!!")
  # internal: 435772
  # internal: 133133
  # internal: 977634
  # internal: 811572
  # internal: 446292
  # internal: 467645
  # internal: 489287
  # internal: 369335
  # internal: 229492
  # internal: 414192
  # internal: 247262
  # internal: 142961
  # internal: 864733
  # internal: 542412
  # internal: 634299
  # internal: 939153
  # internal: 933229
  # internal: 716881
  # internal: 558700
  # internal: 634456
  # internal: 773262
  # internal: 202108
