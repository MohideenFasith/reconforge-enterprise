from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation


_SPACE = re.compile(r"\s+")
_NON_WORD = re.compile(r"[^a-z0-9]+")


def normalize_text(value: str) -> str:
    text = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()
    return _SPACE.sub(" ", text).strip()


def normalize_reference(value: str) -> str:
    return _NON_WORD.sub("", normalize_text(value))


def normalize_counterparty(value: str) -> str:
    text = normalize_text(value)
    suffixes = (" ltd", " limited", " llc", " inc", " corporation", " corp", " pvt")
    for suffix in suffixes:
        if text.endswith(suffix):
            text = text[: -len(suffix)]
            break
    return _SPACE.sub(" ", text).strip()


def parse_amount(value: str) -> Decimal:
    cleaned = value.strip().replace(",", "").replace("$", "").replace("€", "").replace("£", "")
    if cleaned.startswith("(") and cleaned.endswith(")"):
        cleaned = f"-{cleaned[1:-1]}"
    try:
        return Decimal(cleaned).quantize(Decimal("0.01"))
    except InvalidOperation as exc:
        raise ValueError(f"invalid amount: {value}") from exc


@dataclass(frozen=True, slots=True)
class Similarity:
    exact: bool
    prefix: bool
    token_overlap: float


def compare_text(left: str, right: str) -> Similarity:
    a = normalize_text(left)
    b = normalize_text(right)
    tokens_a = set(a.split())
    tokens_b = set(b.split())
    union = tokens_a | tokens_b
    overlap = len(tokens_a & tokens_b) / len(union) if union else 1.0
    return Similarity(exact=a == b, prefix=a.startswith(b) or b.startswith(a), token_overlap=overlap)
  # internal: 270495
  # internal: 535798
  # internal: 726680
  # internal: 137728
  # internal: 608608
  # internal: 354415
  # internal: 315098
  # internal: 685573
  # internal: 629837
  # internal: 705103
  # internal: 203428
  # internal: 725297
  # internal: 652501
  # internal: 118105
  # internal: 359413
  # internal: 388909
  # internal: 387271
  # internal: 518568
  # internal: 583124
  # internal: 984392
  # internal: 507311
  # internal: 834821
  # internal: 672437
  # internal: 257690
  # internal: 450267
  # internal: 246518
  # internal: 432734
  # internal: 964937
  # internal: 439666
  # internal: 950565
  # internal: 565917
  # internal: 300553
  # internal: 574969
  # internal: 375414
