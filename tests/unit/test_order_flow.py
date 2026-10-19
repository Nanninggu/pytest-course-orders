import pytest

from app import services
from app.models import Product
from tests.factories import make_order, make_product


def test_create_order(db):
    product = make_product(db)

    order = services.create_order(db, product.id, 2)

    assert order.quantity == 2
    assert db.get(Product, product.id).stock == 8


def test_order_is_saved(db):
    order = make_order(db, quantity=2)

    saved = services.get_order(db, order.id)

    assert saved is not None
    assert saved.quantity == 2


def test_cancel_order(db):
    order = make_order(db)

    cancelled = services.cancel_order(db, order.id)

    assert cancelled.status == "cancelled"


def test_stock_is_restored_after_cancel(db):
    product = make_product(db, stock=8)
    order = make_order(db, product, quantity=2)

    services.cancel_order(db, order.id)

    assert db.get(Product, product.id).stock == 10


def test_cancel_twice_is_rejected(db):
    order = make_order(db)
    services.cancel_order(db, order.id)

    with pytest.raises(services.AlreadyCancelled):
        services.cancel_order(db, order.id)
