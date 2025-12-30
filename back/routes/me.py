from fastapi import APIRouter, HTTPException, Depends, Cookie, Response
from security.auth import verify_token, verify_cookie
from db.deps import get_db
from models.user import User
from models.attribute import Attribute
from schemas.models import UserProfile
from sqlalchemy.orm import Session

router = APIRouter()

# Get user info
@router.get("/")
def get_me(token = Depends(verify_cookie), db: Session = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user_id = token.get("user_id")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    attributes = db.query(Attribute).filter(Attribute.user_id == user_id).first()
    
    profile = UserProfile(
        username=user.username,
        email=user.email,
        level=user.level,
        created_at=user.created_at,
        attributes=attributes
    )

    return {"profile": profile}


# Update user info
@router.put("/profile")
def update_me(user: dict):
    return {"updated_user": user}


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
@router.post("/change-password")
def change_password(passwords: dict):
    return {"message": "Password changed successfully"}

