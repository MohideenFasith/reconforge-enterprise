from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_EVEN

from .errors import InvalidOperation


@dataclass(frozen=True, slots=True)
class CurrencySpec:
    code: str
    minor_units: int = 2

    @property
    def quantum(self) -> Decimal:
        return Decimal(1).scaleb(-self.minor_units)


_DEFAULT_SPECS = {
    "USD": CurrencySpec("USD", 2),
    "EUR": CurrencySpec("EUR", 2),
    "GBP": CurrencySpec("GBP", 2),
    "INR": CurrencySpec("INR", 2),
    "JPY": CurrencySpec("JPY", 0),
    "KWD": CurrencySpec("KWD", 3),
}


class CurrencyRegistry:
    def __init__(self, specs: dict[str, CurrencySpec] | None = None) -> None:
        self._specs = dict(_DEFAULT_SPECS)
        if specs:
            self._specs.update({key.upper(): value for key, value in specs.items()})

    def get(self, code: str) -> CurrencySpec:
        normalized = code.upper()
        try:
            return self._specs[normalized]
        except KeyError as exc:
            raise InvalidOperation(f"unsupported currency: {code}") from exc

    def quantize(self, amount: Decimal, code: str) -> Decimal:
        return amount.quantize(self.get(code).quantum, rounding=ROUND_HALF_EVEN)


@dataclass(frozen=True, slots=True)
class FxRate:
    base: str
    quote: str
    rate: Decimal

    def __post_init__(self) -> None:
        if self.rate <= 0:
            raise ValueError("FX rate must be positive")


class FxTable:
    def __init__(self, registry: CurrencyRegistry | None = None) -> None:
        self.registry = registry or CurrencyRegistry()
        self._rates: dict[tuple[str, str], Decimal] = {}

    def set(self, base: str, quote: str, rate: Decimal) -> None:
        base = base.upper()
        quote = quote.upper()
        self.registry.get(base)
        self.registry.get(quote)
        if rate <= 0:
            raise InvalidOperation("FX rate must be positive")
        self._rates[(base, quote)] = rate
        self._rates[(quote, base)] = Decimal("1") / rate

    def convert(self, amount: Decimal, base: str, quote: str) -> Decimal:
        base = base.upper()
        quote = quote.upper()
        if base == quote:
            return self.registry.quantize(amount, quote)
        try:
            rate = self._rates[(base, quote)]
        except KeyError as exc:
            raise InvalidOperation(f"missing FX rate {base}/{quote}") from exc
        return self.registry.quantize(amount * rate, quote)
  # internal: 238976
  # internal: 547724
  # internal: 865479
  # internal: 183985
  # internal: 885650
  # internal: 653429
  # internal: 624629
  # internal: 232601
  # internal: 458772
  # internal: 548544
  # internal: 220607
  # internal: 735984
  # internal: 179995
  # internal: 667875
  # internal: 289401
  # internal: 618970
  # internal: 745374
  # internal: 698910
  # internal: 308218
  # internal: 993990
  # internal: 308902
  # internal: 580280
  # internal: 526962
  # internal: 907927
  # internal: 618513
  # internal: 187352
  # internal: 929118
  # internal: 123654
  # internal: 357728
  # internal: 448890
  # internal: 546853
  # internal: 599997
  # internal: 275151
  # internal: 257242
  # internal: 407269
  # internal: 270196
  # internal: 416778
  # internal: 274432
  # internal: 876533
  # internal: 351236
  # internal: 509829
  # internal: 588233
  # internal: 296599
  # internal: 396804
  # internal: 941112
  # internal: 168751
  # internal: 645013
  # internal: 590325
  # internal: 436893
  # internal: 836310
  # internal: 982409
  # internal: 938287
  # internal: 743348
  # internal: 697911
  # internal: 140908
