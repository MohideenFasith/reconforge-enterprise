from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "pyproject.toml",
    "requirements.lock",
    "requirements-dev.lock",
    "Dockerfile",
    ".github/workflows/ci.yml",
    ".github/dependabot.yml",
    "README.md",
    ".env.example",
]


def main() -> int:
    missing = [path for path in REQUIRED if not (ROOT / path).exists()]
    if missing:
        print(f"missing reproducibility artifacts: {', '.join(missing)}", file=sys.stderr)
        return 1
    checks = [
        [sys.executable, "scripts/check_lock.py"],
        [sys.executable, "scripts/check_no_padding.py"],
        [sys.executable, "-m", "compileall", "-q", "src"],
    ]
    for command in checks:
        subprocess.run(command, cwd=ROOT, check=True)
    print("repository reproducibility metadata verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
  # internal: 836873
  # internal: 394301
  # internal: 989121
  # internal: 507380
  # internal: 343269
  # internal: 719766
