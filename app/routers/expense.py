from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.oauth import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from app.services.expense_service import ExpenseService

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)

# Create Expense Endpoint
@router.post("", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)

def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    service = ExpenseService(db)

    return service.create_expense(expense, current_user)

# Get All Expenses
@router.get("", response_model=List[ExpenseResponse])

def get_expenses(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    service = ExpenseService(db)

    return service.get_expenses(current_user)

# Get Expense By ID
@router.get("/{expense_id}", response_model=ExpenseResponse)

def get_expense(expense_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    service = ExpenseService(db)

    return service.get_expense(expense_id, current_user)

# Update Expense
@router.put("/{expense_id}",response_model=ExpenseResponse)

def update_expense(expense_id: int, expense: ExpenseUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    service = ExpenseService(db)

    return service.update_expense(expense_id, expense, current_user)

# Delete Expense
@router.delete("/{expense_id}",status_code=status.HTTP_204_NO_CONTENT)

def delete_expense(expense_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    service = ExpenseService(db)

    service.delete_expense(expense_id, current_user)