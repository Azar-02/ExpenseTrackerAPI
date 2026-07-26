from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.jwt import create_access_token
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserLogin
from app.utils.security import hash_password, verify_password


class AuthService:

    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def register_user(self, user_data: UserCreate):

        existing_user = self.repository.get_by_email(
            user_data.email
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        password_hash = hash_password(
            user_data.password
        )

        return self.repository.create(
            name=user_data.name,
            email=user_data.email,
            password_hash=password_hash
        )

    def login_user(self, user_data: UserLogin):

        user = self.repository.get_by_email(
            user_data.email
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not verify_password(
            user_data.password,
            user.password_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        access_token = create_access_token(
            {
                "sub": str(user.id)
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }