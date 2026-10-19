import pytest

from app import services
from app.models import Product
from tests.factories import make_product


def test_create_order_calculates_total_and_reduces_stock(db):
    db.add(Product(id=1, name="키보드", price=30000, stock=10))
    db.commit()

    order = services.create_order(db, 1, 2)

    assert order.total_price == 60000
    assert db.get(Product, 1).stock == 8


def test_out_of_stock_creates_no_order(db):
    product = make_product(db, stock=1)

    with pytest.raises(services.OutOfStock):
        services.create_order(db, product.id, 2)

    assert services.list_orders(db) == []
