from fastapi import FastAPI

from app.database.base import Base
from app.database.connection import engine

import app.models
from app.routers.auth import router as auth_router
from app.routers.user import router as user_router
from app.routers.expense import router as expense_router
from app.routers import category
from fastapi.staticfiles import StaticFiles



Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Expense Tracker API",
    description="Backend API for Expense Tracker",
    version="1.0.0"
)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads",
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(expense_router)
app.include_router(category.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Expense Tracker API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "Expense Tracker API"
    }