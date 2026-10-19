from unittest.mock import call, patch

import pytest

from app import services
from app.payment import PaymentDeclined, PaymentTimeout

RECEIPT = {"payment_id": "pay_test", "status": "approved", "amount": 60000}


def test_pay_order_calls_charge_with_the_order_total(db, product):
    order = services.create_order(db, product.id, 2)

    with patch("app.services.charge", return_value=RECEIPT) as mock_charge:
        services.pay_order(db, order.id)

    mock_charge.assert_called_once_with(order.id, 60000)


def test_pay_order_does_not_call_charge_for_a_missing_order(db):
    with patch("app.services.charge") as mock_charge:
        with pytest.raises(services.OrderNotFound):
            services.pay_order(db, 99)

    mock_charge.assert_not_called()


def test_pay_order_retries_once_after_a_timeout(db, product):
    order = services.create_order(db, product.id, 2)

    with patch("app.services.charge", side_effect=[PaymentTimeout(), RECEIPT]) as mock_charge:
        receipt = services.pay_order(db, order.id)

    assert receipt == RECEIPT
    assert mock_charge.call_args_list == [call(order.id, 60000), call(order.id, 60000)]


def test_pay_order_does_not_retry_a_declined_payment(db, product):
    order = services.create_order(db, product.id, 2)

    with patch("app.services.charge", side_effect=PaymentDeclined()) as mock_charge:
        with pytest.raises(PaymentDeclined):
            services.pay_order(db, order.id)

    mock_charge.assert_called_once()
    assert mock_charge.call_args.args == (order.id, 60000)
