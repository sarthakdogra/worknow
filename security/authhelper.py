from datetime import datetime , timedelta , timezone
from jose import JWTError , jwt
from config import settings 

class AuthHelper:

    @classmethod
    def create_access_token(cls , data:dict):
        payload=data.copy()

        expire=datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        payload.update({"exp":  expire})

        return jwt.encode(payload , settings.JWT_SECRET_KEY , algorithm=settings.JWT_ALGORITHM)

    @classmethod
    def verify_access_token(cls , token:str) ->dict:

        return jwt.decode(
            token , settings.JWT_SECRET_KEY , algorithms=[settings.JWT_ALGORITHM]
        )