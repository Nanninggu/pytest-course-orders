from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Order, Product
from app.payment import PaymentTimeout, charge


class ProductNotFound(Exception):
    pass


class OutOfStock(Exception):
    pass


class OrderNotFound(Exception):
    pass


class AlreadyCancelled(Exception):
    pass


class NotPayable(Exception):
    pass


class PaymentWindowClosed(Exception):
    pass


MAX_ATTEMPTS = 3
PAYMENT_WINDOW = timedelta(hours=24)


def create_order(db: Session, product_id: int, quantity: int) -> Order:
    product = db.get(Product, product_id)
    if product is None:
        raise ProductNotFound(product_id)
    if product.stock < quantity:
        raise OutOfStock(product_id)
    product.stock -= quantity
    order = Order(product_id=product.id, quantity=quantity, total_price=product.price * quantity, status="created", created_at=datetime.now())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_order(db: Session, order_id: int) -> Order | None:
    return db.get(Order, order_id)


def list_orders(db: Session) -> list[Order]:
    return list(db.scalars(select(Order).order_by(Order.id)))


def cancel_order(db: Session, order_id: int) -> Order:
    """생성 상태의 주문만 취소한다. 주문 수량만큼 재고를 한 번 되돌린다."""
    order = db.get(Order, order_id)
    if order is None:
        raise OrderNotFound(order_id)
    if order.status != "created":
        raise AlreadyCancelled(order_id)
    product = db.get(Product, order.product_id)
    product.stock += order.quantity
    order.status = "cancelled"
    db.commit()
    db.refresh(order)
    return order


def pay_order(db: Session, order_id: int, now: datetime | None = None) -> dict:
    """생성 상태의 주문을 결제 서비스에 요청한다. 주문한 지 24시간이 지나면 결제할 수 없다. 시간 초과면 최대 세 번까지 다시 요청한다. 주문 상태는 바꾸지 않는다."""
    order = db.get(Order, order_id)
    if order is None:
        raise OrderNotFound(order_id)
    if order.status != "created":
        raise NotPayable(order_id)
    now = now or datetime.now()
    if now - order.created_at > PAYMENT_WINDOW:
        raise PaymentWindowClosed(order_id)
    for attempt in range(MAX_ATTEMPTS):  # pragma: no branch (세 번째에 반드시 값을 돌려주거나 예외)
        try:
            return charge(order.id, order.total_price)
        except PaymentTimeout:
            if attempt == MAX_ATTEMPTS - 1:
                raise
