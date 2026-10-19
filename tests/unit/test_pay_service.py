from unittest.mock import patch

import pytest

from app import services
from app.payment import PaymentDeclined, PaymentTimeout

RECEIPT = {"payment_id": "pay_test", "status": "approved", "amount": 60000}


def test_pay_order_charges_the_order_total(db, product):
    order = services.create_order(db, product.id, 2)

    with patch("app.services.charge", return_value=RECEIPT) as mock_charge:
        services.pay_order(db, order.id)

    mock_charge.assert_called_once_with(order.id, 60000)


def test_declined_payment_is_not_retried(db, product):
    order = services.create_order(db, product.id, 2)

    with patch("app.services.charge", side_effect=PaymentDeclined()) as mock_charge:
        with pytest.raises(PaymentDeclined):
            services.pay_order(db, order.id)

    mock_charge.assert_called_once()


def test_three_timeouts_raise_payment_timeout(db, product):
    order = services.create_order(db, product.id, 2)

    with patch("app.services.charge", side_effect=PaymentTimeout()) as mock_charge:
        with pytest.raises(PaymentTimeout):
            services.pay_order(db, order.id)

    assert mock_charge.call_count == 3
