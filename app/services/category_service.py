from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.category_repository import CategoryRepository
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
)


class CategoryService:

    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)

    def create_category(
        self,
        category: CategoryCreate,
    ):

        existing = self.repository.get_category_by_name(
            category.name
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category already exists.",
            )

        return self.repository.create_category(category)

    def get_categories(self):

        return self.repository.get_categories()

    def get_category(
        self,
        category_id: int,
    ):

        category = self.repository.get_category(category_id)

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found.",
            )

        return category

    def update_category(
        self,
        category_id: int,
        category: CategoryUpdate,
    ):

        db_category = self.get_category(category_id)

        existing = self.repository.get_category_by_name(
            category.name
        )

        if existing and existing.id != category_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category already exists.",
            )

        return self.repository.update_category(
            db_category,
            category,
        )

    def delete_category(
        self,
        category_id: int,
    ):

        db_category = self.get_category(category_id)

        self.repository.delete_category(db_category)