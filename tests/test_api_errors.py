
def test_not_found_conflict_and_validation_handlers(client, auth_headers) -> None:
    missing = client.get("/v1/accounts/nope", headers=auth_headers)
    assert missing.status_code == 404
    payload = {"name": "Ops", "external_id": "X", "currency": "USD"}
    assert client.post("/v1/accounts", headers=auth_headers, json=payload).status_code == 201
    duplicate = client.post("/v1/accounts", headers=auth_headers, json=payload)
    assert duplicate.status_code == 409
    invalid = client.post("/v1/accounts", headers=auth_headers, json={"name":"x","external_id":"","currency":"USD"})
    assert invalid.status_code == 422
  # internal: 688098
  # internal: 693071
  # internal: 256532
