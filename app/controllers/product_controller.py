from fastapi import APIRouter
from app.services.product_service import get_products_service

router = APIRouter()

@router.get("/products")
def get_products():
    return get_products_service()