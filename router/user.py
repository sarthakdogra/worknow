from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.user import UserCreate, UserLogin
from service.authservice import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register/customer",
    status_code=status.HTTP_201_CREATED,
)
def register_customer(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    return AuthService.register_customer(
        db=db,
        user_data=user,
    )


@router.post(
    "/register/worker",
    status_code=status.HTTP_201_CREATED,
)
def register_worker(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    return AuthService.register_worker(
        db=db,
        user_data=user,
    )


@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    return AuthService.login(
        db=db,
        login_data=user,
    )