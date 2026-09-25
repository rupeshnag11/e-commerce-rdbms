from fastapi import HTTPException
from sqlalchemy import MetaData, Table
from app.database.database import engine


metadata = MetaData()


inventory_table_name = Table(
    "inventory",
    metadata,
    autoload_with=engine
)


def check_inventory_service(
    request,
    current_user
):
    with engine.connect() as conn:

        result = conn.execute(
            inventory_table_name.select().where(
                inventory_table_name.c.product_id == request.product_id
            )
        ).fetchone()

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found in inventory"
        )

    inventory = dict(result._mapping)

    if inventory["available_quantity"] >= request.quantity:
        return {
            "available": True,
            "product_id": request.product_id,
            "requested_quantity": request.quantity,
            "available_quantity": inventory["available_quantity"]
        }

    return {
        "available": False,
        "product_id": request.product_id,
        "requested_quantity": request.quantity,
        "available_quantity": inventory["available_quantity"]
    }


def inventory_update_service(
    request,
    current_user
):
    with engine.begin() as conn:

        result = conn.execute(
            inventory_table_name.update()
            .where(
                inventory_table_name.c.product_id == request.product_id,
                inventory_table_name.c.available_quantity >= request.quantity
            )
            .values(
                reserved_quantity=(
                    inventory_table_name.c.reserved_quantity
                    + request.quantity
                ),
                available_quantity=(
                    inventory_table_name.c.available_quantity
                    - request.quantity
                )
            )
        )

        if result.rowcount != 1:
            raise HTTPException(
                status_code=400,
                detail="Insufficient stock or product not found"
            )

    return {
        "status": "inventory updated",
        "product_id": request.product_id,
        "quantity": request.quantity
    }