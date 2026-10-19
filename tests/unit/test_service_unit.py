import pytest

from app import services
from app.models import Product


class FakeSession:
    """DB 없이 서비스를 시험하려고 만든 가짜 세션. 서비스가 부르는 것만 흉내 낸다."""

    def __init__(self, product=None):
        self.product = product
        self.added = []
        self.committed = False

    def get(self, model, key):
        return self.product

    def add(self, obj):
        self.added.append(obj)

    def commit(self):
        self.committed = True

    def refresh(self, obj):
        pass


@pytest.fixture
def keyboard():
    return Product(id=1, name="키보드", price=30000, stock=10)


@pytest.mark.parametrize("quantity, total", [(1, 30000), (2, 60000), (3, 90000)])
def test_total_price_is_price_times_quantity(keyboard, quantity, total):
    db = FakeSession(keyboard)

    order = services.create_order(db, 1, quantity)

    assert order.total_price == total


def test_order_reduces_stock(keyboard):
    db = FakeSession(keyboard)

    services.create_order(db, 1, 2)

    assert keyboard.stock == 8


def test_out_of_stock_raises(keyboard):
    db = FakeSession(keyboard)

    with pytest.raises(services.OutOfStock):
        services.create_order(db, 1, 11)

    assert keyboard.stock == 10
    assert db.added == []


def test_unknown_product_raises():
    db = FakeSession(None)

    with pytest.raises(services.ProductNotFound):
        services.create_order(db, 99, 1)
