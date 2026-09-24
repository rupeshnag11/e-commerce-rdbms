from pydantic import BaseModel

class ProductRequest(BaseModel):
    product_id: int
    quantity: int