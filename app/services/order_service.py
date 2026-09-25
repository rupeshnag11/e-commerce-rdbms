from fastapi import HTTPException
from sqlalchemy import MetaData, Table
from app.database.database import engine

metadata = MetaData()

order_table_name = Table(
    "orders",
    metadata,
    autoload_with=engine
)

order_items_table_name = Table(
    "order_items",
    metadata,
    autoload_with=engine
)

product_table_name = Table(
    "products",
    metadata,
    autoload_with=engine
)


inventory_table_name = Table(
    "inventory",
    metadata,
    autoload_with=engine
)


def purchase_order_service(
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

        inventory_result = conn.execute(
            inventory_table_name.update()
            .where(
                inventory_table_name.c.product_id == request.product_id,
                inventory_table_name.c.available_quantity >= request.quantity
            )
            .values(
                reserved_quantity=(
                    inventory_table_name.c.reserved_quantity + request.quantity
                ),
                available_quantity=(
                    inventory_table_name.c.available_quantity - request.quantity
                )
            )
        )

        if inventory_result.rowcount != 1:
            raise HTTPException(
                status_code=400,
                detail="Insufficient stock"
            )

        order_result = conn.execute(
            order_table_name.insert()
            .values(
                user_id=current_user.user_id,
                total_amount=total_amount
            )
            .returning(order_table_name.c.order_id)
        )

        order_id = order_result.scalar_one()

        conn.execute(
            order_items_table_name.insert().values(
                order_id=order_id,
                product_id=request.product_id,
                quantity=request.quantity,
                price=product["price"]
            )
        )

    return {
        "status": "purchase successful",
        "user_id": current_user.user_id,
        "product_id": request.product_id,
        "quantity": request.quantity,
        "total_amount": total_amount,
        "order_id": order_id
    }


def create_order_service(
    request,
    current_user
):
    with engine.begin() as conn:

        result = conn.execute(
            order_table_name.insert()
            .values(
                user_id=current_user.user_id,
                total_amount=request.total_amount
            )
            .returning(order_table_name.c.order_id)
        )

        order_id = result.scalar_one()

    return {
        "order": True,
        "status": "order is created",
        "order_id": order_id,
        "user_id": current_user.user_id,
        "total_amount": request.total_amount
    }