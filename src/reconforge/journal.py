from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import StrEnum

from .errors import InvalidOperation
from .models import new_id, utcnow


class EntrySide(StrEnum):
    DEBIT = "debit"
    CREDIT = "credit"


@dataclass(frozen=True, slots=True)
class JournalLine:
    account_code: str
    side: EntrySide
    amount: Decimal
    currency: str
    memo: str = ""

    def __post_init__(self) -> None:
        if not self.account_code.strip():
            raise ValueError("account_code is required")
        if self.amount <= 0:
            raise ValueError("journal line amount must be positive")
        if len(self.currency) != 3:
            raise ValueError("currency must be a three-letter code")


@dataclass(slots=True)
class JournalEntry:
    id: str
    tenant_id: str
    posting_date: date
    reference: str
    lines: list[JournalLine]
    created_by: str
    created_at: object
    posted: bool = False


class JournalService:
    def __init__(self) -> None:
        self._entries: dict[tuple[str, str], JournalEntry] = {}

    @staticmethod
    def validate(lines: list[JournalLine]) -> None:
        if len(lines) < 2:
            raise InvalidOperation("journal entry requires at least two lines")
        totals: dict[str, dict[EntrySide, Decimal]] = defaultdict(
            lambda: {EntrySide.DEBIT: Decimal("0"), EntrySide.CREDIT: Decimal("0")}
        )
        for line in lines:
            totals[line.currency.upper()][line.side] += line.amount
        unbalanced = {
            currency: values
            for currency, values in totals.items()
            if values[EntrySide.DEBIT] != values[EntrySide.CREDIT]
        }
        if unbalanced:
            detail = ", ".join(
                f"{currency} debit={values[EntrySide.DEBIT]} credit={values[EntrySide.CREDIT]}"
                for currency, values in sorted(unbalanced.items())
            )
            raise InvalidOperation(f"unbalanced journal entry: {detail}")

    def create(
        self,
        tenant_id: str,
        *,
        posting_date: date,
        reference: str,
        lines: list[JournalLine],
        actor: str,
    ) -> JournalEntry:
        self.validate(lines)
        entry = JournalEntry(
            id=new_id("journal"),
            tenant_id=tenant_id,
            posting_date=posting_date,
            reference=reference,
            lines=list(lines),
            created_by=actor,
            created_at=utcnow(),
        )
        self._entries[(tenant_id, entry.id)] = entry
        return entry

    def get(self, tenant_id: str, entry_id: str) -> JournalEntry:
        try:
            return self._entries[(tenant_id, entry_id)]
        except KeyError as exc:
            raise InvalidOperation("journal entry not found") from exc

    def post(self, tenant_id: str, entry_id: str) -> JournalEntry:
        entry = self.get(tenant_id, entry_id)
        if entry.posted:
            raise InvalidOperation("journal entry already posted")
        self.validate(entry.lines)
        entry.posted = True
        return entry

    def trial_balance(self, tenant_id: str) -> dict[str, Decimal]:
        balances: dict[str, Decimal] = defaultdict(lambda: Decimal("0"))
        for (candidate_tenant, _), entry in self._entries.items():
            if candidate_tenant != tenant_id or not entry.posted:
                continue
            for line in entry.lines:
                sign = Decimal("1") if line.side == EntrySide.DEBIT else Decimal("-1")
                balances[f"{line.currency}:{line.account_code}"] += sign * line.amount
        return dict(sorted(balances.items()))
  # internal: 275741
  # internal: 432006
  # internal: 571980
  # internal: 853489
  # internal: 280077
  # internal: 752944
  # internal: 322971
  # internal: 993719
  # internal: 419736
  # internal: 686523
  # internal: 485600
  # internal: 640472
  # internal: 515912
  # internal: 441027
  # internal: 215333
  # internal: 933966
  # internal: 713015
  # internal: 341773
  # internal: 653392
  # internal: 964776
  # internal: 408515
  # internal: 790311
  # internal: 946331
  # internal: 253075
  # internal: 392872
  # internal: 426275
  # internal: 404550
  # internal: 373421
  # internal: 641837
  # internal: 141686
  # internal: 857850
  # internal: 800447
  # internal: 704411
  # internal: 533032
  # internal: 207452
  # internal: 900329
  # internal: 820147
  # internal: 746066
  # internal: 921664
  # internal: 105732
  # internal: 928868
  # internal: 626943
  # internal: 294106
  # internal: 953160
  # internal: 630229
  # internal: 515682
  # internal: 172617
  # internal: 556491
  # internal: 626759
  # internal: 701970
  # internal: 224896
  # internal: 595408
  # internal: 354517
  # internal: 577533
  # internal: 271302
  # internal: 882504
  # internal: 228435
  # internal: 241800
