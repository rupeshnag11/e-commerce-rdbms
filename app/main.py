from dotenv import load_dotenv
from sqlalchemy import create_engine, update
from fastapi import FastAPI, Request, Depends, Cookie, Response
from sqlalchemy import MetaData, Table, Column, Integer, String,DateTime
from pydantic import BaseModel
import os
import bcrypt
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
import secrets
from datetime import datetime, timedelta, timezone


load_dotenv()

app= FastAPI()
database_url = os.getenv("DATABASE_URL")


engine = create_engine(database_url)
print("database connection is successful")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() #link python calss with databse directly.

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserSession(Base):
    __tablename__ = "user_sessions"

    session_id = Column(String, primary_key=True)
    user_id = Column(Integer, nullable=False)
    expires_at = Column(DateTime, nullable=False)



class User_role(Base): #user table structure in postgres database.
    __tablename__ = "users_role"
    user_id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    hashed_password =Column(String, unique=True)


class UserCreate(BaseModel): #Validate incoming JSON data from the registration form.
    username : str
    email : EmailStr
    password : str

class UserResponse(BaseModel):
    user_id : int
    username : str
    email: EmailStr

    class config:
        from_attributes = True

pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")
def hashed_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)


@app.post("/register")  #user registration 
def register(user_data : UserCreate , db : Session = Depends(get_db)):
    existing_mail = db.query(
        User_role
        ).filter(User_role.email == user_data.email).first()
    if existing_mail: #check existing email
        return{
            "status": "email is already registered"
        }
    secure_password = hashed_password(user_data.password)

    new_user = User_role(
        username=user_data.username,
        email=user_data.email,
        hashed_password=secure_password)  
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return{
        "status": "User created successfully",
        "email": new_user.email
    }

class LoginRequest(BaseModel):
    email: EmailStr
    password :str


@app.post("/login")
def login(user_data:LoginRequest,response :Response, db: Session = Depends(get_db)):
    user = db.query(User_role).filter(
        User_role.email == user_data.email
    ).first()
    if not user:
        return{
            "status":"user not found"
        }

    if not verify_password(user_data.password,user.hashed_password):
        return{
            "status":"invalid password"
        }

    session_id = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(hours=24)

    print("-------------------------------------")
    print("SESSION CREATED")
    print("session_id:", session_id)
    print("user_id:", user.user_id)
    print("created_at:", datetime.now(timezone.utc))
    print("expires_at:", expires_at)
    print("------------------------------------")

    new_session = UserSession(
        session_id=session_id,
        user_id=user.user_id,
        expires_at=expires_at
    )

    db.add(new_session)
    db.commit()

    response.set_cookie(
        key="session_id",
        value=session_id,
        max_age=604800, #7 days in seconds
        httponly=True,   # Prevents JavaScript access (protects against XSS)
        secure=True,     # Ensures cookie is only sent over encrypted HTTPS
        samesite="lax")

    return {
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "status":"login succeesful"
    }


@app.post("/logout")
def logout(
    response: Response,
    session_id: str = Cookie(None),
    db: Session = Depends(get_db)
):
    if session_id:
        session = db.query(UserSession).filter(
            UserSession.session_id == session_id
        ).first()

        if session:
            db.delete(session)
            db.commit()

    response.delete_cookie("session_id")

    return {
        "status": "logout successful"
    }


#helath check
@app.get("/health")
def health():
    return {"message": "OK"}

metadata = MetaData()

user_table_name = Table("users", metadata, autoload_with=engine)

class user_request(BaseModel):
    user_id : int
    
@app.post("/users_details")
def users_details(request: user_request):
    with engine.connect() as conn:
        result = conn.execute(
            user_table_name.select().where(
                user_table_name.c.user_id == request.user_id))
        return [dict(row._mapping) for row in result]

@app.post("/get_user_past_n_orders")
def get_user_past_orders(request: user_request):
    with engine.connect() as conn:
        result = conn.execute(
            order_table_name.select().where(
                order_table_name.c.user_id == request.user_id))
        return [dict(row._mapping) for row in result]

product_table_name = Table("products", metadata, autoload_with=engine)
cart_table_name = Table("cart", metadata, autoload_with=engine)
inventory_table_name = Table("inventory", metadata, autoload_with=engine)
order_table_name =Table("orders", metadata, autoload_with=engine)


class product_request(BaseModel):
    product_id : int
    quantity : int
    user_id :int

@app.post('/check_inventory')
def check_inventory(request: product_request):

    with engine.connect() as conn:
        result = conn.execute(
            inventory_table_name.select().where(
                inventory_table_name.c.product_id == request.product_id
            )).fetchone()
        
    inventory = dict(result._mapping)
    if inventory['available_quantity'] >= request.quantity:
        return {

            "available": True,
            "product_id": request.product_id,
            "requested_quantity": request.quantity,
        }

        
    else:
        return {
                'available': False,
                'available_quantity': inventory['available_quantity'],
                'product_id': request.product_id
                }


@app.post("/purchase_order")
def purchase_order(request: product_request):
    inventory = check_inventory(request)
    if inventory['available'] == False:
        return {
            "status":"no stock"
        }
    with engine.connect() as conn:
        result=conn.execute(
            product_table_name.select().where(
                product_table_name.c.product_id == request.product_id
            )
        ).fetchone()
    product = dict(result._mapping)
    total_amount = product['price'] * request.quantity
    inventory_result = inventory_update(request)


    order_result = create_order(
        order_request(
        user_id=request.user_id,
        total_amount=total_amount
        )
    )
    return {
        "status": "purchase successful",
        "user_id": request.user_id,
        "product_id": request.product_id,
        "quantity": request.quantity,
        "total_amount": total_amount,
        "inventory": inventory_result,
        "order": order_result
    }



class cart_request(BaseModel):
    user_id: int
    total_amount: float


@app.post("/create_cart")
def create_cart(request: cart_request):
    with engine.connect() as conn:
        conn.execute(
            cart_table_name.insert().values(
                user_id=request.user_id,
                total_amount=request.total_amount
            )
        )

    return {
        "cart": True,
        "status": "cart is created",
        "user_id": request.user_id,
        "total_amount": request.total_amount
    }

class order_request(BaseModel):
    user_id: int
    total_amount:float

@app.post("/create_order")
def create_order(request: order_request):
    with engine.connect() as conn:
        conn.execute(
            order_table_name.insert().values(
                user_id=request.user_id,
                total_amount=request.total_amount
            )
        )

    return {
        "order": True,
        "status": "order is created",
        "user_id": request.user_id,
        "total_amount": request.total_amount
    }

@app.post('/inventory_update')
def inventory_update(request: product_request):
    with engine.connect() as conn:
        conn.execute(
            inventory_table_name.update().where(
                inventory_table_name.c.product_id == request.product_id
            ).values(
                reserved_quantity= inventory_table_name.c.reserved_quantity + request.quantity,
                available_quantity = inventory_table_name.c.available_quantity - request.quantity
            )
        )
    return{
        "status":"inventory updated",
        "product_id": request.product_id,
        "quantity": request.quantity
        
    }

