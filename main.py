import os
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import database
import models
import schemas
import crud

# Initialize Database Tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="User Details CRUD API",
    description="A simple, production-ready User Details CRUD Application using FastAPI & PostgreSQL.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to dashboard template
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates", "index.html")

# ================================
# API Endpoints
# ================================

@app.get("/health", tags=["Health"])
def health_check(db: Session = Depends(database.get_db)):
    """Health check endpoint validating database connectivity."""
    db_status = "connected"
    try:
        db.execute(database.text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
        
    return {
        "status": "healthy",
        "database_status": db_status,
        "database_engine": database.engine.name
    }

@app.post(
    "/api/v1/users/",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"],
    summary="Create a new user"
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(database.get_db)
):
    """
    Create a new user in the system.
    - Checks for existing user with the same email.
    - Returns HTTP 400 if email is already registered.
    """
    existing_user = crud.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email '{user.email}' already exists."
        )
    return crud.create_user(db=db, user_data=user)

@app.get(
    "/api/v1/users/",
    response_model=schemas.PaginatedUserResponse,
    tags=["Users"],
    summary="Get paginated users list"
)
def get_users(
    skip: int = Query(0, ge=0, description="Records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Records limit"),
    search: Optional[str] = Query(None, description="Search by name, email or role"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(database.get_db)
):
    """
    Fetch a list of users with optional filtering and pagination.
    """
    users, total = crud.get_users(
        db=db, skip=skip, limit=limit, search=search, is_active=is_active
    )
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "users": users
    }

@app.get(
    "/api/v1/users/{user_id}",
    response_model=schemas.UserResponse,
    tags=["Users"],
    summary="Get user by ID"
)
def get_user(
    user_id: int,
    db: Session = Depends(database.get_db)
):
    """
    Retrieve user details by user ID.
    Returns HTTP 404 if user is not found.
    """
    db_user = crud.get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found."
        )
    return db_user

@app.put(
    "/api/v1/users/{user_id}",
    response_model=schemas.UserResponse,
    tags=["Users"],
    summary="Update user details"
)
def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: Session = Depends(database.get_db)
):
    """
    Update details of an existing user.
    - Returns HTTP 404 if user is not found.
    - Returns HTTP 400 if updating email to one that is already taken by another user.
    """
    db_user = crud.get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found."
        )
        
    if user_update.email and user_update.email.lower().strip() != db_user.email.lower():
        email_owner = crud.get_user_by_email(db=db, email=user_update.email)
        if email_owner and email_owner.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email '{user_update.email}' is already taken by another user."
            )

    updated_user = crud.update_user(db=db, user_id=user_id, user_update=user_update)
    return updated_user

@app.delete(
    "/api/v1/users/{user_id}",
    tags=["Users"],
    summary="Delete a user"
)
def delete_user(
    user_id: int,
    db: Session = Depends(database.get_db)
):
    """
    Delete a user by ID.
    Returns HTTP 404 if user is not found.
    """
    success = crud.delete_user(db=db, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found."
        )
    return {"message": f"User with ID {user_id} successfully deleted."}

# ================================
# Web Management UI Endpoint
# ================================

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def serve_dashboard():
    """Serves an interactive single-page web management dashboard for User Details CRUD operations."""
    if os.path.exists(TEMPLATE_PATH):
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>User Details CRUD API</h1><p>API documentation available at <a href='/docs'>/docs</a></p>"