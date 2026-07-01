from fastapi import APIRouter , Depends
from constants.roles import UserRole
from dependencies.roles import required_role
from sqlalchemy.orm import Session
from database import get_db
from schemas.worker import WorkerResponse , WorkerCreate , WorkerUpdate
from dependencies.auth import get_current_user
from service.workerservice import WorkerService
from fastapi import   status



router= APIRouter(
    prefix="/worker", 
    tags=["Worker"], 
    dependencies=[Depends(required_role(UserRole.WORKER))]
)

@router.post("/profile" , response_model=WorkerResponse , status_code=status.HTTP_201_CREATED)
def worker_profile(  worker: WorkerCreate ,db:Session=Depends(get_db) , current_user=Depends(get_current_user)):
    return WorkerService.create_worker_profile(db  , current_user , worker_data=worker)


@router.get("/profile" , response_model=WorkerResponse)
def getWorker(db:Session=Depends(get_db) , current_user=Depends(get_current_user)):
    return WorkerService.get_worker_profile(db , current_user)

@router.put("/profile" , response_model= WorkerResponse)
def updateWorker( worker: WorkerUpdate, db:Session=Depends(get_db) ,  current_user=Depends(get_current_user)):
    return WorkerService.update_worker_profile(db  , current_user , worker_data=worker)

@router.delete("/profile" , status_code=status.HTTP_200_OK )
def deleteWorker(db:Session=Depends(get_db) , current_user=Depends(get_current_user)):
    return WorkerService.delete_worker_profile(db , current_user)