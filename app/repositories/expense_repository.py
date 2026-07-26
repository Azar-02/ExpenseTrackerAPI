from sqlalchemy.orm import Session
from app.models.expense import Expense

class ExpenseRepository:

    def __init__(self, db: Session):
        self.db = db

    # create expense
    def create(self, title: str, amount, category: str, description: str, expense_date, owner_id: int):

        expense = Expense(
            title=title,
            amount=amount,
            category=category,
            description=description,
            expense_date=expense_date,
            owner_id=owner_id
        )

        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)

        return expense

    # get expense
    def get_all(self, expense_id: int, owner_id: int):
        return self.db.query(Expense).filter(Expense.id == expense_id, Expense.owner_id == owner_id).first()


    # update expense
    def update(self, expense: Expense, update_data: dict):
        for key, value in update_data.items():
            setattr(expense, key, value)

        self.db.commit()
        self.db.refresh(expense)

        return expense

    # delete expense
    def delete(self, expense: Expense):
        self.db.delete(expense)
        self.db.commit()
        