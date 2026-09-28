from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.controllers.auth_controller import router as auth_router
from app.controllers.user_controller import router as user_router
from app.controllers.product_controller import router as product_router
from app.controllers.cart_controller import router as cart_router
from app.controllers.inventory_controller import router as inventory_router
from app.controllers.order_controller import router as order_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {
        "message": "OK"
    }

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(inventory_router)
app.include_router(order_router)