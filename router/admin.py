from fastapi import APIRouter , Depends
from constants.roles import UserRole
from dependencies.roles import required_role


router= APIRouter(
    prefix="/admin", 
    tags=["/Admin"], 
    dependencies=[Depends(required_role(UserRole.ADMIN))]
)

@router.get("/")
def admin_dashboard():
    return{
        "massage" : "welcome Admin"
    }