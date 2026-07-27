from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_category(
        self,
        category: CategoryCreate,
    ) -> Category:

        db_category = Category(
            name=category.name
        )

        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)

        return db_category

    def get_categories(self) -> list[Category]:

        return self.db.query(Category).order_by(Category.name).all()

    def get_category(
        self,
        category_id: int,
    ) -> Category | None:

        return (
            self.db.query(Category)
            .filter(Category.id == category_id)
            .first()
        )

    def get_category_by_name(
        self,
        name: str,
    ) -> Category | None:

        return (
            self.db.query(Category)
            .filter(Category.name == name)
            .first()
        )

    def update_category(
        self,
        db_category: Category,
        category: CategoryUpdate,
    ) -> Category:

        db_category.name = category.name

        self.db.commit()
        self.db.refresh(db_category)

        return db_category

    def delete_category(
        self,
        db_category: Category,
    ) -> None:

        self.db.delete(db_category)
        self.db.commit()