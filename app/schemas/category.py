from pydantic import BaseModel, Field, ConfigDict


class CategoryCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )


class CategoryUpdate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )


class CategoryResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)