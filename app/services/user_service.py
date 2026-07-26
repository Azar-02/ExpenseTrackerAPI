from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository


class UserService:

    def __init__(self, db: Session):
        self.repository = UserRepository(db)