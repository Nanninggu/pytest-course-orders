from pydantic import BaseModel, ConfigDict, Field


class OrderCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    total_price: int
    status: str


class PaymentOut(BaseModel):
    payment_id: str
    status: str
    amount: int
