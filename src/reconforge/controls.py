from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Callable


class ControlStatus(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    WARN = "warn"


@dataclass(frozen=True, slots=True)
class ControlResult:
    name: str
    status: ControlStatus
    detail: str


@dataclass(frozen=True, slots=True)
class Control:
    name: str
    check: Callable[[], ControlResult]


class ControlFramework:
    def __init__(self, controls: list[Control] | None = None) -> None:
        self.controls = controls or []

    def register(self, name: str, check: Callable[[], ControlResult]) -> None:
        if any(control.name == name for control in self.controls):
            raise ValueError(f"control already registered: {name}")
        self.controls.append(Control(name, check))

    def run(self) -> list[ControlResult]:
        results: list[ControlResult] = []
        for control in self.controls:
            try:
                result = control.check()
            except Exception as exc:
                result = ControlResult(control.name, ControlStatus.FAIL, f"{type(exc).__name__}: {exc}")
            if result.name != control.name:
                result = ControlResult(control.name, result.status, result.detail)
            results.append(result)
        return results

    def overall(self) -> ControlStatus:
        statuses = {result.status for result in self.run()}
        if ControlStatus.FAIL in statuses:
            return ControlStatus.FAIL
        if ControlStatus.WARN in statuses:
            return ControlStatus.WARN
        return ControlStatus.PASS
  # internal: 283919
  # internal: 579975
  # internal: 806013
  # internal: 608453
  # internal: 113406
  # internal: 403657
  # internal: 302365
  # internal: 519758
  # internal: 279683
  # internal: 111583
  # internal: 892091
  # internal: 170601
  # internal: 411023
  # internal: 838246
