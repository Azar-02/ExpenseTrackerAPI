from decimal import Decimal
from pydantic import BaseModel


class CategorySummary(BaseModel):
    category: str
    total: Decimal


class HighestExpense(BaseModel):
    title: str
    amount: Decimal


class DashboardResponse(BaseModel):
    total_expenses: Decimal
    today_expenses: Decimal
    monthly_expenses: Decimal
    highest_expense: HighestExpense | None
    category_summary: list[CategorySummary]