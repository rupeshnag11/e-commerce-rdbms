from app.database.database import SessionLocal
from app.models.models import Product


products = [
    {
        "product_id": 1,
        "product_name": "iPhone 16",
        "description": "Apple smartphone with 128GB storage",
        "price": 69999.00,
        "is_active": True,
    },
    {
        "product_id": 2,
        "product_name": "Samsung Galaxy S25",
        "description": "Samsung flagship Android smartphone",
        "price": 74999.00,
        "is_active": True,
    },
    {
        "product_id": 3,
        "product_name": "OnePlus 13",
        "description": "Premium Android smartphone",
        "price": 64999.00,
        "is_active": True,
    },
    {
        "product_id": 4,
        "product_name": "Google Pixel 9",
        "description": "Google smartphone with advanced camera",
        "price": 79999.00,
        "is_active": True,
    },
    {
        "product_id": 5,
        "product_name": "Redmi Note 14 Pro",
        "description": "Affordable Android smartphone",
        "price": 29999.00,
        "is_active": True,
    },
    {
        "product_id": 6,
        "product_name": "Dell Inspiron 15",
        "description": "15-inch laptop with Intel processor",
        "price": 58999.00,
        "is_active": True,
    },
    {
        "product_id": 7,
        "product_name": "HP Pavilion 14",
        "description": "14-inch performance laptop",
        "price": 62999.00,
        "is_active": True,
    },
    {
        "product_id": 8,
        "product_name": "Lenovo IdeaPad Slim 5",
        "description": "Slim laptop for work and study",
        "price": 54999.00,
        "is_active": True,
    },
    {
        "product_id": 9,
        "product_name": "MacBook Air M3",
        "description": "Apple laptop with M3 processor",
        "price": 109999.00,
        "is_active": True,
    },
    {
        "product_id": 10,
        "product_name": "ASUS Vivobook 15",
        "description": "15-inch productivity laptop",
        "price": 51999.00,
        "is_active": True,
    },
    {
        "product_id": 11,
        "product_name": "Sony WH-1000XM5",
        "description": "Wireless noise cancelling headphones",
        "price": 29999.00,
        "is_active": True,
    },
    {
        "product_id": 12,
        "product_name": "Apple AirPods Pro",
        "description": "Wireless earbuds with active noise cancellation",
        "price": 24999.00,
        "is_active": True,
    },
    {
        "product_id": 13,
        "product_name": "JBL Tune 770NC",
        "description": "Wireless noise cancelling headphones",
        "price": 7999.00,
        "is_active": True,
    },
    {
        "product_id": 14,
        "product_name": "boAt Airdopes 141",
        "description": "Affordable wireless earbuds",
        "price": 1499.00,
        "is_active": True,
    },
    {
        "product_id": 15,
        "product_name": "Logitech MX Master 3S",
        "description": "Wireless productivity mouse",
        "price": 8999.00,
        "is_active": True,
    },
    {
        "product_id": 16,
        "product_name": "Samsung 27 Inch Monitor",
        "description": "Full HD IPS monitor",
        "price": 18999.00,
        "is_active": True,
    },
    {
        "product_id": 17,
        "product_name": "LG UltraGear 24 Inch",
        "description": "Gaming monitor with high refresh rate",
        "price": 15999.00,
        "is_active": True,
    },
    {
        "product_id": 18,
        "product_name": "Amazon Echo Dot",
        "description": "Smart speaker with Alexa",
        "price": 5499.00,
        "is_active": True,
    },
    {
        "product_id": 19,
        "product_name": "Kindle Paperwhite",
        "description": "E-reader with high resolution display",
        "price": 13999.00,
        "is_active": True,
    },
    {
        "product_id": 20,
        "product_name": "Mi Smart LED TV 43 Inch",
        "description": "4K smart television",
        "price": 32999.00,
        "is_active": True,
    },
    {
        "product_id": 21,
        "product_name": "Atomic Habits",
        "description": "Self-improvement book",
        "price": 599.00,
        "is_active": True,
    },
    {
        "product_id": 22,
        "product_name": "The Alchemist",
        "description": "Fiction novel",
        "price": 399.00,
        "is_active": True,
    },
    {
        "product_id": 23,
        "product_name": "Parker Ball Pen",
        "description": "Premium blue ink ball pen",
        "price": 299.00,
        "is_active": True,
    },
    {
        "product_id": 24,
        "product_name": "Classmate Notebook",
        "description": "A5 ruled notebook for writing and study",
        "price": 149.00,
        "is_active": True,
    },
    {
        "product_id": 25,
        "product_name": "Casio Scientific Calculator",
        "description": "Scientific calculator for students",
        "price": 899.00,
        "is_active": True,
    },
]


def seed_products():
    db = SessionLocal()

    try:
        inserted = 0
        skipped = 0

        for product_data in products:
            existing_product = db.query(Product).filter(
                Product.product_id == product_data["product_id"]
            ).first()

            if existing_product:
                skipped += 1
                continue

            product = Product(**product_data)
            db.add(product)
            inserted += 1

        db.commit()

        print(f"Products inserted: {inserted}")
        print(f"Products skipped: {skipped}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_products()