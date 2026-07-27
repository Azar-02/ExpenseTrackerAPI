from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.auth.oauth import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from app.services.expense_service import ExpenseService
from datetime import date
from decimal import Decimal
from typing import Optional
from fastapi import Query
from app.schemas.dashboard import DashboardResponse

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
@router.get("/", response_model=list[ExpenseResponse])
def get_expenses(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    min_amount: Optional[Decimal] = None,
    max_amount: Optional[Decimal] = None,
    sort_by: str = Query(
        "expense_date",
        pattern="^(title|amount|category|expense_date)$",
    ),
    order: str = Query(
        "desc",
        pattern="^(asc|desc)$",
    ),
    search: Optional[str] = Query(
        default=None,
        description="Search by title or description",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = ExpenseService(db)

    return service.get_expenses(
        current_user=current_user,
        page=page,
        size=size,
        category=category,
        start_date=start_date,
        end_date=end_date,
        min_amount=min_amount,
        max_amount=max_amount,
        sort_by=sort_by,
        order=order,
        search=search,
    )

# Dashboard
@router.get("/dashboard", response_model=DashboardResponse)

def get_dashboard(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    service = ExpenseService(db)

    return service.get_dashboard(current_user.id)

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

