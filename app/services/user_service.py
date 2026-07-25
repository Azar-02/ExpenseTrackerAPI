from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.utils.security import hash_password

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def register_user(self, user_data : UserCreate):
        # Check if email already exists
        existing_user = self.repository.get_by_email(user_data.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
            
        # Hash password
        hashed_password = hash_password(user_data.password)

        # Save user
        user = self.repository.create(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_password
        )
        return user