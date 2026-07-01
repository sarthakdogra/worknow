from fastapi import APIRouter , Depends , status
from constants.roles import UserRole
from dependencies.roles import required_role
from schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
)

from service.categoryService import CategoryService
from database import get_db
from sqlalchemy.orm import Session


router= APIRouter(
    prefix="/admin", 
    tags=["/Admin"], 
    dependencies=[Depends(required_role(UserRole.ADMIN))]
)

@router.post(
    "/categories",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
):
    return CategoryService.create_category(
        db=db,
        category_data=category,
    )


@router.put(
    "/categories/{category_id}",
    response_model=CategoryResponse,
)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
):
    return CategoryService.update_category(
        db=db,
        category_id=category_id,
        category_data=category,
    )


@router.delete(
    "/categories/{category_id}",
    status_code=status.HTTP_200_OK,
)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    return CategoryService.delete_category(
        db=db,
        category_id=category_id,
    )