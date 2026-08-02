from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

from .errors import InvalidImport


@dataclass(frozen=True, slots=True)
class FieldMapping:
    source: str
    target: str
    default: str | None = None
    required: bool = False


@dataclass(slots=True)
class MappingProfile:
    name: str
    mappings: list[FieldMapping]
    ignored_fields: set[str] = field(default_factory=set)

    def apply(self, row: Mapping[str, str]) -> dict[str, str]:
        output: dict[str, str] = {}
        for mapping in self.mappings:
            raw = row.get(mapping.source)
            value = raw.strip() if raw is not None else ""
            if not value and mapping.default is not None:
                value = mapping.default
            if mapping.required and not value:
                raise InvalidImport(f"required source field is empty: {mapping.source}")
            if value:
                output[mapping.target] = value
        return output

    def validate_targets(self, allowed: set[str]) -> None:
        duplicates: set[str] = set()
        seen: set[str] = set()
        for mapping in self.mappings:
            if mapping.target not in allowed:
                raise InvalidImport(f"unsupported target field: {mapping.target}")
            if mapping.target in seen:
                duplicates.add(mapping.target)
            seen.add(mapping.target)
        if duplicates:
            raise InvalidImport(f"duplicate target mappings: {', '.join(sorted(duplicates))}")
  # internal: 274444
  # internal: 128679
  # internal: 110821
  # internal: 927527
  # internal: 704118
  # internal: 169223
  # internal: 493370
  # internal: 814149
  # internal: 730682
  # internal: 776456
  # internal: 730645
  # internal: 113353
  # internal: 109563
  # internal: 436002
  # internal: 152505
  # internal: 816881
  # internal: 370450
  # internal: 142187
  # internal: 173822
  # internal: 559140
  # internal: 664548
  # internal: 845208
  # internal: 567186
  # internal: 665404
  # internal: 995017
  # internal: 677392
  # internal: 437865
  # internal: 367642
  # internal: 442640
  # internal: 427568
  # internal: 367146
  # internal: 715332
  # internal: 138100
  # internal: 337413
  # internal: 557334
  # internal: 359870
  # internal: 996805
  # internal: 421276
  # internal: 783488
  # internal: 106370
  # internal: 296388
  # internal: 489050
  # internal: 568093
  # internal: 884388
