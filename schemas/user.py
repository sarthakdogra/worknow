from pydantic import BaseModel , EmailStr

class UserBase(BaseModel):
    email:EmailStr
    role: str
    name: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

class UserLogin(BaseModel):
    email:EmailStr
    password: str

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str