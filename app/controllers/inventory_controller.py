from fastapi import APIRouter, Depends
from app.models.models import User_role
from app.schemas.product import ProductRequest
from app.services.auth_service import get_current_user
from app.services.inventory_service import (
    check_inventory_service,
    inventory_update_service
)


router = APIRouter()


@router.post("/check_inventory")
def check_inventory(
    request: ProductRequest,
    current_user: User_role = Depends(get_current_user)
):
    return check_inventory_service(
        request,
        current_user
    )


@router.post("/inventory_update")
def inventory_update(
    request: ProductRequest,
    current_user: User_role = Depends(get_current_user)
):
    return inventory_update_service(
        request,
        current_user
    )