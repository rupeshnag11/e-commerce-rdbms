from pydantic import BaseModel

class CartItemRequest(BaseModel):
    product_id: int
    quantity: int

class CartRequest(BaseModel):
    items: list[CartItemRequest]