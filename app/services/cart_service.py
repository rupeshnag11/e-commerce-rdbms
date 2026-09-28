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
        cart_result = conn.execute(                       #any cart is already present for the user or not, if not then create a new cart for the user
            cart_table_name.select().where(
                cart_table_name.c.user_id == current_user.user_id,
                cart_table_name.c.status == "active"
            )
        ).fetchone()

        if cart_result is None:                           #no cart found for the user, create a new cart
            cart_result = conn.execute(
                cart_table_name.insert()
                .values(
                    user_id=current_user.user_id,
                    total_amount=0,
                    status="active"
                )
                .returning(cart_table_name.c.cart_id)
            )

            cart_id = cart_result.scalar_one()

        else:
            cart_id = cart_result._mapping["cart_id"]

        total_amount = 0

        for item in request.items:
            product_result = conn.execute(
                product_table_name.select().where(
                    product_table_name.c.product_id == item.product_id
                )
            ).fetchone()

            if product_result is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product with ID {item.product_id} not found"
                )

            product = dict(product_result._mapping)

            item_total = product["price"] * item.quantity

            total_amount += item_total

            conn.execute(
                cart_items_table_name.insert().values(
                    cart_id=cart_id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=product["price"]
                )
            )
        conn.execute(
            cart_table_name.update()
            .where(
                cart_table_name.c.cart_id == cart_id
            )
            .values(
                total_amount=total_amount
            )
        )

    return {
        "cart": True,
        "status": "products added to cart",
        "user_id": current_user.user_id,
        "cart_id": cart_id,
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