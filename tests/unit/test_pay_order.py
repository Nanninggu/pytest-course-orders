from app import services


def fake_charge(order_id, amount):
    return {"payment_id": "pay_test", "status": "approved", "amount": amount}


def test_pay_order_returns_approved_receipt(db, product, monkeypatch):
    monkeypatch.setattr(services, "charge", fake_charge)
    order = services.create_order(db, product.id, 2)

    receipt = services.pay_order(db, order.id)

    assert receipt == {"payment_id": "pay_test", "status": "approved", "amount": 60000}


def test_charge_is_restored_after_each_test():
    assert services.charge is not fake_charge
