from unittest.mock import patch

from app import payment, services

RECEIPT = {"payment_id": "pay_test", "status": "approved", "amount": 60000}


def test_pay_order_with_patch_where_charge_is_used(db, product):
    order = services.create_order(db, product.id, 2)

    with patch("app.services.charge", return_value=RECEIPT):
        receipt = services.pay_order(db, order.id)

    assert receipt == RECEIPT


def test_patching_payment_does_not_change_the_name_in_services():
    with patch("app.payment.charge") as fake:
        assert payment.charge is fake
        assert services.charge is not fake
