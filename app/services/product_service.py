from sqlalchemy import MetaData, Table
from app.database.database import engine

metadata = MetaData()

product_table_name = Table(
    "products",
    metadata,
    autoload_with=engine
)


def get_products_service():
    with engine.connect() as conn:
        result = conn.execute(
            product_table_name.select().where(
                product_table_name.c.is_active == True
            )
        )
        return [dict(row._mapping) for row in result]