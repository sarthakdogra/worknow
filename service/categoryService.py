from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status

from models.category import Category
from schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:

    @staticmethod
    def _get_category(
        db: Session,
        category_id: int,
    ) -> Category:

        category = (
            db.query(Category)
            .filter(
                Category.id == category_id,
                Category.is_active == True,
            )
            .first()
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found.",
            )

        return category

    @staticmethod
    def _check_duplicate(
        db: Session,
        name: str,
        exclude_id: int | None = None,
    ):

        query = (
            db.query(Category)
            .filter(
                func.lower(Category.name) == name.strip().lower(),
                Category.is_active == True,
            )
        )

        if exclude_id is not None:
            query = query.filter(Category.id != exclude_id)

        existing = query.first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category already exists.",
            )

    @staticmethod
    def create_category(
        db: Session,
        category_data: CategoryCreate,
    ):

        CategoryService._check_duplicate(
            db,
            category_data.name,
        )

        category = Category(
            name=category_data.name.strip(),
            description=category_data.description.strip(),
            icon_url=category_data.icon_url,
        )

        try:
            db.add(category)
            db.commit()
            db.refresh(category)

            return category

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_all_categories(
        db: Session,
    ):

        return (
            db.query(Category)
            .filter(Category.is_active == True)
            .order_by(Category.name)
            .all()
        )

    @staticmethod
    def get_category_by_id(
        db: Session,
        category_id: int,
    ):

        return CategoryService._get_category(
            db,
            category_id,
        )

    @staticmethod
    def update_category(
        db: Session,
        category_id: int,
        category_data: CategoryUpdate,
    ):

        category = CategoryService._get_category(
            db,
            category_id,
        )

        update_data = category_data.model_dump(
            exclude_unset=True
        )

        if "name" in update_data:
            CategoryService._check_duplicate(
                db,
                update_data["name"],
                exclude_id=category.id,
            )

        for key, value in update_data.items():

            if isinstance(value, str):
                value = value.strip()

            setattr(category, key, value)

        try:
            db.commit()
            db.refresh(category)

            return category

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def delete_category(
        db: Session,
        category_id: int,
    ):

        category = CategoryService._get_category(
            db,
            category_id,
        )

        category.is_active = False

        try:
            db.commit()

        except Exception:
            db.rollback()
            raise

        return {
            "success": True,
            "message": "Category deleted successfully."
        }