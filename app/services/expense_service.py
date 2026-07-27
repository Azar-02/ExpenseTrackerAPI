from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.expense_repository import ExpenseRepository
from app.schemas.expense import ExpenseCreate,ExpenseUpdate
from datetime import date
from decimal import Decimal
from typing import Optional

class ExpenseService:

    # Create Service
    def __init__(self, db: Session):
        self.repository = ExpenseRepository(db)

    # Create Expense
    def create_expense(self, expense_data: ExpenseCreate, current_user: User):
        return self.repository.create(
            title = expense_data.title,
            amount = expense_data.amount,
            category = expense_data.category,
            description = expense_data.description,
            expense_date = expense_data.expense_date,
            owner_id = current_user.id
        )

    # Get All Expenses
    def get_expenses(
    self,
    current_user: User,
    page: int,
    size: int,
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    min_amount: Optional[Decimal] = None,
    max_amount: Optional[Decimal] = None,
    sort_by: str = "expense_date",
    order: str = "desc",
):

        return self.repository.get_all(
            owner_id=current_user.id,
            page=page,
            size=size,
            category=category,
            start_date=start_date,
            end_date=end_date,
            min_amount=min_amount,
            max_amount=max_amount,
            sort_by=sort_by,
            order=order,
        )

    # Get One Expense
    def get_expense(self, expense_id: int, current_user: User):

        expense = self.repository.get_by_id(expense_id, current_user.id)

        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not found"
            )

        return expense

    # Update Expense
    def update_expense(self, expense_id: int, expense_data: ExpenseUpdate, current_user: User):

        expense = self.get_expense(expense_id, current_user)

        update_data = expense_data.model_dump(exclude_unset=True)

        return self.repository.update(expense, update_data)

    # Delete Expense 
    def delete_expense(self, expense_id: int, current_user: User):

        expense = self.get_expense(expense_id, current_user)

        self.repository.delete(expense)