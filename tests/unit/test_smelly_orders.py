from app import services
from app.models import Product

used_ids = []


def test_1(db):
    db.add(Product(id=1, name="키보드", price=30000, stock=10))
    db.commit()
    order = services.create_order(db, 1, 2)
    used_ids.append(order.id)
    assert order.total_price == 60000
    assert order.status == "created"
    cancelled = services.cancel_order(db, order.id)
    assert cancelled.status == "cancelled"
    assert db.get(Product, 1).stock == 10


def test_order(db):
    db.add(Product(id=1, name="키보드", price=30000, stock=10))
    db.commit()
    services.create_order(db, 1, 3)


def test_stock(db):
    db.add(Product(id=1, name="키보드", price=30000, stock=10))
    db.commit()
    services.create_order(db, 1, 3)
    assert db.get(Product, 1).stock == 7


def test_second():
    assert len(used_ids) == 1
