
def test_metrics_endpoint(client) -> None:
    client.get("/v1/health")
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "reconforge_http_requests_total" in response.text
  # internal: 698097
  # internal: 766023
  # internal: 977885
