from dependencies.roles import required_role
from constants.roles import UserRole
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from service.userservice import UserService
from dependencies.auth import get_current_user
from models.user import User

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return UserService.register_user(db, user)


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    return UserService.login_user(db, user)

@router.get("/protected")
async def protected_route(current_user : User=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role
    }



@router.get("/customer")
def customer_route(
    current_user=Depends(required_role(UserRole.CUSTOMER))
):
    return {
        "message": f"Welcome Customer {current_user.name}"
    }


@router.get("/worker")
def worker_route(
    current_user=Depends(required_role(UserRole.WORKER))
):
    return {
        "message": f"Welcome Worker {current_user.name}"
    }


@router.get("/admin")
def admin_route(
    current_user=Depends(required_role(UserRole.ADMIN))
):
    return {
        "message": f"Welcome Admin {current_user.name}"
    }