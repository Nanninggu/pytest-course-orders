from app import services
from app.payment import PaymentTimeout

RECEIPT = {"payment_id": "pay_test", "status": "approved", "amount": 60000}


def test_pay_order_retries_once_after_a_timeout_with_mocker(db, product, mocker):
    mock_charge = mocker.patch("app.services.charge", side_effect=[PaymentTimeout(), RECEIPT])
    order = services.create_order(db, product.id, 2)

    receipt = services.pay_order(db, order.id)

    assert receipt == RECEIPT
    assert mock_charge.call_count == 2
