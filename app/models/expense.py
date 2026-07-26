from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey, Numeric, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class Expense(Base):

    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(100), nullable=False)

    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    category: Mapped[str] = mapped_column(String(50), nullable=False)

    description: Mapped[str] = mapped_column(String(255), nullable=True)

    expense_date: Mapped[datetime] = mapped_column(Date, nullable=False)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="expenses")
