from fastapi import FastAPI
from app.services.product_service import get_products_service

app = FastAPI()

@app.get("/products")
def get_products():
    return get_products_service()