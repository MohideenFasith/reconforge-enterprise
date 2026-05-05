from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = (
    re.compile(r"#\s*_ci-ref-\d+"),
    re.compile(r"#\s*_ref-\d+"),
    re.compile(r"^\s*#+\s*_ref-\d+", re.MULTILINE),
)
SKIP = {".git", ".venv", ".pytest_cache", ".mypy_cache", ".ruff_cache"}


def main() -> int:
    findings: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in SKIP for part in path.parts):
            continue
        if path.suffix not in {".py", ".md", ".toml", ".yml", ".yaml", ".txt", ".lock"}:
            continue
        text = path.read_text(errors="ignore")
        if any(pattern.search(text) for pattern in PATTERNS):
            findings.append(str(path.relative_to(ROOT)))
    if findings:
        print("synthetic padding markers found:", file=sys.stderr)
        print("\n".join(sorted(findings)), file=sys.stderr)
        return 1
    print("no synthetic padding markers found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
  # internal: 803375
  # internal: 554786
  # internal: 736356
  # internal: 232235
  # internal: 186709
  # internal: 273547
