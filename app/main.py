from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from fastapi import FastAPI, Depends, HTTPException, Response
from pydantic import BaseModel, EmailStr
import os
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()

app = FastAPI()

database_url = os.getenv("DATABASE_URL")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
JWT_EXPIRES_MINUTES = 30

engine = create_engine(database_url)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class User_role(Base):
    __tablename__ = "users_role"

    user_id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    user_id: int
    username: str
    email: EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ProductRequest(BaseModel):
    product_id: int
    quantity: int


class CartRequest(BaseModel):
    product_id: int
    quantity: int


class OrderRequest(BaseModel):
    total_amount: float


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hashed_password(password):
    return pwd_context.hash(password)


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def create_access_token(user_id: int):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=JWT_EXPIRES_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        user_id = int(user_id)

    except (JWTError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user = db.query(User_role).filter(
        User_role.user_id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


metadata = MetaData()

user_table_name = Table(
    "users",
    metadata,
    autoload_with=engine
)

product_table_name = Table(
    "products",
    metadata,
    autoload_with=engine
)

cart_table_name = Table(
    "cart",
    metadata,
    autoload_with=engine
)

inventory_table_name = Table(
    "inventory",
    metadata,
    autoload_with=engine
)

order_table_name = Table(
    "orders",
    metadata,
    autoload_with=engine
)


@app.post("/register")
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    existing_mail = db.query(User_role).filter(
        User_role.email == user_data.email
    ).first()

    if existing_mail:
        return {
            "status": "email is already registered"
        }

    new_user = User_role(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "status": "User created successfully",
        "user_id": new_user.user_id,
        "email": new_user.email
    }


@app.post("/login")
def login(
    user_data: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    user = db.query(User_role).filter(
        User_role.email == user_data.email
    ).first()

    if not user:
        return {
            "status": "user not found"
        }

    if not verify_password(
        user_data.password,
        user.hashed_password
    ):
        return {
            "status": "invalid password"
        }

    access_token = create_access_token(user.user_id)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=1800
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "status": "login successful"
    }


@app.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")

    return {
        "status": "successfully logout"
    }


@app.get("/health")
def health():
    return {
        "message": "OK"
    }


@app.get("/users_details")
def users_details(
    current_user: User_role = Depends(get_current_user)
):
    return {
        "user_id": current_user.user_id,
        "username": current_user.username,
        "email": current_user.email
    }


@app.get("/get_user_past_n_orders")
def get_user_past_orders(
    current_user: User_role = Depends(get_current_user)
):
    with engine.connect() as conn:
        result = conn.execute(
            order_table_name.select().where(
                order_table_name.c.user_id == current_user.user_id
            )
        )

        return [dict(row._mapping) for row in result]


@app.post("/check_inventory")
def check_inventory(
    request: ProductRequest,
    current_user: User_role = Depends(get_current_user)
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


@app.post("/purchase_order")
def purchase_order(
    request: ProductRequest,
    current_user: User_role = Depends(get_current_user)
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
                    inventory_table_name.c.reserved_quantity
                    + request.quantity
                ),
                available_quantity=(
                    inventory_table_name.c.available_quantity
                    - request.quantity
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

    return {
        "status": "purchase successful",
        "user_id": current_user.user_id,
        "product_id": request.product_id,
        "quantity": request.quantity,
        "total_amount": total_amount,
        "order_id": order_id
    }


@app.post("/create_cart")
def create_cart(
    request: CartRequest,
    current_user: User_role = Depends(get_current_user)
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

        conn.execute(
            cart_table_name.insert().values(
                user_id=current_user.user_id,
                product_id=request.product_id,
                quantity=request.quantity,
                total_amount=total_amount
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


@app.post("/create_order")
def create_order(
    request: OrderRequest,
    current_user: User_role = Depends(get_current_user)
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


@app.post("/inventory_update")
def inventory_update(
    request: ProductRequest,
    current_user: User_role = Depends(get_current_user)
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
