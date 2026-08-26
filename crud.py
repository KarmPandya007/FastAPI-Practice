from typing import Optional, Tuple, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
import models
import schemas

def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email.lower().strip()).first()

def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    is_active: Optional[bool] = None
) -> Tuple[List[models.User], int]:
    query = db.query(models.User)
    
    if is_active is not None:
        query = query.filter(models.User.is_active == is_active)
        
    if search:
        search_term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                models.User.name.ilike(search_term),
                models.User.email.ilike(search_term),
                models.User.role.ilike(search_term)
            )
        )
        
    total = query.count()
    users = query.order_by(models.User.id.desc()).offset(skip).limit(limit).all()
    return users, total

def create_user(db: Session, user_data: schemas.UserCreate) -> models.User:
    db_user = models.User(
        name=user_data.name.strip(),
        email=user_data.email.lower().strip(),
        role=user_data.role.strip() if user_data.role else "user",
        is_active=user_data.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> Optional[models.User]:
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)
    
    # Exclude password field from direct model dict if provided for demo
    if "password" in update_data:
        update_data.pop("password")

    if "email" in update_data and update_data["email"]:
        update_data["email"] = update_data["email"].lower().strip()
        
    if "name" in update_data and update_data["name"]:
        update_data["name"] = update_data["name"].strip()

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True
