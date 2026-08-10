from __future__ import annotations

import re
from dataclasses import dataclass


_SEPA = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{1,30}\b")
_SWIFT = re.compile(r"\b[A-Z0-9]{8,11}\b")
_UPI = re.compile(r"\b\d{12}\b")
_CARD = re.compile(r"\b(?:\d[ -]*?){13,19}\b")


@dataclass(frozen=True, slots=True)
class ParsedReference:
    raw: str
    normalized: str
    kind: str
    confidence: float


def _alnum(value: str) -> str:
    return "".join(character for character in value.upper() if character.isalnum())


def luhn_valid(value: str) -> bool:
    digits = [int(character) for character in value if character.isdigit()]
    if len(digits) < 12:
        return False
    total = 0
    parity = len(digits) % 2
    for index, digit in enumerate(digits):
        if index % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


def parse_payment_reference(value: str) -> ParsedReference:
    raw = value.strip()
    normalized = _alnum(raw)
    if _SEPA.search(raw.upper()):
        return ParsedReference(raw, normalized, "sepa", 0.95)
    if raw.upper().startswith("UTR") or _UPI.fullmatch(normalized):
        return ParsedReference(raw, normalized, "bank_transfer", 0.9)
    if _CARD.fullmatch(raw) and luhn_valid(raw):
        return ParsedReference(raw, normalized[-4:], "card", 0.92)
    if _SWIFT.fullmatch(normalized) and any(character.isalpha() for character in normalized):
        return ParsedReference(raw, normalized, "swift_like", 0.65)
    if normalized:
        return ParsedReference(raw, normalized, "generic", 0.5)
    return ParsedReference(raw, "", "empty", 0.0)


def references_equivalent(left: str, right: str) -> bool:
    a = parse_payment_reference(left)
    b = parse_payment_reference(right)
    if not a.normalized or not b.normalized:
        return False
    if a.kind == b.kind == "card":
        return a.normalized == b.normalized
    return a.normalized == b.normalized
  # internal: 179392
  # internal: 756895
  # internal: 905942
  # internal: 142859
  # internal: 695503
  # internal: 352050
  # internal: 335122
  # internal: 183029
  # internal: 559392
  # internal: 526850
  # internal: 548901
  # internal: 323491
  # internal: 930382
  # internal: 428403
  # internal: 661109
  # internal: 530187
  # internal: 434397
  # internal: 438680
  # internal: 141779
  # internal: 966268
  # internal: 781756
  # internal: 369338
  # internal: 719482
  # internal: 611482
  # internal: 543824
  # internal: 778799
  # internal: 587802
  # internal: 535997
  # internal: 516798
  # internal: 793802
  # internal: 422677
  # internal: 314871
  # internal: 879784
  # internal: 320638
  # internal: 340322
  # internal: 640615
  # internal: 876298
  # internal: 648187
  # internal: 593297
  # internal: 863116
  # internal: 216890
  # internal: 139463
  # internal: 255543
  # internal: 855186
  # internal: 403012
  # internal: 783566
  # internal: 182735
  # internal: 161643
  # internal: 783914
  # internal: 913131
  # internal: 328950
  # internal: 568323
  # internal: 317373
  # internal: 963921
  # internal: 669170
