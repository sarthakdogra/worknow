from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from constants.roles import UserRole
from models.user import User
from schemas.user import UserCreate, UserLogin
from security.hashhelper import HashHelper
from security.authhelper import AuthHelper


class AuthService:

    @staticmethod
    def _register_user(
        db: Session,
        user_data: UserCreate,
        role: UserRole,
    ):

        existing_user = (
            db.query(User)
            .filter(User.email == user_data.email)
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered."
            )

        hashed_password = HashHelper.hash_password(
            user_data.password
        )

        user = User(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_password,
            role=role.value,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return {
            "message": f"{role.value.capitalize()} registered successfully."
        }

    @staticmethod
    def register_customer(
        db: Session,
        user_data: UserCreate,
    ):
        return AuthService._register_user(
            db=db,
            user_data=user_data,
            role=UserRole.CUSTOMER,
        )

    @staticmethod
    def register_worker(
        db: Session,
        user_data: UserCreate,
    ):
        return AuthService._register_user(
            db=db,
            user_data=user_data,
            role=UserRole.WORKER,
        )

    @staticmethod
    def login(
        db: Session,
        login_data: UserLogin,
    ):

        user = (
            db.query(User)
            .filter(User.email == login_data.email)
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials."
            )

        if not HashHelper.verify_password(
            login_data.password,
            user.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials."
            )

        token = AuthHelper.create_access_token(
            {
                "user_id" :user.id
            }
        )
        

        return {
            "access_token": token,
            "token_type": "bearer",
            "role": user.role,
        }