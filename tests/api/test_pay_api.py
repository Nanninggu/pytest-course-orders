import pytest

from app.payment import PaymentDeclined, PaymentError, PaymentTimeout

RECEIPT = {"payment_id": "pay_test", "status": "approved", "amount": 60000}


def make_order(client, auth_headers):
    return client.post("/orders", json={"product_id": 1, "quantity": 2}, headers=auth_headers).json()


def test_pay_returns_200_and_the_receipt(client, auth_headers, product, mocker):
    mocker.patch("app.services.charge", return_value=RECEIPT)
    order = make_order(client, auth_headers)

    response = client.post(f"/orders/{order['id']}/pay", headers=auth_headers)

    assert response.status_code == 200
    assert response.json() == RECEIPT


@pytest.mark.parametrize("error, status", [(PaymentDeclined(), 402), (PaymentTimeout(), 504), (PaymentError(), 502)],
                         ids=["declined", "timeout", "service_error"])
def test_pay_maps_payment_errors(client, auth_headers, product, mocker, error, status):
    mocker.patch("app.services.charge", side_effect=error)
    order = make_order(client, auth_headers)

    response = client.post(f"/orders/{order['id']}/pay", headers=auth_headers)

    assert response.status_code == status


def test_pay_unknown_order_returns_404(client, auth_headers, mocker):
    mock_charge = mocker.patch("app.services.charge")

    response = client.post("/orders/99/pay", headers=auth_headers)

    assert response.status_code == 404
    mock_charge.assert_not_called()


def test_pay_cancelled_order_returns_409_and_does_not_charge(client, auth_headers, product, mocker):
    mock_charge = mocker.patch("app.services.charge", return_value=RECEIPT)
    order = make_order(client, auth_headers)
    client.post(f"/orders/{order['id']}/cancel", headers=auth_headers)

    response = client.post(f"/orders/{order['id']}/pay", headers=auth_headers)

    assert response.status_code == 409
    mock_charge.assert_not_called()
