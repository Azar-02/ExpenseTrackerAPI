from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreate(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=100,
        description="Full Name"
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
        description="User Password"
    )


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True
    )

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

