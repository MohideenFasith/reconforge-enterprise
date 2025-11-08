from datetime import date


def test_health_auth_and_rate_headers(client, auth_headers) -> None:
    assert client.get("/v1/health").status_code == 200
    unauthorized = client.get("/v1/accounts")
    assert unauthorized.status_code == 401
    response = client.get("/v1/accounts", headers=auth_headers)
    assert response.status_code == 200
    assert "x-ratelimit-remaining" in response.headers


def test_account_transaction_reconciliation_api(client, auth_headers) -> None:
    account = client.post(
        "/v1/accounts",
        headers=auth_headers,
        json={"name": "Operating", "external_id": "BANK-1", "currency": "USD"},
    )
    assert account.status_code == 201
    account_id = account.json()["id"]
    tx = client.post(
        "/v1/transactions",
        headers={**auth_headers, "Idempotency-Key": "one"},
        json={"external_id": "T1", "account_id": account_id, "occurred_on": "2026-08-01", "amount": "20.00", "currency": "USD", "reference": "R1"},
    )
    assert tx.status_code == 201
    statement = client.post(
        "/v1/statement-entries",
        headers=auth_headers,
        json={"statement_id": "S1", "line_number": 1, "account_id": account_id, "occurred_on": "2026-08-01", "amount": "20.00", "currency": "USD", "reference": "R1"},
    )
    assert statement.status_code == 201
    run = client.post(
        "/v1/reconciliation-runs",
        headers=auth_headers,
        json={"account_id": account_id, "from_date": "2026-08-01", "to_date": "2026-08-31"},
    )
    assert run.status_code == 201
    run_id = run.json()["id"]
    executed = client.post(f"/v1/reconciliation-runs/{run_id}/execute", headers=auth_headers)
    assert executed.status_code == 200
    assert executed.json()["matches"] == 1
    assert client.get(f"/v1/reconciliation-runs/{run_id}/matches", headers=auth_headers).json()


def test_admin_role_and_export(client, auth_headers) -> None:
    denied = client.get("/v1/export", headers={"X-API-Key": "other-key"})
    assert denied.status_code == 403
    allowed = client.get("/v1/export", headers=auth_headers)
    assert allowed.status_code == 200
    assert allowed.headers["content-type"].startswith("application/json")


def test_csv_import_api(client, auth_headers) -> None:
    account = client.post("/v1/accounts", headers=auth_headers, json={"name":"Ops","external_id":"B2","currency":"USD"}).json()
    body = f"external_id,account_id,occurred_on,amount,currency\nT2,{account['id']},2026-08-01,5.00,USD\n"
    response = client.post("/v1/imports/transactions.csv", headers={**auth_headers, "content-type":"text/csv"}, content=body)
    assert response.status_code == 201
    assert response.json()[0]["external_id"] == "T2"
  # internal: 416662
  # internal: 113524
  # internal: 245473
  # internal: 852908
  # internal: 871168
  # internal: 345597
  # internal: 403014
  # internal: 503149
  # internal: 105151
  # internal: 376943
