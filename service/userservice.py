from sqlalchemy.orm import Session
from fastapi import HTTPException , status
from models.user import User
from schemas.user import UserCreate , UserLogin
from security.hashhelper import HashHelper
from security.authhelper import AuthHelper

class UserService:

    def register_user(db: Session , user: UserCreate):

        existing_user=db.query(User).filter(User.email==user.email).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST ,
                detail="Email already registered"
            )
        
        db_user= User(
            name=user.name,
            email=user.email,
            hashed_password=HashHelper.hash_password(user.password),
            role=user.role,
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    def login_user(db: Session , user:UserLogin):
        db_user=db.query(User).filter(User.email==user.email).first()

        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED , detail="Invalid email or paswword"
            )
        
        if not HashHelper.verify_password(user.password , db_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED , detail="Inavlid email or password"
            )
        
        access_token= AuthHelper.create_access_token({
            "id":db_user.id
        })

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }