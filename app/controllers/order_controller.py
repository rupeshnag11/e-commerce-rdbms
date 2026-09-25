from fastapi import FastAPI, Depends
from app.models.models import User_role
from app.schemas.product import ProductRequest
from app.schemas.order import OrderRequest
from app.services.auth_service import get_current_user
from app.services.order_service import purchase_order_service, create_order_service


app = FastAPI()


@app.post("/purchase_order")
def purchase_order(
    request: ProductRequest,
    current_user: User_role = Depends(get_current_user)
):
    return purchase_order_service(
        request,
        current_user
    )


@app.post("/create_order")
def create_order(request: OrderRequest, current_user: User_role = Depends(get_current_user)):
    return create_order_service(request,current_user)
