from datetime import date
from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import Session
from app.models.expense import Expense


class ExpenseRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        title: str,
        amount: Decimal,
        category: str,
        description: Optional[str],
        expense_date: date,
        owner_id: int,
    ) -> Expense:

        expense = Expense(
            title=title,
            amount=amount,
            category=category,
            description=description,
            expense_date=expense_date,
            owner_id=owner_id,
        )

        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)

        return expense

    def get_all(
    self,
    owner_id: int,
    page: int,
    size: int,
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    min_amount: Optional[Decimal] = None,
    max_amount: Optional[Decimal] = None,
):

        query = (
            self.db.query(Expense)
            .filter(Expense.owner_id == owner_id)
        )

        if category:
            query = query.filter(
                Expense.category == category
            )

        if start_date:
            query = query.filter(
                Expense.expense_date >= start_date
            )

        if end_date:
            query = query.filter(
                Expense.expense_date <= end_date
            )

        if min_amount:
            query = query.filter(
                Expense.amount >= min_amount
            )

        if max_amount:
            query = query.filter(
                Expense.amount <= max_amount
            )

        offset = (page - 1) * size

        return (
            query.order_by(
                Expense.expense_date.desc()
            )
            .offset(offset)
            .limit(size)
            .all()
        )

    def get_by_id(
        self,
        expense_id: int,
        owner_id: int,
    ):

        return (
            self.db.query(Expense)
            .filter(
                Expense.id == expense_id,
                Expense.owner_id == owner_id,
            )
            .first()
        )

    def update(
        self,
        expense: Expense,
        update_data: dict,
    ):

        for field, value in update_data.items():
            if hasattr(expense, field):
                setattr(expense, field, value)

        self.db.commit()
        self.db.refresh(expense)

        return expense

    def delete(self, expense: Expense):

        self.db.delete(expense)
        self.db.commit()