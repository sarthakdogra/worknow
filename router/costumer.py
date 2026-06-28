from fastapi import APIRouter , Depends
from constants.roles import UserRole
from dependencies.roles import required_role


router= APIRouter(
    prefix="/costumer", 
    tags=["/Customer"], 
    dependencies=[Depends(required_role(UserRole.CUSTOMER))]
)

@router.get("/")
def customer_dashboard():
    return{
        "massage" : "welcome Customer"
    }