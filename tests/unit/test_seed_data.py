import pytest

from app import services
from tests.factories import make_order, make_product


def test_orders_are_listed_in_id_order(db):
    keyboard = make_product(db)
    mouse = make_product(db, name="마우스", price=15000)
    make_order(db, keyboard)
    make_order(db, mouse, quantity=3)

    orders = services.list_orders(db)

    assert [o.product_id for o in orders] == [keyboard.id, mouse.id]
    assert [o.quantity for o in orders] == [1, 3]


def test_sold_out_product_cannot_be_ordered(db):
    sold_out = make_product(db, stock=0)

    with pytest.raises(services.OutOfStock):
        services.create_order(db, sold_out.id, 1)

    assert services.list_orders(db) == []
