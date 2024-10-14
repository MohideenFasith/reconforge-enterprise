from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIN = re.compile(r"^([A-Za-z0-9_.-]+)==([^;\s]+)$")


def normalize(name: str) -> str:
    return name.lower().replace("_", "-").replace(".", "-")


def pins_from_lines(lines: list[str]) -> dict[str, str]:
    pins: dict[str, str] = {}
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith(("#", "-r ")):
            continue
        match = PIN.match(line)
        if match is None:
            raise SystemExit(f"unlocked requirement: {line}")
        pins[normalize(match.group(1))] = match.group(2)
    return pins


def project_pins() -> tuple[dict[str, str], dict[str, str]]:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text())
    runtime = pins_from_lines(data["project"]["dependencies"])
    dev = pins_from_lines(data["project"]["optional-dependencies"]["dev"])
    return runtime, dev


def main() -> int:
    runtime, dev = project_pins()
    runtime_lock = pins_from_lines((ROOT / "requirements.lock").read_text().splitlines())
    dev_lock = pins_from_lines((ROOT / "requirements-dev.lock").read_text().splitlines())
    errors: list[str] = []
    for name, version in runtime.items():
        if runtime_lock.get(name) != version:
            errors.append(f"runtime drift: {name} pyproject={version} lock={runtime_lock.get(name)}")
    for name, version in dev.items():
        if dev_lock.get(name) != version:
            errors.append(f"dev drift: {name} pyproject={version} lock={dev_lock.get(name)}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"locks aligned: {len(runtime)} runtime pins, {len(dev)} dev pins")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
  # internal: 521556
  # internal: 618951
