from datetime import datetime
from types import SimpleNamespace

from app.models import Order, Product


def make_product(db, **fields):
    values = {"name": "키보드", "price": 30000, "stock": 10}
    values.update(fields)
    product = Product(**values)
    db.add(product)
    db.commit()
    return product


def make_order(db, product=None, quantity=1, **fields):
    product = product or make_product(db)
    values = {
        "product_id": product.id,
        "quantity": quantity,
        "total_price": product.price * quantity,
        "status": "created",
        "created_at": datetime(2026, 1, 1, 12, 0),
    }
    values.update(fields)
    order = Order(**values)
    db.add(order)
    db.commit()
    return order


def seed_catalog(db):
    keyboard = make_product(db)
    mouse = make_product(db, name="마우스", price=15000, stock=20)
    sold_out = make_product(db, name="헤드셋", price=50000, stock=0)
    orders = [make_order(db, keyboard), make_order(db, mouse, quantity=3)]
    return SimpleNamespace(keyboard=keyboard, mouse=mouse, sold_out=sold_out, orders=orders)
