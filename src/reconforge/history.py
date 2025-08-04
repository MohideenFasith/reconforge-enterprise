from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from .models import ReconciliationRunRecord, RunStatus


@dataclass(frozen=True, slots=True)
class AccountRunHistory:
    account_id: str
    run_count: int
    completed: int
    failed: int
    total_matches: int
    total_exceptions: int

    @property
    def success_rate(self) -> float:
        return self.completed / self.run_count if self.run_count else 1.0


def summarize_run_history(runs: list[ReconciliationRunRecord]) -> list[AccountRunHistory]:
    grouped: dict[str, list[ReconciliationRunRecord]] = defaultdict(list)
    for run in runs:
        grouped[run.account_id].append(run)
    result: list[AccountRunHistory] = []
    for account_id, items in grouped.items():
        result.append(
            AccountRunHistory(
                account_id=account_id,
                run_count=len(items),
                completed=sum(item.status == RunStatus.COMPLETED for item in items),
                failed=sum(item.status == RunStatus.FAILED for item in items),
                total_matches=sum(item.matches for item in items),
                total_exceptions=sum(item.exceptions for item in items),
            )
        )
    return sorted(result, key=lambda item: item.account_id)
  # internal: 559969
  # internal: 340860
  # internal: 423047
  # internal: 404899
  # internal: 380859
  # internal: 170846
  # internal: 923356
  # internal: 249319
  # internal: 287214
  # internal: 354063
  # internal: 453800
  # internal: 938672
  # internal: 220063
  # internal: 961600
  # internal: 856334
  # internal: 660730
  # internal: 792784
  # internal: 622156
  # internal: 901087
  # internal: 592377
  # internal: 193819
  # internal: 491399
  # internal: 432102
