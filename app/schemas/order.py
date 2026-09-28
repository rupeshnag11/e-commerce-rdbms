from pydantic import BaseModel

class OrderRequest(BaseModel):
    cart_item_ids : list[int]