from sqlalchemy import DateTime, ForeignKey, Integer, String, Column, text ,BigInteger, Text, Numeric, Boolean
from app.database.database import Base
class User_role(Base):
    __tablename__ = "users_role"

    user_id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(150))
    phone = Column(String(20))
    password = Column(String(100))
    created_at = Column(DateTime,server_default=text("CURRENT_TIMESTAMP"))

class UserSession(Base):
    __tablename__ = "user_sessions"

    session_id = Column(String(255), primary_key=True)
    user_id = Column(Integer,ForeignKey("users_role.user_id", ondelete="CASCADE"), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)


class Address(Base):
    __tablename__ = "address"

    address_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    address_line = Column(String(200))
    city = Column(String(100))
    state = Column(String(100))
    pincode = Column(String(10))
    country = Column(String(50))

class Inventory(Base):
    __tablename__ = "inventory"

    inventory_id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    quantity = Column(Integer)
    reserved_quantity = Column(Integer)
    available_quantity = Column(Integer)
    warehouse_location = Column(String(100))
    stock_status = Column(String(30))
    last_updated = Column(DateTime,server_default=text("CURRENT_TIMESTAMP"))


class Product(Base):
    __tablename__ = "products"

    product_id = Column(BigInteger, primary_key=True)
    product_name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Numeric(12, 2), nullable=False)
    is_active = Column(Boolean, nullable=False, server_default=text("true"))
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))


class Cart(Base):
    __tablename__ = "cart"

    cart_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    total_amount = Column(Numeric(10, 2))
    status = Column(String(30))
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

class CartItem(Base):
    __tablename__ = "cart_items"

    cart_item_id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey("cart.cart_id"), nullable=False)
    product_id = Column(BigInteger, ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(12, 2), nullable=False)


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    total_amount = Column(Numeric(10, 2))
    order_status = Column(String(30))
    order_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id = Column(Integer, primary_key=True)
    order_id = Column(Integer,ForeignKey("orders.order_id") ,nullable=False)
    product_id = Column(BigInteger, ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(12, 2), nullable=False)

class Payment(Base):
    __tablename__ = "payment"

    payment_id = Column(Integer, primary_key=True)
    order_id = Column(Integer)
    payment_method = Column(String(30))
    payment_status = Column(String(30))
    amount = Column(Numeric(10, 2))
    transaction_id = Column(String(100))
    payment_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    user_id = Column(Integer,ForeignKey("users.user_id"))

