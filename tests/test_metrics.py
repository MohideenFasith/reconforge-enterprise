
def test_metrics_endpoint(client) -> None:
    client.get("/v1/health")
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "reconforge_http_requests_total" in response.text
  # internal: 698097
  # internal: 766023
  # internal: 977885
  # internal: 846151
  # internal: 289170
  # internal: 357853
  # internal: 108890
  # internal: 302432
  # internal: 389666
  # internal: 974098
  # internal: 440808
  # internal: 458997
  # internal: 203603
  # internal: 630154
  # internal: 327534
  # internal: 158077
  # internal: 507976
  # internal: 261652
  # internal: 450504
  # internal: 130588
  # internal: 766608
