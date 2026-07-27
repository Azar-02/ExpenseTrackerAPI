from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.services.category_service import CategoryService

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


# Create Category
@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
):

    service = CategoryService(db)

    return service.create_category(category)


# Get All Categories
@router.get(
    "",
    response_model=List[CategoryResponse],
)
def get_categories(
    db: Session = Depends(get_db),
):

    service = CategoryService(db)

    return service.get_categories()


# Get Category By ID
@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
):

    service = CategoryService(db)

    return service.get_category(category_id)


# Update Category
@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
):

    service = CategoryService(db)

    return service.update_category(
        category_id,
        category,
    )


# Delete Category
@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
):

    service = CategoryService(db)

    service.delete_category(category_id)