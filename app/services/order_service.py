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
        cart_result = conn.execute(                          #users active cart search
            cart_table_name.select().where(
                cart_table_name.c.user_id == current_user.user_id,
                cart_table_name.c.status == "active"
            )
        ).fetchone()
        if cart_result is None:
            raise HTTPException(
                status_code=404,
                detail="Active cart not found"
            )
        cart_id = cart_result._mapping["cart_id"]

        cart_items_result = conn.execute(
            cart_items_table_name.select().where(
                cart_items_table_name.c.cart_id == cart_id,
                cart_items_table_name.c.cart_item_id.in_(request.cart_item_ids)
            )
        ).fetchall()
        cart_items = [dict(row._mapping) for row in cart_items_result]

        if not cart_items:
            raise HTTPException(
                status_code=404,
                detail="No cart items found for the provided IDs"
            )
        total_amount = 0
        for item in cart_items:
            total_amount += item["price"] * item["quantity"]

        order_result = conn.execute(        #order creation for the user with total amount and user id
            order_table_name.insert()
            .values(
                user_id=current_user.user_id,
                total_amount=total_amount
            ).returning(order_table_name.c.order_id)
        )
        order_id = order_result.scalar_one()  #order id is generated for the user

        for item in cart_items: #order items creation
            conn.execute(
                order_items_table_name.insert().values(
                    order_id=order_id,
                    product_id=item["product_id"],
                    quantity=item["quantity"],
                    price=item["price"]
                )
            )
        #items are removed from the cart after order creation
        conn.execute(
            cart_items_table_name.delete().where(
                cart_items_table_name.c.cart_id == cart_id,
                cart_items_table_name.c.cart_item_id.in_(request.cart_item_ids)
            )
        )
        return {
            "order": True,
            "status": "order created successfully",
            "order_id": order_id,
            "user_id": current_user.user_id,
            "total_amount": total_amount,
            "cart_item_ids": request.cart_item_ids
    }
