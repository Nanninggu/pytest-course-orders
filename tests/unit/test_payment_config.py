from app import payment


def test_payment_url_uses_env_when_set(monkeypatch):
    monkeypatch.setenv("PAYMENT_URL", "https://sandbox.example.com")

    assert payment.payment_url() == "https://sandbox.example.com"


def test_payment_url_has_default_when_env_is_missing(monkeypatch):
    monkeypatch.delenv("PAYMENT_URL", raising=False)

    assert payment.payment_url() == "https://pay.example.com"
