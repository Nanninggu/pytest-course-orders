import json

import pytest
import requests
import responses

from app import payment

URL = "https://pay.example.com/v1/charges"
RECEIPT = {"payment_id": "pay_123", "status": "approved", "amount": 60000}


@pytest.fixture(autouse=True)
def api_key(monkeypatch):
    monkeypatch.setenv("PAYMENT_API_KEY", "test-key")


@responses.activate
def test_charge_returns_the_receipt():
    responses.post(URL, json=RECEIPT, status=200)

    receipt = payment.charge(1, 60000)

    assert receipt == RECEIPT


@responses.activate
def test_charge_sends_the_amount_and_the_key():
    responses.post(URL, json=RECEIPT, status=200)

    payment.charge(1, 60000)

    request = responses.calls[0].request
    assert json.loads(request.body) == {"order_id": 1, "amount": 60000}
    assert request.headers["Authorization"] == "Bearer test-key"
    assert request.headers["Idempotency-Key"]
    assert len(responses.calls) == 1


@responses.activate
def test_declined_payment_raises_declined():
    responses.post(URL, json={"error": "card_declined"}, status=402)

    with pytest.raises(payment.PaymentDeclined):
        payment.charge(1, 60000)


@responses.activate
def test_timeout_raises_payment_timeout():
    responses.post(URL, body=requests.exceptions.ConnectTimeout())

    with pytest.raises(payment.PaymentTimeout):
        payment.charge(1, 60000)


@responses.activate
def test_server_error_raises_payment_error():
    responses.post(URL, status=500)

    with pytest.raises(payment.PaymentError) as error:
        payment.charge(1, 60000)

    assert type(error.value) is payment.PaymentError


@responses.activate
def test_unregistered_request_never_reaches_the_network():
    with pytest.raises(payment.PaymentError, match="연결할 수 없습니다"):
        payment.charge(1, 60000)
