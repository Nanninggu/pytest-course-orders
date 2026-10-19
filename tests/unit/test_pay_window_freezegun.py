from datetime import timedelta

import pytest
from freezegun import freeze_time

from app import services

RECEIPT = {"payment_id": "pay_test", "status": "approved", "amount": 60000}
ORDERED_AT = "2026-10-18 12:00:00"


@pytest.mark.parametrize("elapsed", [timedelta(hours=23, minutes=59, seconds=59), timedelta(hours=24)],
                         ids=["just_before", "exactly_24h"])
def test_pay_order_inside_the_payment_window(db, product, mocker, elapsed):
    mocker.patch("app.services.charge", return_value=RECEIPT)
    with freeze_time(ORDERED_AT) as frozen:
        order = services.create_order(db, product.id, 2)
        frozen.tick(elapsed)

        receipt = services.pay_order(db, order.id)

    assert receipt == RECEIPT


def test_pay_order_after_the_payment_window(db, product, mocker):
    mocker.patch("app.services.charge", return_value=RECEIPT)
    with freeze_time(ORDERED_AT) as frozen:
        order = services.create_order(db, product.id, 2)
        frozen.tick(timedelta(hours=24, seconds=1))

        with pytest.raises(services.PaymentWindowClosed):
            services.pay_order(db, order.id)
