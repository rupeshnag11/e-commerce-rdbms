from dotenv import load_dotenv
from sqlalchemy import create_engine, update
from fastapi import FastAPI, Request, Depends, HTTPException, Response
from sqlalchemy import MetaData, Table, Column, Integer, String
from pydantic import BaseModel
import os
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials



load_dotenv()

app= FastAPI()
database_url = os.getenv("DATABASE_URL")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
JWT_EXPIRES_MINUTES = 30

engine = create_engine(database_url)
print("----------------------------------------")
print("database connection is successful")
print("----------------------------------------")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() #link python calss with database directly.

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class User_role(Base): #user table structure in postgres database.
    __tablename__ = "users_role"
    user_id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    hashed_password =Column(String, unique=False)


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

def create_access_token(user_id:int):
    expire = datetime.now(timezone.utc) + timedelta(minutes= JWT_EXPIRES_MINUTES)
    payload={
        "sub" : str(user_id),
        "exp" : expire
    }
    token = jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )
    return token

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),
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
        except JWTError:
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
def login(user_data:LoginRequest, response: Response, db: Session = Depends(get_db)):
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
    db.commit()

    access_token = create_access_token(user.user_id)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=1800)

    
    return {
        "access_token":access_token,
        "token_type": "bearer",
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "status":"login succeesful"
    }

class LogoutRequest(BaseModel):
    email: EmailStr
    password :str

@app.post("/logout")
def logout(user_data:LogoutRequest, response:Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="lax"
    )
    return{
        "status":"sucessfully logout",
        "user_data": user_data

    }


#health check
@app.get("/health")
def health():
    return {"message": "OK"}

metadata = MetaData()

user_table_name = Table("users", metadata, autoload_with=engine)

class user_request(BaseModel):
    user_id : int
    
@app.post("/users_details")
def users_details(request: user_request, current_user : User_role = Depends(get_current_user)):
    with engine.connect() as conn:
        result = conn.execute(
            user_table_name.select().where(
                user_table_name.c.user_id == request.user_id))
        return [dict(row._mapping) for row in result]

@app.post("/get_user_past_n_orders")
def get_user_past_orders(current_user :User_role = Depends(get_current_user)):
    with engine.connect() as conn:
        result = conn.execute(
            order_table_name.select().where(
                order_table_name.c.user_id == current_user.user_id))
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

