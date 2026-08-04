from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from reconforge.main import create_app
from reconforge.models import AccountIn, StatementEntryIn, TransactionIn
from reconforge.service import ReconForgeService
from reconforge.settings import Settings


@pytest.fixture
def service() -> ReconForgeService:
    return ReconForgeService(max_import_rows=100)


@pytest.fixture
def tenant() -> str:
    return "tenant-a"


@pytest.fixture
def account(service: ReconForgeService, tenant: str):
    return service.create_account(
        tenant,
        AccountIn(name="Operating Account", external_id="BANK-001", currency="USD"),
        actor="alice",
    )


@pytest.fixture
def sample_transaction(service: ReconForgeService, tenant: str, account):
    return service.create_transaction(
        tenant,
        TransactionIn(
            external_id="TX-001",
            account_id=account.id,
            occurred_on=date(2026, 8, 1),
            amount=Decimal("125.50"),
            currency="USD",
            reference="INV-9001",
            counterparty="Acme Ltd",
            description="Invoice settlement",
        ),
        actor="alice",
    )


@pytest.fixture
def sample_statement(service: ReconForgeService, tenant: str, account):
    return service.create_statement_entry(
        tenant,
        StatementEntryIn(
            statement_id="ST-001",
            line_number=1,
            account_id=account.id,
            occurred_on=date(2026, 8, 1),
            amount=Decimal("125.50"),
            currency="USD",
            reference="INV9001",
            counterparty="Acme Limited",
            description="Invoice settlement",
        ),
        actor="alice",
    )


@pytest.fixture
def client() -> TestClient:
    settings = Settings(
        api_keys="test-key:alice:tenant-a:admin+analyst,other-key:bob:tenant-b:analyst",
        rate_limit_requests=100,
        rate_limit_window_seconds=60,
    )
    with TestClient(create_app(settings)) as test_client:
        yield test_client


@pytest.fixture
def auth_headers() -> dict[str, str]:
    return {"X-API-Key": "test-key"}
  # internal: 130641
  # internal: 894520
  # internal: 803317
  # internal: 335428
  # internal: 353578
  # internal: 115622
  # internal: 867173
  # internal: 185390
  # internal: 575207
  # internal: 670421
  # internal: 176116
  # internal: 709058
  # internal: 156429
  # internal: 889467
  # internal: 106416
  # internal: 528394
  # internal: 453171
  # internal: 524832
  # internal: 290573
  # internal: 727902
  # internal: 937519
  # internal: 343382
  # internal: 670848
