from fastapi import APIRouter, Depends, Response
from app.schemas.user import UserCreate
from app.schemas.user import LoginRequest
from app.models.models import User_role
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.services.auth_service import hashed_password, verify_password, create_access_token


router = APIRouter()

@router.post("/register")
def register(user_data: UserCreate, 
            db: Session = Depends(get_db)):
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


@router.post("/login")
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


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")

    return {
        "status": "successfully logout"
    }