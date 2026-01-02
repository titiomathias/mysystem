from fastapi import APIRouter, HTTPException, Depends, Cookie, Response
from security.auth import verify_cookie
from security.security import hash_password
from db.deps import get_db
from models.user import User
from models.task_log import TaskLog
from models.attribute import Attribute
from schemas.models import UserProfile, UserUpdate
from sqlalchemy.orm import Session
from core.progression import xp_to_next_level, calculate_level_and_xp
from sqlalchemy import func

router = APIRouter()

# Get user info
@router.get("/")
def get_me(
    token=Depends(verify_cookie),
    db: Session = Depends(get_db)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user_id = token["user_id"]

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    attributes = (
        db.query(Attribute)
        .filter(Attribute.user_id == user_id)
        .first()
    )

    total_xp = (
        db.query(func.coalesce(func.sum(TaskLog.xp_earned), 0))
        .filter(TaskLog.user_id == user_id)
        .scalar()
    )

    level, current_xp = calculate_level_and_xp(total_xp)

    profile = UserProfile(
        username=user.username,
        email=user.email,
        level=level,
        current_xp=current_xp,
        next_level_xp=xp_to_next_level(level),
        created_at=user.created_at,
        attributes=attributes
    )

    return {"profile": profile}


# Update user info
@router.put("/update")
def update_me(user: UserUpdate, db: Session = Depends(get_db), token=Depends(verify_cookie)):
    user_id = token["user_id"]

    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.username is not None:
        db_user.username = user.username
    if user.email is not None:
        db_user.email = user.email

    db.commit()
    db.refresh(db_user)

    return {"message": "User updated successfully"}
    

# Delete user account
@router.delete("/")
def delete_me(user = Depends(verify_cookie), db: Session = Depends(get_db), response: Response = None):
    user = db.query(User).filter(User.id == user["user_id"]).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    response.delete_cookie(key="access_token")
    response.status_code = 204

    return {"message": "User account deleted"}


# Change user password
@router.post("/password")
def change_password(passwords: dict, user=Depends(verify_cookie), db: Session = Depends(get_db)):
    user_id = user["user_id"]

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_password = passwords.get("new_password")
    confirm_password = passwords.get("confirm_password")

    if new_password != confirm_password or new_password is None or confirm_password is None:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    if len(new_password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long")

    user.password_hash = hash_password(new_password)

    db.commit()
    db.refresh(user)

    return {"message": "Password changed successfully"}

