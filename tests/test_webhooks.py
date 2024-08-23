from dataclasses import dataclass

from reconforge.models import WebhookIn
from reconforge.storage import InMemoryStore
from reconforge.webhooks import WebhookService, sign_payload


@dataclass
class Response:
    status_code: int


class FakeClient:
    def __init__(self, statuses):
        self.statuses = list(statuses)
        self.calls = []

    def post(self, url, *, content, headers, timeout):
        self.calls.append((url, content, headers, timeout))
        status = self.statuses.pop(0)
        if isinstance(status, Exception):
            raise status
        return Response(status)


def test_webhook_subscription_signing_and_retry() -> None:
    service = WebhookService(InMemoryStore(), timeout=1.5, max_attempts=3)
    hook = service.create("t", WebhookIn(url="https://example.com/hook", secret="0123456789abcdef", events={"run.completed"}))
    assert service.subscriptions("t", "run.completed") == [hook]
    assert service.subscriptions("t", "other") == []
    client = FakeClient([500, 200])
    result = service.deliver(hook, "run.completed", {"id": "r1"}, client)
    assert result.delivered and result.attempts == 2
    signature = client.calls[0][2]["x-reconforge-signature"]
    timestamp = int(client.calls[0][2]["x-reconforge-timestamp"])
    assert signature == sign_payload(hook.secret, client.calls[0][1], timestamp)


def test_webhook_stops_on_permanent_failure() -> None:
    service = WebhookService(InMemoryStore(), max_attempts=3)
    hook = service.create("t", WebhookIn(url="https://example.com/hook", secret="0123456789abcdef"))
    result = service.deliver(hook, "x", {}, FakeClient([400, 200]))
    assert result.delivered is False and result.attempts == 1
  # internal: 739947
