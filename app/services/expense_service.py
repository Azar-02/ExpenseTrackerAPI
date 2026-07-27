from datetime import date
from decimal import Decimal
from typing import Optional
import os
import shutil
import uuid

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.expense_repository import ExpenseRepository
from app.schemas.dashboard import (
    CategorySummary,
    DashboardResponse,
    HighestExpense,
)
from app.schemas.expense import ExpenseCreate, ExpenseUpdate
import csv
from io import StringIO



class ExpenseService:

    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

    def __init__(self, db: Session):
        self.repository = ExpenseRepository(db)

    def create_expense(
        self,
        expense_data: ExpenseCreate,
        current_user: User,
    ):
        return self.repository.create(
            title=expense_data.title,
            amount=expense_data.amount,
            category=expense_data.category,
            description=expense_data.description,
            expense_date=expense_data.expense_date,
            owner_id=current_user.id,
        )

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
        search: Optional[str] = None,
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
            search=search,
        )

    def get_expense(
        self,
        expense_id: int,
        current_user: User,
    ):
        expense = self.repository.get_by_id(
            expense_id,
            current_user.id,
        )

        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Expense not found",
            )

        return expense

    def update_expense(
        self,
        expense_id: int,
        expense_data: ExpenseUpdate,
        current_user: User,
    ):
        expense = self.get_expense(
            expense_id,
            current_user,
        )

        update_data = expense_data.model_dump(
            exclude_unset=True
        )

        return self.repository.update(
            expense,
            update_data,
        )

    def delete_expense(
        self,
        expense_id: int,
        current_user: User,
    ):
        expense = self.get_expense(
            expense_id,
            current_user,
        )

        self.repository.delete(expense)

    def get_dashboard(
        self,
        owner_id: int,
    ):
        dashboard = self.repository.get_dashboard(
            owner_id
        )

        highest_expense = None

        if dashboard["highest_expense"]:
            highest_expense = HighestExpense(
                title=dashboard["highest_expense"].title,
                amount=dashboard["highest_expense"].amount,
            )

        category_summary = [
            CategorySummary(
                category=row.category,
                total=row.total,
            )
            for row in dashboard["category_summary"]
        ]

        return DashboardResponse(
            total_expenses=dashboard["total_expenses"],
            today_expenses=dashboard["today_expenses"],
            monthly_expenses=dashboard["monthly_expenses"],
            highest_expense=highest_expense,
            category_summary=category_summary,
        )

    def upload_receipt(
        self,
        expense_id: int,
        file: UploadFile,
        current_user: User,
    ):
        expense = self.get_expense(
            expense_id,
            current_user,
        )

        # --------------------------------------------------
        # Validate filename
        # --------------------------------------------------
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file selected.",
            )

        # --------------------------------------------------
        # Validate extension
        # --------------------------------------------------
        allowed_extensions = {
            ".jpg",
            ".jpeg",
            ".png",
        }

        extension = os.path.splitext(
            file.filename
        )[1].lower()

        if extension not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only JPG, JPEG and PNG files are allowed.",
            )

        # --------------------------------------------------
        # Validate MIME Type
        # --------------------------------------------------
        allowed_types = {
            "image/jpeg",
            "image/png",
        }

        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type.",
            )

        # --------------------------------------------------
        # Validate File Size
        # --------------------------------------------------
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)

        if file_size > self.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size must not exceed 5 MB.",
            )

        # --------------------------------------------------
        # Generate unique filename
        # --------------------------------------------------
        unique_filename = f"{uuid.uuid4()}{extension}"

        file_path = os.path.join(
            "uploads",
            unique_filename,
        )

        # --------------------------------------------------
        # Delete old receipt only after validations pass
        # --------------------------------------------------
        if (
            expense.receipt_url
            and os.path.exists(expense.receipt_url)
        ):
            os.remove(expense.receipt_url)

        # --------------------------------------------------
        # Save new receipt
        # --------------------------------------------------
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(
                    file.file,
                    buffer,
                )

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save receipt.",
            )

        # --------------------------------------------------
        # Update database
        # --------------------------------------------------
        return self.repository.update_receipt(
            expense,
            file_path,
        )

    def export_csv(
    self,
    current_user: User,
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    min_amount: Optional[Decimal] = None,
    max_amount: Optional[Decimal] = None,
    sort_by: str = "expense_date",
    order: str = "desc",
    search: Optional[str] = None,
    ):
        expenses = self.repository.get_all_for_export(
            owner_id=current_user.id,
            category=category,
            start_date=start_date,
            end_date=end_date,
            min_amount=min_amount,
            max_amount=max_amount,
            sort_by=sort_by,
            order=order,
            search=search,
        )

        output = StringIO()

        writer = csv.writer(output)

        writer.writerow([
            "ID",
            "Title",
            "Amount",
            "Category",
            "Description",
            "Expense Date",
            "Receipt URL",
        ])

        for expense in expenses:
            writer.writerow([
                expense.id,
                expense.title,
                float(expense.amount),
                expense.category,
                expense.description or "",
                expense.expense_date,
                expense.receipt_url or "",
            ])

        output.seek(0)

        return output