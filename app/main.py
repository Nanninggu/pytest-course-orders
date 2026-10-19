from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import services
from app.auth import require_token
from app.database import get_db
from app.payment import PaymentDeclined, PaymentError, PaymentTimeout
from app.schemas import OrderCreate, OrderOut, PaymentOut

app = FastAPI(title="주문 관리 API", dependencies=[Depends(require_token)])


@app.exception_handler(Exception)
async def unhandled_error(request, exc):
    return JSONResponse(status_code=500, content={"detail": "서버 오류가 발생했습니다."})


@app.post("/orders", response_model=OrderOut, status_code=201)
def create_order(body: OrderCreate, db: Session = Depends(get_db)):
    try:
        return services.create_order(db, body.product_id, body.quantity)
    except services.ProductNotFound:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")
    except services.OutOfStock:
        raise HTTPException(status_code=409, detail="재고가 부족합니다.")


@app.get("/orders", response_model=list[OrderOut])
def list_orders(db: Session = Depends(get_db)):
    return services.list_orders(db)


@app.get("/orders/{order_id}", response_model=OrderOut)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = services.get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="주문을 찾을 수 없습니다.")
    return order


@app.post("/orders/{order_id}/cancel", response_model=OrderOut)
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    try:
        return services.cancel_order(db, order_id)
    except services.OrderNotFound:
        raise HTTPException(status_code=404, detail="주문을 찾을 수 없습니다.")
    except services.AlreadyCancelled:
        raise HTTPException(status_code=409, detail="이미 취소된 주문입니다.")


@app.post("/orders/{order_id}/pay", response_model=PaymentOut)
def pay_order(order_id: int, db: Session = Depends(get_db)):
    try:
        return services.pay_order(db, order_id)
    except services.OrderNotFound:
        raise HTTPException(status_code=404, detail="주문을 찾을 수 없습니다.")
    except services.NotPayable:
        raise HTTPException(status_code=409, detail="결제할 수 없는 주문입니다.")
    except services.PaymentWindowClosed:
        raise HTTPException(status_code=409, detail="결제 기한이 지났습니다.")
    except PaymentDeclined:
        raise HTTPException(status_code=402, detail="결제가 거절되었습니다.")
    except PaymentTimeout:
        raise HTTPException(status_code=504, detail="결제 서비스가 응답하지 않습니다.")
    except PaymentError:
        raise HTTPException(status_code=502, detail="결제 서비스에 문제가 있습니다.")
