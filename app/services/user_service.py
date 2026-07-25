from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserLogin
from app.utils.security import hash_password, verify_password
from app.auth.jwt import create_access_token

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
        password_hash = hash_password(user_data.password)

        # Save user
        user = self.repository.create(
            name=user_data.name,
            email=user_data.email,
            password_hash=password_hash
        )
        return user

    def login_user(self, user_data: UserLogin):
        
        # Get user by email
        user = self.repository.get_by_email(user_data.email)

        if not user or not verify_password(user_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Create access token
        access_token = create_access_token({"sub": str(user.id)})

        return {"access_token": access_token, "token_type": "bearer"}

    

