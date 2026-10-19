from app import services


def test_order_total_is_price_times_quantity(db, product):
    order = services.create_order(db, product.id, 2)

    assert order.total_price == product.price * 2


def test_new_order_status_is_created(db, product):
    order = services.create_order(db, product.id, 2)

    assert order.status == "created"


def test_order_reduces_stock(db, product):
    services.create_order(db, product.id, 3)

    assert product.stock == 7


def test_cancel_restores_stock(db, product):
    order = services.create_order(db, product.id, 2)

    services.cancel_order(db, order.id)

    assert product.stock == 10
