from fastapi import APIRouter , Depends
from constants.roles import UserRole
from dependencies.roles import required_role


router= APIRouter(
    prefix="/worker", 
    tags=["/Worker"], 
    dependencies=[Depends(required_role(UserRole.WORKER))]
)

@router.get("/")
def worker_dashboard():
    return{
        "massage" : "welcome Worker"
    }