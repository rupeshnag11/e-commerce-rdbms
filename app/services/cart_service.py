from fastapi import HTTPException
from sqlalchemy import MetaData, Table
from app.database.database import engine


metadata = MetaData()


cart_table_name = Table(
    "cart",
    metadata,
    autoload_with=engine
)


cart_items_table_name = Table(
    "cart_items",
    metadata,
    autoload_with=engine
)


product_table_name = Table(
    "products",
    metadata,
    autoload_with=engine
)


def create_cart_service(
    request,
    current_user
):
    with engine.begin() as conn:

        product_result = conn.execute(
            product_table_name.select().where(
                product_table_name.c.product_id == request.product_id
            )
        ).fetchone()

        if product_result is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        product = dict(product_result._mapping)

        total_amount = product["price"] * request.quantity

        cart_result = conn.execute(
            cart_table_name.insert().values(
                user_id=current_user.user_id,
                total_amount=total_amount,
                status="active"
            ).returning(
                cart_table_name.c.cart_id
            )
        )

        cart_id = cart_result.scalar_one()

        conn.execute(
            cart_items_table_name.insert().values(
                cart_id=cart_id,
                product_id=request.product_id,
                quantity=request.quantity,
                price=product["price"]
            )
        )

    return {
        "cart": True,
        "status": "cart is created",
        "user_id": current_user.user_id,
        "product_id": request.product_id,
        "quantity": request.quantity,
        "total_amount": total_amount
    }




def get_cart_service(current_user):
    with engine.connect() as conn:
        cart_result = conn.execute(
            cart_table_name.select().where(
                cart_table_name.c.user_id == current_user.user_id,
                cart_table_name.c.status == "active"
            )
        ).fetchone()

        if cart_result is None:
            raise HTTPException(
                status_code=404,
                detail="Cart not found"
            )

        cart = dict(cart_result._mapping)

        result = conn.execute(
            cart_items_table_name.select().where(
                cart_items_table_name.c.cart_id == cart["cart_id"]
            )
        )

        items = [dict(row._mapping) for row in result]

    return {
        "cart_id": cart["cart_id"],
        "user_id": current_user.user_id,
        "total_amount": cart["total_amount"],
        "status": cart["status"],
        "items": items
    }