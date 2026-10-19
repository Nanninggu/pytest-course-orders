from datetime import timedelta

import pytest

from app import services

RECEIPT = {"payment_id": "pay_test", "status": "approved", "amount": 60000}


def test_pay_order_at_exactly_24_hours_with_injected_now(db, product, mocker):
    mocker.patch("app.services.charge", return_value=RECEIPT)
    order = services.create_order(db, product.id, 2)

    receipt = services.pay_order(db, order.id, now=order.created_at + timedelta(hours=24))

    assert receipt == RECEIPT


def test_pay_order_after_24_hours_with_injected_now(db, product, mocker):
    mocker.patch("app.services.charge", return_value=RECEIPT)
    order = services.create_order(db, product.id, 2)

    with pytest.raises(services.PaymentWindowClosed):
        services.pay_order(db, order.id, now=order.created_at + timedelta(hours=24, seconds=1))
