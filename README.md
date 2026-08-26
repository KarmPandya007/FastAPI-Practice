# User Details CRUD API (FastAPI & Supabase PostgreSQL)

A production-ready User Management CRUD application built with **FastAPI**, **SQLAlchemy ORM**, **Pydantic v2**, and **Supabase PostgreSQL**. Includes a single-page interactive management dashboard.

## 🚀 Features

- **RESTful API**: Full CRUD endpoints (`POST`, `GET`, `PUT`, `DELETE`) for user management.
- **Supabase PostgreSQL Integration**: Direct connection with safe URL password encoding and connection pooling.
- **Data Validation**: Strict Pydantic email and data validation.
- **Search & Pagination**: Built-in query filtering by name, email, or role with offset/limit pagination.
- **Interactive UI Dashboard**: Embedded web management UI served at `/`.
- **API Documentation**: Automatic Swagger UI (`/docs`) and ReDoc (`/redoc`).
- **Integration Test Suite**: Automated verification via `test_crud.py`.

---

## 🛠️ Project Structure

```text
├── database.py       # Engine creation, session management, and DB dependency
├── models.py         # SQLAlchemy ORM database models
├── schemas.py        # Pydantic request/response validation schemas
├── crud.py           # Database query functions (Create, Read, Update, Delete)
├── main.py           # FastAPI application routes & template rendering
├── templates/
│   └── index.html    # Web Management Dashboard UI
├── test_crud.py      # Integration test suite
├── requirements.txt  # Project dependencies
└── .env              # Environment variables (DB Connection)
```

---

## 💻 Local Setup & Execution

### 1. Install Dependencies
```bash
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory:
```ini
DATABASE_URI="postgresql://postgres.ttefklzjnktwxxxqmloa:YOUR_PASSWORD@aws-0-ap-northeast-1.pooler.supabase.com:6543/postgres"
```

### 3. Run Application Server
```bash
uvicorn main:app --reload
```
Access the application:
- **Web Dashboard**: `http://127.0.0.1:8000/`
- **Swagger Docs**: `http://127.0.0.1:8000/docs`

### 4. Run Test Suite
```bash
python test_crud.py
```