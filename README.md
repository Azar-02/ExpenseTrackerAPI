# Expense Tracker API

A RESTful Expense Tracker API built using FastAPI.

This project allows users to securely manage their daily expenses with JWT Authentication, advanced filtering, searching, pagination, receipt uploads, dashboard analytics, and CSV export.

---

## Features

- User Registration
- JWT Authentication
- Login
- Expense CRUD
- Pagination
- Search
- Filtering
- Sorting
- Dashboard Analytics
- Receipt Upload
- CSV Export
- Category Management
- Swagger API Documentation

---

## Tech Stack

- Python 3
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- JWT Authentication
- Passlib
- Uvicorn

---

## Project Structure

```
app/
│
├── database/
├── models/
├── repositories/
├── routers/
├── schemas/
├── services/
└── utils/
```

---

## Installation

Clone the repository

```bash
git clone <repository_url>
```

Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
uvicorn app.main:app --reload
```

---

## API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## Main Features

### Authentication

- Register
- Login
- JWT Tokens

### Expenses

- Create Expense
- Update Expense
- Delete Expense
- Search
- Pagination
- Filtering
- Sorting

### Dashboard

- Total Expenses
- Today's Expenses
- Monthly Expenses
- Highest Expense
- Category Summary

### Receipt Upload

- JPG/JPEG/PNG Support
- 5 MB Validation
- MIME Validation
- Automatic Receipt Replacement

### Export

- CSV Export

---

## Future Improvements

- PostgreSQL Support
- Docker
- Alembic Migrations
- Unit Tests
- Background Tasks
- Redis Caching
- CI/CD

---

## Author

Azar S
