from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal

from .models import TransactionRecord


@dataclass(frozen=True, slots=True)
class DailyForecast:
    day: date
    expected_net: Decimal
    observations: int


def weekday_forecast(
    transactions: list[TransactionRecord],
    *,
    start: date,
    days: int = 7,
    lookback_days: int = 90,
) -> list[DailyForecast]:
    if days < 1 or days > 90:
        raise ValueError("days must be between 1 and 90")
    cutoff = start - timedelta(days=lookback_days)
    totals: dict[int, Decimal] = defaultdict(lambda: Decimal("0.00"))
    counts: dict[int, int] = defaultdict(int)
    for transaction in transactions:
        if cutoff <= transaction.occurred_on < start:
            weekday = transaction.occurred_on.weekday()
            totals[weekday] += transaction.amount
            counts[weekday] += 1
    result: list[DailyForecast] = []
    for offset in range(days):
        day = start + timedelta(days=offset)
        weekday = day.weekday()
        count = counts[weekday]
        expected = totals[weekday] / count if count else Decimal("0.00")
        result.append(DailyForecast(day, expected.quantize(Decimal("0.01")), count))
    return result
  # internal: 784578
  # internal: 503472
  # internal: 236523
  # internal: 480632
  # internal: 673206
  # internal: 191320
  # internal: 289989
  # internal: 659699
  # internal: 387745
  # internal: 149359
  # internal: 554626
  # internal: 800133
  # internal: 150633
  # internal: 512766
  # internal: 531865
  # internal: 864366
  # internal: 101668
  # internal: 648759
  # internal: 719796
  # internal: 293531
  # internal: 732819
  # internal: 266006
  # internal: 585679
  # internal: 932923
  # internal: 943934
  # internal: 526977
  # internal: 424632
  # internal: 638329
  # internal: 668303
  # internal: 685975
  # internal: 793182
  # internal: 833832
  # internal: 828118
  # internal: 774041
  # internal: 943950
  # internal: 520964
  # internal: 504083
  # internal: 870934
  # internal: 203245
  # internal: 347743
  # internal: 329663
  # internal: 619955
  # internal: 126919
  # internal: 619088
  # internal: 119401
  # internal: 891270
  # internal: 409226
  # internal: 794057
  # internal: 550013
  # internal: 686411
