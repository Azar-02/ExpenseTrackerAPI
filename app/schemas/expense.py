from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class ExpenseCreate(BaseModel):

    title: str = Field(min_length=2, max_length=100)

    amount: Decimal = Field(gt=0)

    category: str = Field(min_length=2, max_length=50)

    description: Optional[str] = Field(default=None, max_length=255)

    expense_date: date

class ExpenseResponse(BaseModel):

    id: int

    title: str

    amount: Decimal

    category: str

    description: Optional[str]

    expense_date: date

    model_config = ConfigDict(from_attributes=True)

class ExpenseUpdate(BaseModel):

    title: Optional[str] = Field(default=None, min_length=2, max_length=100)

    amount: Optional[Decimal] = Field(default=None, gt=0)

    category: Optional[str] = Field(default=None, min_length=2, max_length=50)

    description: Optional[str] = Field(default=None, max_length=255)

    expense_date: Optional[date] = None