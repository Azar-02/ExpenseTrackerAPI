from fastapi import FastAPI

from app.database.base import Base
from app.database.connection import engine

import app.models


app = FastAPI(
    title="Expense Tracker API",
    description="Backend API for Expense Tracker",
    version="1.0.0"
)


Base.metadata.create_all(bind=engine)


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