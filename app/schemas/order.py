from pydantic import BaseModel

class OrderRequest(BaseModel):
    total_amount: float