import pytest

from app import services


def test_cancel_restores_stock_by_quantity(db, product):
    order = services.create_order(db, product.id, 3)
    assert product.stock == 7

    cancelled = services.cancel_order(db, order.id)

    assert cancelled.status == "cancelled"
    assert product.stock == 10


def test_second_cancel_raises_and_keeps_stock(db, product):
    order = services.create_order(db, product.id, 3)
    services.cancel_order(db, order.id)
    stock_after_first = product.stock

    with pytest.raises(services.AlreadyCancelled):
        services.cancel_order(db, order.id)

    assert product.stock == stock_after_first


def test_cancel_unknown_order_raises(db):
    with pytest.raises(services.OrderNotFound):
        services.cancel_order(db, 99)
