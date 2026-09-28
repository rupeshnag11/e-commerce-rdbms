from fastapi import APIRouter, Depends
from app.models.models import User_role
from app.schemas.cart import CartRequest
from app.services.auth_service import get_current_user
from app.services.cart_service import create_cart_service,get_cart_service


router = APIRouter()


@router.post("/create_cart")
def create_cart(
    request: CartRequest,
    current_user: User_role = Depends(get_current_user)
):
    return create_cart_service(
        request,
        current_user
    )

@router.get("/cart")
def get_cart(
    current_user: User_role = Depends(get_current_user)
):
    return get_cart_service(current_user)