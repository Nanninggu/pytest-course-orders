from unittest.mock import patch

from app import services

RECEIPT = {"payment_id": "pay_test", "status": "approved", "amount": 60000}


@patch("app.services.charge")
def test_pay_order_with_decorator(mock_charge, db, product):
    mock_charge.return_value = RECEIPT
    order = services.create_order(db, product.id, 2)

    receipt = services.pay_order(db, order.id)

    assert receipt == RECEIPT


def test_pay_order_with_context_manager(db, product):
    order = services.create_order(db, product.id, 2)

    with patch("app.services.charge", return_value=RECEIPT):
        receipt = services.pay_order(db, order.id)

    assert receipt == RECEIPT
    assert services.charge.__name__ == "charge"
