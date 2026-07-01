from fastapi import APIRouter , Depends
from typing import List
from constants.roles import UserRole
from dependencies.roles import required_role
from sqlalchemy.orm import Session
from database import get_db
from schemas.category import CategoryResponse 
from service.categoryService import CategoryService

router= APIRouter(
    prefix="/costumer", 
    tags=["/Customer"], 
    dependencies=[Depends(required_role(UserRole.CUSTOMER))]
)

@router.get(
    "/categories",
    response_model=List[CategoryResponse],
)
def get_all_categories(
    db: Session = Depends(get_db),
):
    return CategoryService.get_all_categories(db)


@router.get(
    "/categories/{category_id}",
    response_model=CategoryResponse,
)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    return CategoryService.get_category_by_id(
        db=db,
        category_id=category_id,
    )