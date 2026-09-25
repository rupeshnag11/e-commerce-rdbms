from sqlalchemy import MetaData, Table
from app.database.database import engine


metadata = MetaData()

order_table_name = Table(
    "orders",
    metadata,
    autoload_with=engine
)


def get_user_details_service(current_user):
    return {
        "user_id": current_user.user_id,
        "username": current_user.username,
        "email": current_user.email
    }


def get_user_past_orders_service(current_user):
    with engine.connect() as conn:
        result = conn.execute(
            order_table_name.select().where(
                order_table_name.c.user_id == current_user.user_id
            )
        )
    return [dict(row._mapping) for row in result]