import importlib


class FakeResponse:
    def __init__(self, status_code=200, payload=None, text=""):
        self.status_code = status_code
        self._payload = payload or {"ok": True}
        self.text = text

    def json(self):
        return self._payload


def notifier_module():
    return importlib.import_module("telegram_notifier")


def configure_credentials(monkeypatch, module, token="token", chat_id="123"):
    monkeypatch.setattr(module, "TELEGRAM_BOT_TOKEN", token)
    monkeypatch.setattr(module, "CHAT_ID", chat_id)


def test_send_message_skips_network_without_credentials(monkeypatch):
    module = notifier_module()
    calls = []
    monkeypatch.setattr(module.requests, "post", lambda *args, **kwargs: calls.append((args, kwargs)))

    notifier = module.TelegramNotifier()

    assert notifier.send_message("test") is False
    assert calls == []


def test_send_message_posts_payload_when_configured(monkeypatch):
    module = notifier_module()
    configure_credentials(monkeypatch, module)
    calls = []

    def fake_post(url, json, timeout):
        calls.append({"url": url, "json": json, "timeout": timeout})
        return FakeResponse(status_code=200)

    monkeypatch.setattr(module.requests, "post", fake_post)
    notifier = module.TelegramNotifier()

    assert notifier.send_message("hello") is True
    assert calls == [
        {
            "url": "https://api.telegram.org/bottoken/sendMessage",
            "json": {"chat_id": "123", "text": "hello", "parse_mode": "HTML"},
            "timeout": 10,
        }
    ]


def test_send_message_returns_false_on_api_error(monkeypatch):
    module = notifier_module()
    configure_credentials(monkeypatch, module)
    monkeypatch.setattr(
        module.requests,
        "post",
        lambda *args, **kwargs: FakeResponse(status_code=500),
    )
    notifier = module.TelegramNotifier()

    assert notifier.send_message("hello") is False


def test_send_photo_missing_file_skips_network(monkeypatch, tmp_path):
    module = notifier_module()
    configure_credentials(monkeypatch, module)
    calls = []
    monkeypatch.setattr(module.requests, "post", lambda *args, **kwargs: calls.append((args, kwargs)))
    notifier = module.TelegramNotifier()

    assert notifier.send_photo(str(tmp_path / "missing.jpg"), "caption") is False
    assert calls == []


def test_notify_unknown_person_uses_cooldown(monkeypatch):
    module = notifier_module()
    monkeypatch.setattr(module, "NOTIFICATION_COOLDOWN", 30)
    current_time = {"value": 1000}
    monkeypatch.setattr(module.time, "time", lambda: current_time["value"])

    notifier = module.TelegramNotifier()
    monkeypatch.setattr(notifier, "send_message", lambda message: True)
    monkeypatch.setattr(notifier, "send_photo", lambda photo_path, caption="": True)

    assert notifier.notify_unknown_person() is True

    current_time["value"] = 1005
    assert notifier.notify_unknown_person() is False
