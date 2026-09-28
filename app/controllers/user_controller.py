from fastapi import Depends, APIRouter
from app.models.models import User_role
from app.services.auth_service import get_current_user
from app.services.user_service import get_user_details_service,get_user_past_orders_service

router = APIRouter()


@router.get("/users_details")
def users_details(current_user: User_role = Depends(get_current_user)):
    return get_user_details_service(current_user)


@router.get("/get_user_past_n_orders")
def get_user_past_orders(current_user: User_role = Depends(get_current_user)):
    return get_user_past_orders_service(current_user)