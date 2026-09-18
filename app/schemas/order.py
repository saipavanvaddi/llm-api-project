from pydantic import BaseModel


class OrderItem(BaseModel):
    name: str
    quantity: int
    price: float


class OrderInfo(BaseModel):
    items: list[OrderItem]
    total: float


    